from abc import abstractmethod
from typing import Optional, List, Tuple
from src.siasdapi.domain.entities import UserEntity
from src.siasdapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.siasdapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class UserRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = UserEntity

    def find_by_email(self, email: str) -> UserEntity:
        user = self._find_by_email(email)
        return user

    def is_available(self, email: str) -> bool:
        return self._is_available(email)

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[UserEntity], int]:
        return self._find_all(
            params=params,
        )

    @abstractmethod
    def _find_by_email(self, email: str) -> UserEntity:
        raise NotImplementedError

    @abstractmethod
    def _is_available(self, email: str) -> bool:
        raise NotImplementedError
