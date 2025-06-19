from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.permissions import (
    PermissionSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.permissions import (
    PermissionUnitOfWorkInterface,
)
from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class PermissionSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, PermissionUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.permissions = PermissionSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
