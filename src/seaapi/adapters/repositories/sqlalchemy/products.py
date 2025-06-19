from src.seaapi.domain.ports.repositories.products import (
    ProductRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class ProductSqlAlchemyRepository(
    ProductRepositoryInterface, DefaultAlchemyRepository
):
    pass
