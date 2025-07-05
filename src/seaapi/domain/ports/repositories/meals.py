import abc
from typing import Optional, List, Tuple
from src.seaapi.domain.entities import MealEntity
from src.seaapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.seaapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class MealRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = MealEntity

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[MealEntity], int]:
        return self._find_all(
            params=params,
        )

    def exists_non_finished_meal(
        self, user_id: int
    ) -> bool:
        return self._exists_non_finished_meal(
            user_id=user_id,
        )

    @abc.abstractmethod
    def _exists_non_finished_meal(
        cls, user_id: int
    ) -> bool:
        raise NotImplementedError
