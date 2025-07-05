from sqlalchemy import (
    Column,
    Integer,
    String,
    Table,
    Float,
    ForeignKey,
    DateTime,
    Boolean,
    func,
)
from sqlalchemy.orm import relationship
from src.seaapi.adapters.db.models.base import (
    TablesRegistration,
)
from src.seaapi.domain.entities import (
    FoodEntity,
    ScaleEntity,
    FoodMeasurementEntity,
    MealEntity,
)


class FoodsTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):
        self.scale = Table(
            "scales",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column("name", String(255), nullable=False),
            Column(
                "serial",
                String(255),
                nullable=True,
                unique=True,
            ),
        )

        self.food = Table(
            "foods",
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
            Column(
                "calories",
                Float,
                nullable=False,
            ),
            Column(
                "carbs",
                Float,
                nullable=False,
            ),
            Column(
                "fat",
                Float,
                nullable=False,
            ),
            Column(
                "protein",
                Float,
                nullable=False,
            ),
            Column(
                "scale_id",
                ForeignKey("scales.id"),
                nullable=True,
            ),
        )

        self.meal = Table(
            "meals",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "created_at",
                DateTime,
                server_default=func.now(),
                nullable=False,
            ),
            Column(
                "user_id",
                ForeignKey("users.id"),
                nullable=False,
            ),
            Column(
                "final_price",
                Float,
                nullable=False,
                server_default="0.0",
            ),
            Column(
                "finished",
                Boolean,
                nullable=False,
                server_default="false",
            ),
        )

        self.food_measurement = Table(
            "food_measurements",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "meal_id",
                ForeignKey("meals.id"),
                nullable=False,
            ),
            Column(
                "food_id",
                ForeignKey("foods.id"),
                nullable=False,
            ),
            Column(
                "weight",
                Float,
                nullable=False,
            ),
        )

    def register(self):

        self.mapper_registry.map_imperatively(
            ScaleEntity, self.scale
        )

        self.mapper_registry.map_imperatively(
            FoodEntity,
            self.food,
            properties={
                "scale": relationship(
                    ScaleEntity,
                    lazy="joined",
                )
            },
        )

        primary_join = (
            self.food_measurement.c.meal_id
            == self.meal.c.id
        )

        self.mapper_registry.map_imperatively(
            FoodMeasurementEntity,
            self.food_measurement,
            properties={
                "food": relationship(
                    FoodEntity,
                    lazy="joined",
                )
            },
        )

        self.mapper_registry.map_imperatively(
            MealEntity,
            self.meal,
            properties={
                "food_measurements": relationship(
                    FoodMeasurementEntity,
                    primaryjoin=primary_join,
                    lazy="subquery",
                )
            },
        )

        super().register()
