from src.seaapi.domain.ports.repositories.foods import (
    FoodRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class FoodUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    foods: FoodRepositoryInterface

    def __enter__(self) -> "FoodUnitOfWorkInterface":
        return self
