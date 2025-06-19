from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.groups import (
    GroupSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.groups import (
    GroupUnitOfWorkInterface,
)
from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class GroupSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, GroupUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.groups = GroupSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
