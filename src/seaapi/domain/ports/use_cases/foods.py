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

    def get_food(
        self, id_: int, entity: bool = False
    ) -> Union[FoodEntity, FoodOutputDto]:
        return self._get_food(id_, entity)

    def update_food(
        self, id_: int, food: FoodUpdateInputDto
    ) -> SuccessResponse:
        return self._update_food(id_, food)

    def delete_food(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_food(id_)

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
        self, id_: int, food: FoodUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_food(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError
