from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.sections import (
    SectionSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.sections import (
    SectionUnitOfWorkInterface,
)

from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class SectionSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, SectionUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.sections = SectionSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
