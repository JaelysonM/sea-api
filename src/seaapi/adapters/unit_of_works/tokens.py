from sqlalchemy.orm import Session
from src.seaapi.adapters.repositories.sqlalchemy.tokens import (
    TokenSqlAlchemyRepository,
)
from src.seaapi.domain.ports.unit_of_works.tokens import (
    TokenUnitOfWorkInterface,
)
from src.seaapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class TokenSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, TokenUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.tokens = TokenSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
