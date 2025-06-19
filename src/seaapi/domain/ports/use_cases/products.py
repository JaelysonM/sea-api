import abc
from typing import Union

from src.seaapi.domain.entities import (
    ProductEntity,
)
from src.seaapi.domain.dtos.products import (
    ProductCreateInputDto,
    ProductUpdateInputDto,
    ProductOutputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)


class ProductServiceInterface(abc.ABC):
    def create(
        self, product: ProductCreateInputDto, scheduler
    ) -> SuccessResponse:
        return self._create(product, scheduler)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_product(
        self, id_: int, entity: bool = False
    ) -> Union[ProductEntity, ProductOutputDto]:
        return self._get_product(id_, entity)

    def update_product(
        self,
        id_: int,
        product: ProductUpdateInputDto,
        scheduler,
    ) -> SuccessResponse:
        return self._update_product(id_, product, scheduler)

    def delete_product(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_product(id_)

    @abc.abstractmethod
    def _create(
        self, product: ProductUpdateInputDto, scheduler
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_product(
        self, id_: int, entity: bool = True
    ) -> Union[ProductEntity, ProductOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_product(
        self,
        id_: int,
        product: ProductUpdateInputDto,
        scheduler,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_product(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError
