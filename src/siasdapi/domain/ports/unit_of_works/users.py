from src.siasdapi.domain.ports.repositories.users import (
    UserRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class UserUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    users: UserRepositoryInterface

    def __enter__(self) -> "UserUnitOfWorkInterface":
        return self
