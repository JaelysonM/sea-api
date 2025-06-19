from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.stores import (
    StoreSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.stores import (
    StoreUnitOfWorkInterface,
)

from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class StoreSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, StoreUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.stores = StoreSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
