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

    def find_current_meal(
        self, user_id: int
    ) -> Optional[MealEntity]:
        return self._find_current_meal(
            user_id=user_id,
        )

    def find_meal_by_plate(
        self, plate_identifier: str
    ) -> Optional[MealEntity]:
        return self._find_meal_by_plate(
            plate_identifier=plate_identifier,
        )

    def exists_meal_by_plate(
        self, plate_identifier: str
    ) -> bool:
        return (
            self.find_meal_by_plate(plate_identifier)
            is not None
        )

    @abc.abstractmethod
    def _exists_non_finished_meal(
        cls, user_id: int
    ) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    def _find_current_meal(
        cls, user_id: int
    ) -> Optional[MealEntity]:
        raise NotImplementedError

    @abc.abstractmethod
    def _find_meal_by_plate(
        cls, plate_identifier: str
    ) -> Optional[MealEntity]:
        raise NotImplementedError
