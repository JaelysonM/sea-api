from src.siasdapi.domain.ports.repositories.permissions import (
    PermissionRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class PermissionUnitOfWorkInterface(
    DefaultUnitOfWorkInterface
):
    permissions: PermissionRepositoryInterface

    def __enter__(self) -> "PermissionUnitOfWorkInterface":
        return self
