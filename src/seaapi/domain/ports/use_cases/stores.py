import abc
from typing import Union

from src.seaapi.domain.entities import (
    StoreEntity,
)
from src.seaapi.domain.dtos.stores import (
    StoreCreateInputDto,
    StoreUpdateInputDto,
    StoreOutputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)
from src.seaapi.domain.dtos.mics import UploadedFile


class StoreServiceInterface(abc.ABC):
    def create(
        self, store: StoreCreateInputDto
    ) -> SuccessResponse:
        return self._create(store)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_store(
        self, id_: int, entity: bool = False
    ) -> Union[StoreEntity, StoreOutputDto]:
        return self._get_store(id_, entity)

    def update_store(
        self, id_: int, store: StoreUpdateInputDto
    ) -> SuccessResponse:
        return self._update_store(id_, store)

    def delete_store(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_store(id_)

    def update_store_icon(
        self, id_: int, file: UploadedFile, scheduler=None
    ) -> SuccessResponse:
        return self._update_store_icon(id_, file, scheduler)

    @abc.abstractmethod
    def _create(
        self, store: StoreUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_store(
        self, id_: int, entity: bool = True
    ) -> Union[StoreEntity, StoreOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_store(
        self, id_: int, store: StoreUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_store(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_store_icon(
        self, id_: int, file: UploadedFile, scheduler=None
    ) -> SuccessResponse:
        raise NotImplementedError
