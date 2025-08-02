import abc
from typing import Union

from src.seaapi.domain.entities import (
    FoodEntity,
)
from src.seaapi.domain.dtos.foods import (
    FoodCreateInputDto,
    FoodUpdateInputDto,
    FoodOutputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)
from src.seaapi.domain.dtos.nutrition import (
    NutritionCalculateInputDto,
    NutritionCalculateOutputDto,
)


class FoodServiceInterface(abc.ABC):
    def create(
        self, food: FoodCreateInputDto
    ) -> SuccessResponse:
        return self._create(food)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_current_menu(self) -> PaginationData:
        return self._get_current_menu()

    def get_food(
        self, id_: int, entity: bool = False
    ) -> Union[FoodEntity, FoodOutputDto]:
        return self._get_food(id_, entity)

    def update_food(
        self, id_: int, food: FoodUpdateInputDto, scheduler
    ) -> SuccessResponse:
        return self._update_food(id_, food, scheduler)

    def delete_food(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_food(id_)

    async def calculate_nutrition(
        self, food_data: NutritionCalculateInputDto
    ) -> NutritionCalculateOutputDto:
        return await self._calculate_nutrition(food_data)

    @abc.abstractmethod
    def _create(
        self, food: FoodUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_food(
        self, id_: int, entity: bool = True
    ) -> Union[FoodEntity, FoodOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_food(
        self, id_: int, food: FoodUpdateInputDto, scheduler
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_current_menu(
        self,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_food(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    async def _calculate_nutrition(
        self, food_data: NutritionCalculateInputDto
    ) -> NutritionCalculateOutputDto:
        raise NotImplementedError
