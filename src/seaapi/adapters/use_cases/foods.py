from typing import Union, Optional
from datetime import datetime
import asyncio
import logging
from contextlib import suppress
from src.seaapi.domain.entities import (
    FoodEntity,
    ScaleEntity,
)
from src.seaapi.domain.dtos.foods import (
    FoodCreateInputDto,
    FoodOutputDto,
    FoodUpdateInputDto,
    FoodPaginationParams,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
    PaginationOptions,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.ports.services.messaging import (
    EventBusInterface,
)
from src.seaapi.domain.entities.food_entity import (
    food_model_factory,
)
from src.seaapi.domain.ports.unit_of_works.foods import (
    FoodUnitOfWorkInterface,
)
from src.seaapi.domain.ports.unit_of_works.scales import (
    ScaleUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.foods import (
    FoodServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    NotAuthorizedException,
)


from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)

logger = logging.getLogger(__name__)


class FoodService(FoodServiceInterface):
    def __init__(
        self,
        uow: FoodUnitOfWorkInterface,
        scale_uow: ScaleUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
        event_bus: EventBusInterface,
    ):
        self.uow = uow
        self.scale_uow = scale_uow
        self.storage_service = storage_service
        self.event_bus = event_bus

    def _schedule_event_publication(
        self,
        coro,
        background_tasks: Optional[object] = None,
    ):
        if background_tasks and hasattr(
            background_tasks, "add_task"
        ):
            try:
                background_tasks.add_task(
                    self._run_async_event, coro
                )
                return
            except Exception as e:
                logger.warning(
                    f"Erro ao usar BackgroundTasks: {e}"
                )

        with suppress(RuntimeError):
            loop = asyncio.get_running_loop()
            task = loop.create_task(coro)
            task.add_done_callback(
                self._handle_event_task_result
            )
            return

        try:
            asyncio.run(coro)
        except Exception as e:
            logger.error(f"Erro ao executar evento: {e}")

    async def _run_async_event(self, coro):
        try:
            await coro
        except Exception as e:
            logger.error(
                f"Erro na execução de evento assíncrono: {e}"
            )

    def _handle_event_task_result(self, task):
        with suppress(Exception):
            if task.exception():
                logger.error(
                    f"Erro na publicação de evento: {task.exception()}"
                )

    async def _publish_food_scale_event(
        self,
        event_type: str,
        food: FoodEntity,
    ):
        try:

            scale_entity = check_or_get_entity_if_exists(
                id_=food.scale_id,
                repository="scales",
                uow=self.scale_uow,
                entity_class=ScaleEntity,
            )

            scale_serial = (
                scale_entity.serial
                if scale_entity
                else None
            )

            if not scale_serial:
                logger.warning(
                    f"Serial da balança não encontrado para evento {event_type}"
                )
                return

            await self._publish_to_scale_topic(
                event_type, food, scale_serial
            )

        except Exception as e:
            logger.error(
                f"Erro ao publicar evento {event_type}: {e}"
            )

    async def _publish_food_scale_event_with_serial(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        try:
            await self._publish_to_scale_topic(
                event_type, food, scale_serial
            )
        except Exception as e:
            logger.error(
                f"Erro ao publicar evento {event_type} com serial {scale_serial}: {e}"
            )

    async def _publish_to_scale_topic(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        topic = f"foods.{scale_serial}"
        if event_type in ["attached", "updated"]:
            payload = {
                "food_id": food.id,
                "name": food.name,
                "calories": food.calories,
                "protein": food.protein,
                "carbs": food.carbs,
                "fat": food.fat,
                "retain": True,
            }

            await self.event_bus.publish(topic, payload)

        elif event_type in ["detached", "deleted"]:
            await self.event_bus.publish(
                topic, {"retain": True}
            )
            logger.info(
                f"Evento '{event_type}' (mensagem vazia) publicado no tópico {topic}"
            )

    def _create(
        self, food: FoodCreateInputDto
    ) -> SuccessResponse:

        with self.uow:
            new_food = food_model_factory(
                name=food.name,
                description=food.description,
                calories=food.calories,
                carbs=food.carbs,
                fat=food.fat,
                protein=food.protein,
            )

            self.uow.foods.create(new_food)

            self.uow.flush()

            if food.photo is not None:
                new_food.upload_photo(
                    storage_service=self.storage_service,
                    file=food.photo,
                    replace=True,
                )

            self.uow.commit()

            return SuccessResponse(
                message="Comida criada com sucesso!",
                code="food_registered",
                status_code=201,
            )

    def _update_food(
        self,
        id_: int,
        food: FoodUpdateInputDto,
    ) -> SuccessResponse:
        with self.uow:
            existing_food = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.foods,
                entity_class=FoodEntity,
            )

            previous_scale_id = existing_food.scale_id
            previous_scale_serial = (
                existing_food.scale.serial
                if existing_food.scale
                else None
            )

            special_fields = ["photo", "scale_id"]

            if (
                hasattr(food, "scale_id")
                and food.scale_id is not None
            ):
                if existing_food.set_scale(food.scale_id):
                    check_or_get_entity_if_exists(
                        id_=food.scale_id,
                        repository="scales",
                        uow=self.scale_uow,
                        entity_class=ScaleEntity,
                    )

            for field, value in food.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_food, field, value)

            if food.photo is not None:
                existing_food.upload_photo(
                    storage_service=self.storage_service,
                    file=food.photo,
                    replace=True,
                )

            existing_food.updated_at = datetime.now()

            events_scheduled = []
            try:
                if (
                    previous_scale_id
                    and not existing_food.scale_id
                ):
                    if previous_scale_serial:
                        event_coro = self._publish_food_scale_event_with_serial(
                            "detached",
                            existing_food,
                            previous_scale_serial,
                        )
                        events_scheduled.append(event_coro)
                elif (
                    not previous_scale_id
                    and existing_food.scale_id
                ):
                    event_coro = (
                        self._publish_food_scale_event(
                            "attached", existing_food
                        )
                    )
                    events_scheduled.append(event_coro)
                elif (
                    previous_scale_id
                    and existing_food.scale_id
                    and previous_scale_id
                    != existing_food.scale_id
                ):
                    if previous_scale_serial:
                        event_coro = self._publish_food_scale_event_with_serial(
                            "detached",
                            existing_food,
                            previous_scale_serial,
                        )
                        events_scheduled.append(event_coro)

                    event_coro = (
                        self._publish_food_scale_event(
                            "attached", existing_food
                        )
                    )
                    events_scheduled.append(event_coro)
                elif (
                    existing_food.scale_id
                    and previous_scale_id
                    == existing_food.scale_id
                ):
                    nutritional_fields = [
                        "name",
                        "calories",
                        "protein",
                        "carbs",
                        "fat",
                    ]
                    if any(
                        hasattr(food, field)
                        and getattr(food, field) is not None
                        for field in nutritional_fields
                    ):
                        event_coro = (
                            self._publish_food_scale_event(
                                "updated", existing_food
                            )
                        )
                        events_scheduled.append(event_coro)
            except Exception as e:
                logger.error(
                    f"Erro ao preparar eventos: {e}"
                )

            self.uow.commit()

            for event_coro in events_scheduled:
                self._schedule_event_publication(event_coro)

            return SuccessResponse(
                message="Dados do alimento atualizados com sucesso!",
                code="food_updated",
            )

    def _get_food(
        self, id_: int, entity: bool = False
    ) -> Union[FoodEntity, FoodOutputDto]:
        with self.uow:
            food_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.foods,
                entity_class=FoodEntity,
            )
            if entity:
                return food_
            return FoodOutputDto(
                **food_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            foods, results = self.uow.foods.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    FoodOutputDto(
                        **food.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for food in foods
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _get_current_menu(
        self,
    ) -> PaginationData:
        with self.uow:
            foods, _ = self.uow.foods.find_all(
                params=FoodPaginationParams(
                    scale_id={"not": None}, page=None
                ),
            )
            return PaginationData(
                data=[
                    FoodOutputDto(
                        **food.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for food in foods
                ]
            )

    def _delete_food(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()

        with self.uow:
            existing_food = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.foods,
                entity_class=FoodEntity,
            )

            scale_serial = (
                existing_food.scale.serial
                if existing_food.scale
                else None
            )

            event_coro = None
            if existing_food.scale_id and scale_serial:
                event_coro = self._publish_food_scale_event_with_serial(
                    "deleted",
                    existing_food,
                    scale_serial,
                )

            self.uow.foods.delete(existing_food)
            self.uow.commit()

            if event_coro:
                self._schedule_event_publication(event_coro)

            return SuccessResponse(
                message="Alimento removido com sucesso!",
                code="food_removed",
            )
