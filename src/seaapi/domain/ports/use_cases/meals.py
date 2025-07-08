import abc
from typing import Union

from src.seaapi.domain.entities import (
    MealEntity,
)
from src.seaapi.domain.dtos.meals import (
    MealCreateInputDto,
    FoodMeasurementCreateInputDto,
    MealOutputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)


class MealServiceInterface(abc.ABC):
    def initialize_meal(
        self, meal: MealCreateInputDto
    ) -> SuccessResponse:
        return self._initialize_meal(meal)

    def add_meal_food_measurement(
        self,
        id: int,
        food_measurement: FoodMeasurementCreateInputDto,
    ) -> SuccessResponse:
        return self._add_meal_food_measurement(
            id, food_measurement
        )

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_user_meals(
        self,
        user_id: int,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_user_meals(
            user_id=user_id, params=params
        )

    def get_user_meal(
        self,
        user_id: int,
        id_: int,
        entity: bool = False,
    ) -> MealOutputDto:
        return self._get_user_meal(user_id, id_, entity)

    def get_current_meal(
        self,
        user_id: int,
    ) -> MealOutputDto:
        return self._get_current_meal(user_id)

    def get_meal(
        self, id_: int, entity: bool = False
    ) -> Union[MealEntity, MealOutputDto]:
        return self._get_meal(id_, entity)

    def finish_meal(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._finish_meal(id_)

    @abc.abstractmethod
    def _initialize_meal(
        self, meal: MealCreateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _add_meal_food_measurement(
        self,
        id: int,
        food_measurement: FoodMeasurementCreateInputDto,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_meal(
        self, id_: int, entity: bool = True
    ) -> Union[MealEntity, MealOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_user_meal(
        self,
        user_id: int,
        id_: int,
    ) -> MealOutputDto:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_current_meal(
        self,
        user_id: int,
    ) -> MealOutputDto:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_user_meals(
        self,
        user_id: int,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _finish_meal(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError
