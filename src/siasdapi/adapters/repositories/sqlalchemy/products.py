from src.siasdapi.domain.ports.repositories.products import (
    ProductRepositoryInterface,
)

from src.siasdapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class ProductSqlAlchemyRepository(
    ProductRepositoryInterface, DefaultAlchemyRepository
):
    pass
