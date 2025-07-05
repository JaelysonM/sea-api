from src.seaapi.domain.ports.repositories.meals import (
    MealRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class MealUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    meals: MealRepositoryInterface

    def __enter__(self) -> "MealUnitOfWorkInterface":
        return self
