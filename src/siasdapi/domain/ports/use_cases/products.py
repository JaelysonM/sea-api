import abc
from typing import Union

from src.siasdapi.domain.entities import (
    ProductEntity,
)
from src.siasdapi.domain.dtos.products import (
    ProductCreateInputDto,
    ProductUpdateInputDto,
    ProductOutputDto,
    ProductChildCreateInputDto,
    ProductScheduleInputDto,
    ProductScheduleOutputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)


class ProductServiceInterface(abc.ABC):
    def create(
        self, product: ProductCreateInputDto, scheduler
    ) -> SuccessResponse:
        return self._create(product, scheduler)

    def create_child(
        self,
        id_: int,
        product_child: ProductChildCreateInputDto,
    ) -> SuccessResponse:
        return self._create_child(id_, product_child)

    def get_product_schedule(
        self,
        id_: int,
        product_schedule: ProductScheduleInputDto,
    ) -> ProductScheduleOutputDto:
        return self._get_product_schedule(
            id_, product_schedule
        )

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
    def _create_child(
        self,
        id: int,
        product_child: ProductChildCreateInputDto,
        scheduler,
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

    @abc.abstractmethod
    def _get_product_schedule(
        self,
        id_: int,
        product_schedule: ProductScheduleInputDto,
    ) -> ProductScheduleOutputDto:
        raise NotImplementedError
