from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Float,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from src.siasdapi.adapters.db.models.base import (
    TablesRegistration,
)
from src.siasdapi.domain.entities import (
    SectionEntity,
    ProductEntity,
    ProductChildEntity,
    StoreEntity,
)


class ProductsTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):
        self.section = Table(
            "sections",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "store_id",
                Integer,
                ForeignKey("stores.id", ondelete="CASCADE"),
                nullable=False,
            ),
            Column("title", String(255), nullable=False),
            Column(
                "description", String(255), nullable=True
            ),
        )

        self.product = Table(
            "products",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "section_id",
                Integer,
                ForeignKey(
                    "sections.id", ondelete="CASCADE"
                ),
                nullable=False,
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
            ProductChildEntity, self.product_variant
        )

        self.mapper_registry.map_imperatively(
            ProductEntity,
            self.product,
            properties={
                "children": relationship(
                    ProductChildEntity,
                    lazy="subquery",
                    viewonly=True,
                ),
            },
        )

        self.mapper_registry.map_imperatively(
            SectionEntity,
            self.section,
            properties={
                "products": relationship(
                    ProductEntity,
                    lazy="subquery",
                    viewonly=True,
                ),
                "store": relationship(
                    StoreEntity,
                    lazy="joined",
                    viewonly=True,
                ),
            },
        )

        super().register()
