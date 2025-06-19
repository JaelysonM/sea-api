from src.siasdapi.domain.ports.repositories.tokens import (
    TokenRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class TokenUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    tokens: TokenRepositoryInterface

    def __enter__(self) -> "TokenUnitOfWorkInterface":
        return self
