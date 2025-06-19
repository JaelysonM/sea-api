from typing import Optional, List, Tuple
from src.siasdapi.domain.entities import ProductEntity
from src.siasdapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.siasdapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class ProductRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = ProductEntity

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[ProductEntity], int]:
        return self._find_all(
            params=params,
        )
