from sqlalchemy.orm import Session
from src.siasdapi.adapters.repositories.sqlalchemy.products import (
    ProductSqlAlchemyRepository,
)
from src.siasdapi.domain.ports.unit_of_works.products import (
    ProductUnitOfWorkInterface,
)

from src.siasdapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class ProductSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, ProductUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.products = ProductSqlAlchemyRepository(
            self.session
        )
        return super().__enter__()
