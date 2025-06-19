from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
)
from src.seaapi.adapters.db.models.base import (
    TablesRegistration,
)
from src.seaapi.domain.entities import (
    ProductEntity,
)


class ProductsTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):

        self.product = Table(
            "products",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column("name", String(255), nullable=False),
            Column(
                "description", String(255), nullable=True
            ),
            Column("photo", String(255), nullable=True),
        )

    def register(self):

        self.mapper_registry.map_imperatively(
            ProductEntity, self.product
        )

        super().register()
