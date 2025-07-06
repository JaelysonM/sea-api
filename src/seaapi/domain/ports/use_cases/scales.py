import abc
from typing import Union

from src.seaapi.domain.entities import (
    ScaleEntity,
)
from src.seaapi.domain.dtos.scales import (
    ScaleCreateInputDto,
    ScaleUpdateInputDto,
    ScaleOutputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)


class ScaleServiceInterface(abc.ABC):
    def create(
        self, scale: ScaleCreateInputDto
    ) -> SuccessResponse:
        return self._create(scale)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_scale(
        self, id_: int, entity: bool = False
    ) -> Union[ScaleEntity, ScaleOutputDto]:
        return self._get_scale(id_, entity)

    def update_scale(
        self, id_: int, scale: ScaleUpdateInputDto
    ) -> SuccessResponse:
        return self._update_scale(id_, scale)

    def delete_scale(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_scale(id_)

    @abc.abstractmethod
    def _create(
        self, scale: ScaleUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_scale(
        self, id_: int, entity: bool = True
    ) -> Union[ScaleEntity, ScaleOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_scale(
        self, id_: int, scale: ScaleUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_scale(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError
