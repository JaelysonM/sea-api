import logging
from typing import Optional
from src.seaapi.domain.ports.use_cases.food_events import (
    FoodEventPublisherInterface,
)
from src.seaapi.domain.ports.unit_of_works.scales import (
    ScaleUnitOfWorkInterface,
)
from src.seaapi.domain.ports.services.messaging import (
    EventBusInterface,
)
from src.seaapi.domain.entities import (
    FoodEntity,
    ScaleEntity,
)
from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)

logger = logging.getLogger(__name__)


class FoodEventPublisher(FoodEventPublisherInterface):
    def __init__(
        self,
        event_bus: EventBusInterface,
        scale_uow: ScaleUnitOfWorkInterface,
    ):
        self.event_bus = event_bus
        self.scale_uow = scale_uow

    def schedule_event_publication(
        self,
        event_coro,
        background_tasks: Optional[object] = None,
    ):
        """
        Agenda publicação de evento usando APENAS BackgroundTasks.
        Se não houver BackgroundTasks disponível, loga aviso.
        """
        if background_tasks and hasattr(
            background_tasks, "add_task"
        ):
            try:
                background_tasks.add_task(
                    self._run_async_event, event_coro
                )
                logger.info(
                    "Evento agendado via BackgroundTasks"
                )
                return
            except Exception as e:
                logger.warning(
                    f"Erro ao usar BackgroundTasks: {e}"
                )

        # Sem BackgroundTasks disponível - apenas logar
        logger.warning(
            "BackgroundTasks não disponível - evento não será publicado"
        )

    async def _run_async_event(self, coro):
        try:
            await coro
        except Exception as e:
            logger.error(
                f"Erro na execução de evento assíncrono: {e}"
            )

    async def _publish_food_scale_event(
        self, event_type: str, food: FoodEntity
    ):
        scale_entity = check_or_get_entity_if_exists(
            id_=food.scale_id,
            repository="scales",
            uow=self.scale_uow,
            entity_class=ScaleEntity,
        )
        scale_serial = (
            scale_entity.serial if scale_entity else None
        )
        if not scale_serial:

            return
        await self.publish_to_scale_topic(
            event_type, food, scale_serial
        )

    async def _publish_food_scale_event_with_serial(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        await self.publish_to_scale_topic(
            event_type, food, scale_serial
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
