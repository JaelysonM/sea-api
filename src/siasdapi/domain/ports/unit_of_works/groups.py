from src.siasdapi.domain.ports.repositories.groups import (
    GroupRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class GroupUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    groups: GroupRepositoryInterface

    def __enter__(self) -> "GroupUnitOfWorkInterface":
        return self
