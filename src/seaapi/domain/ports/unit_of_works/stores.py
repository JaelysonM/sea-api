from src.seaapi.domain.ports.repositories.stores import (
    StoreRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class StoreUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    stores: StoreRepositoryInterface

    def __enter__(self) -> "StoreUnitOfWorkInterface":
        return self
