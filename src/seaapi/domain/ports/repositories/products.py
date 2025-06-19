from typing import Optional, List, Tuple
from src.seaapi.domain.entities import ProductEntity
from src.seaapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.seaapi.domain.dtos.mics import (
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
