from sqlalchemy.orm import Session
from src.seaapi.adapters.repositories.sqlalchemy.stores import (
    StoreSqlAlchemyRepository,
)
from src.seaapi.domain.ports.unit_of_works.stores import (
    StoreUnitOfWorkInterface,
)

from src.seaapi.adapters.unit_of_works.shared import (
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
