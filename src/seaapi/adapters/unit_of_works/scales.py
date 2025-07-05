from sqlalchemy.orm import Session
from src.seaapi.adapters.repositories.sqlalchemy.scales import (
    ScaleSqlAlchemyRepository,
)
from src.seaapi.domain.ports.unit_of_works.scales import (
    ScaleUnitOfWorkInterface,
)

from src.seaapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class ScaleSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, ScaleUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.scales = ScaleSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
