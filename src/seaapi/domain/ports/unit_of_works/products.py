from src.seaapi.domain.ports.repositories.products import (
    ProductRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class ProductUnitOfWorkInterface(
    DefaultUnitOfWorkInterface
):
    products: ProductRepositoryInterface

    def __enter__(self) -> "ProductUnitOfWorkInterface":
        return self
