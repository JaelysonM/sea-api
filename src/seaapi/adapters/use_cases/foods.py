from typing import Union
from datetime import datetime
from src.seaapi.domain.entities import (
    FoodEntity,
    ScaleEntity,
)
from src.seaapi.domain.dtos.foods import (
    FoodCreateInputDto,
    FoodOutputDto,
    FoodUpdateInputDto,
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


class FoodService(FoodServiceInterface):
    def __init__(
        self,
        uow: FoodUnitOfWorkInterface,
        scale_uow: ScaleUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.scale_uow = scale_uow
        self.storage_service = storage_service

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

            special_fields = ["photo", "scale_id"]

            if (
                hasattr(food, "scale_id")
                and food.scale_id is not None
            ):
                print(
                    existing_food.set_scale(food.scale_id)
                )
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
            self.uow.commit()

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

            self.uow.foods.delete(existing_food)

            self.uow.commit()

            return SuccessResponse(
                message="Alimento removido com sucesso!",
                code="food_removed",
            )
