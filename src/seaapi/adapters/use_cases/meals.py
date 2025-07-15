from typing import Union
from src.seaapi.domain.entities import (
    MealEntity,
    FoodEntity,
    UserEntity,
)
from src.seaapi.domain.entities.food_measurement_entity import (
    food_measurement_model_factory,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.dtos.meals import (
    MealCreateInputDto,
    MealOutputDto,
    MealFinishInputDto,
    FoodMeasurementCreateInputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
    PaginationOptions,
)
from src.seaapi.domain.entities.meal_entity import (
    meal_model_factory,
)
from src.seaapi.domain.ports.unit_of_works.meals import (
    MealUnitOfWorkInterface,
)
from src.seaapi.domain.ports.unit_of_works.users import (
    UserUnitOfWorkInterface,
)
from src.seaapi.domain.ports.unit_of_works.foods import (
    FoodUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.meals import (
    MealServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    MealAlreadyInProgressException,
    PlateAlreadyAttachedToMealException,
    EntityNotFoundOrDeletedException,
    NoActiveMealException,
)


from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class MealService(MealServiceInterface):
    def __init__(
        self,
        uow: MealUnitOfWorkInterface,
        food_uow: FoodUnitOfWorkInterface,
        user_uow: UserUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.food_uow = food_uow
        self.user_uow = user_uow
        self.storage_service = storage_service

    def _initialize_meal(
        self, meal: MealCreateInputDto, user_id: int
    ) -> SuccessResponse:

        with self.uow:
            check_or_get_entity_if_exists(
                id_=user_id,
                repository="users",
                uow=self.user_uow,
                entity_class=UserEntity,
            )

            if self.uow.meals.exists_meal_by_plate(
                plate_identifier=meal.plate_identifier
            ):
                raise PlateAlreadyAttachedToMealException()

            if self.uow.meals.exists_non_finished_meal(
                user_id=user_id
            ):
                raise MealAlreadyInProgressException()

            new_meal = meal_model_factory(
                user_id=user_id,
                plate_identifier=meal.plate_identifier,
            )

            self.uow.meals.create(new_meal)

            self.uow.commit()

            return SuccessResponse(
                message="Refeição criada com sucesso!",
                code="meal_registered",
                status_code=201,
            )

    def _add_meal_food_measurement(
        self,
        food_measurement: FoodMeasurementCreateInputDto,
    ) -> SuccessResponse:
        with self.uow:

            plate_identifier = (
                food_measurement.plate_identifier
            )

            existing_meal = (
                self.uow.meals.find_meal_by_plate(
                    plate_identifier=plate_identifier
                )
            )
            if not existing_meal:
                raise EntityNotFoundOrDeletedException(
                    entity=MealEntity,
                    identifier="com o identificador do prato",
                    id=plate_identifier,
                )
            with self.food_uow:
                serial = food_measurement.serial
                food_entity = self.food_uow.foods.find_food_by_scale_serial(
                    scale_serial=serial
                )

                if not food_entity:
                    raise EntityNotFoundOrDeletedException(
                        entity=FoodEntity,
                        identifier="na balança com o serial",
                        id=serial,
                    )
                food_measurement_entity = (
                    food_measurement_model_factory(
                        food_id=food_entity.id,
                        weight=food_measurement.weight,
                    )
                )

                existing_meal.add_food_measurement(
                    food_measurement_entity
                )

                self.uow.commit()

            return SuccessResponse(
                message="Pesagem de alimento adicionada com sucesso!",
                code="food_measurement_added",
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            meals, results = self.uow.meals.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    MealOutputDto(
                        **meal.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for meal in meals
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _get_meal(
        self, id_: int, entity: bool = False
    ) -> Union[MealEntity, MealOutputDto]:
        with self.uow:
            food_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.foods,
                entity_class=FoodEntity,
            )
            if entity:
                return food_
            return MealOutputDto(
                **food_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _finish_meal(
        self,
        finish_meal: MealFinishInputDto,
    ) -> SuccessResponse:
        with self.uow:
            plate_identifier = finish_meal.plate_identifier
            existing_meal = (
                self.uow.meals.find_meal_by_plate(
                    plate_identifier=plate_identifier
                )
            )

            if not existing_meal:
                raise EntityNotFoundOrDeletedException(
                    entity=MealEntity,
                    identifier="com o identificador do prato",
                    id=plate_identifier,
                )
            existing_meal.finish()

            self.uow.commit()

            return SuccessResponse(
                message="Refeição finalizada com sucesso!",
                code="meal_finished",
            )

    def _get_user_meals(
        self, user_id: int, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size

            params.user_id = user_id
            meals, results = self.uow.meals.find_all(
                params=params
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    MealOutputDto(
                        **meal.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for meal in meals
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _get_user_meal(
        self, user_id: int, id_: int
    ) -> MealOutputDto:
        with self.uow:
            meal_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.meals,
                entity_class=MealEntity,
            )
            if meal_.user_id != user_id:
                raise EntityNotFoundOrDeletedException(
                    entity=FoodEntity,
                    id=id_,
                )
            return MealOutputDto(
                **meal_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _get_current_meal(
        self, user_id: int
    ) -> MealOutputDto:
        with self.uow:
            current_meal = self.uow.meals.find_current_meal(
                user_id=user_id
            )

            if not current_meal:
                raise NoActiveMealException()

            return MealOutputDto(
                **current_meal.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )
