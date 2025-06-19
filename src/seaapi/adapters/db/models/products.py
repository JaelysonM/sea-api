from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Float,
    ForeignKey,
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

        self.product_variant = Table(
            "products_variants",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "product_id",
                Integer,
                ForeignKey(
                    "products.id", ondelete="CASCADE"
                ),
                nullable=False,
                primary_key=True,
            ),
            Column("name", String(255), nullable=False),
            Column(
                "description", String(255), nullable=True
            ),
            Column("min_price", Float, nullable=False),
            Column("max_price", Float, nullable=False),
            Column("duration", Integer, nullable=False),
        )

    def register(self):

        self.mapper_registry.map_imperatively(
            ProductEntity,
            self.product
        )

        super().register()
