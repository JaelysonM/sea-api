from typing import Optional, List, Tuple
from src.siasdapi.domain.entities import SectionEntity
from src.siasdapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.siasdapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class SectionRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = SectionEntity

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[SectionEntity], int]:
        return self._find_all(
            params=params,
        )
