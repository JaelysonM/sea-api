from dataclasses import dataclass, field
from typing import Optional

from src.seaapi.domain.entities.base import BaseEntity
from src.seaapi.domain.entities.food_entity import (
    FoodEntity,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)


@dataclass
class FoodMeasurementEntity(BaseEntity):
    id: int
    meal_id: int
    food_id: int
    weight: float

    food: Optional[FoodEntity] = field(default=None)

    class Meta:
        verbose = "Pesagem de Comida"
        display_name = "Food Measurement"
        name = "food_measurement"
        search = []
        filters = [
            "id",
            "food_id",
            "meal_id",
            "weight",
        ]
        composite_field = None
        active_field = None
        joins = []

    def to_beautiful_dict(
        self, storage_service: StorageServiceInterface
    ) -> dict:
        data = self.to_dict()
        if self.food:
            data["food"] = self.food.to_beautiful_dict(
                storage_service=storage_service
            )
        return data


def food_measurement_model_factory(
    food_id: int,
    weight: float,
    meal_id: Optional[int] = None,
    id: Optional[int] = None,
) -> FoodMeasurementEntity:
    return FoodMeasurementEntity(
        id=id, food_id=food_id, weight=weight, meal_id=None
    )
