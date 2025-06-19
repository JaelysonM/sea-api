from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.users import (
    UserSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.users import (
    UserUnitOfWorkInterface,
)

from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class UserSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, UserUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.users = UserSqlAlchemyRepository(self.session)
        return super().__enter__()
