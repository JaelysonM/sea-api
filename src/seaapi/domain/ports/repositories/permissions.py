from abc import abstractmethod
from typing import Optional, List, Tuple
from src.seaapi.domain.entities import PermissionEntity
from src.seaapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)
from src.seaapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class PermissionRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = PermissionEntity

    def find_by_code(self, code: str) -> PermissionEntity:
        return self._find_by_code(code)

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[PermissionEntity], int]:
        return self._find_all(params=params)

    @abstractmethod
    def _find_by_code(self, code: str) -> PermissionEntity:
        raise NotImplementedError
