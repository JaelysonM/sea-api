from abc import abstractmethod
from typing import Optional, List, Tuple
from src.siasdapi.domain.entities import StoreEntity
from src.siasdapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.siasdapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class StoreRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = StoreEntity

    def find_by_identifier(
        self, identifier: str
    ) -> StoreEntity:
        user = self._find_by_identifier(identifier)
        return user

    def is_available(self, identifier: str) -> bool:
        return self._is_available(identifier)

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[StoreEntity], int]:
        return self._find_all(
            params=params,
        )

    @abstractmethod
    def _find_by_identifier(
        self, identifier: str
    ) -> StoreEntity:
        raise NotImplementedError

    @abstractmethod
    def _is_available(self, email: str) -> bool:
        raise NotImplementedError
