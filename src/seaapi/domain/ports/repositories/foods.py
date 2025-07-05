import abc
from typing import Optional, List, Tuple
from src.seaapi.domain.entities import FoodEntity
from src.seaapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)

from src.seaapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
)


class FoodRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = FoodEntity

    def find_all(
        self,
        params: Optional[
            PaginationParams
        ] = default_pagination_params,
    ) -> Tuple[List[FoodEntity], int]:
        return self._find_all(
            params=params,
        )

    def find_food_by_scale_serial(
        self, scale_serial: str
    ) -> Optional[FoodEntity]:
        return self._find_food_by_scale_serial(
            scale_serial=scale_serial,
        )

    @abc.abstractmethod
    def _find_food_by_scale_serial(
        self, scale_serial: str
    ) -> Optional[FoodEntity]:
        raise NotImplementedError
