from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    DateTime,
    func,
    ForeignKey,
    Boolean,
    Time,
)
from sqlalchemy.orm import relationship
from src.seaapi.adapters.db.models.base import (
    TablesRegistration,
)
from src.seaapi.domain.entities import (
    StoreEntity,
    StoreConfigEntity,
    StoreScheduleEntity,
)


class StoresTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):
        self.store = Table(
            "stores",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column("name", String(255), nullable=False),
            Column(
                "identifier",
                String(18),
                nullable=False,
                unique=True,
                index=True,
            ),
            Column("address", String(255), nullable=False),
            Column("zipcode", String(9), nullable=False),
            Column(
                "store_config_id",
                ForeignKey(
                    "stores_config.id", ondelete="CASCADE"
                ),
                nullable=False,
            ),
            Column(
                "created_at",
                DateTime,
                server_default=func.now(),
                nullable=False,
            ),
            Column(
                "updated_at",
                DateTime,
                server_default=func.now(),
                onupdate=func.now(),
                nullable=False,
            ),
        )

        self.store_config = Table(
            "stores_config",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "supports_dynamic_pricing",
                Boolean,
                nullable=False,
                default=False,
            ),
            Column(
                "icon",
                String,
                nullable=True,
            ),
        )

        self.store_schedule = Table(
            "store_schedules",
            self.mapper_registry.metadata,
            Column(
                "store_id",
                Integer,
                ForeignKey("stores.id", ondelete="CASCADE"),
                nullable=False,
                primary_key=True,
            ),
            Column(
                "day_of_week",
                Integer,
                nullable=False,
                primary_key=True,
            ),
            Column("opens_at", Time, nullable=True),
            Column("closes_at", Time, nullable=True),
            Column(
                "is_closed",
                Boolean,
                nullable=False,
                default=False,
            ),
        )

    def register(self):

        primaryjoin = (
            self.store.c.id
            == self.store_schedule.c.store_id
        )

        self.mapper_registry.map_imperatively(
            StoreScheduleEntity,
            self.store_schedule,
        )

        self.mapper_registry.map_imperatively(
            StoreConfigEntity,
            self.store_config,
        )

        self.mapper_registry.map_imperatively(
            StoreEntity,
            self.store,
            properties={
                "store_config": relationship(
                    StoreConfigEntity,
                    lazy="subquery",
                ),
                "schedules": relationship(
                    StoreScheduleEntity,
                    primaryjoin=primaryjoin,
                    lazy="subquery",
                ),
            },
        )

        super().register()
