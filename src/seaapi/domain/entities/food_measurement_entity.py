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

    def per_hundred_grams_calories(self) -> float:
        """Returns the calories per 100 grams of the food."""
        if self.food:
            return self.food.calories * (self.weight / 100)
        return 0.0

    def per_hundred_grams_carbs(self) -> float:
        """Returns the carbs per 100 grams of the food."""
        if self.food:
            return self.food.carbs * (self.weight / 100)
        return 0.0

    def per_hundred_grams_fat(self) -> float:
        """Returns the fat per 100 grams of the food."""
        if self.food:
            return self.food.fat * (self.weight / 100)
        return 0.0

    def per_hundred_grams_protein(self) -> float:
        """Returns the protein per 100 grams of the food."""
        if self.food:
            return self.food.protein * (self.weight / 100)
        return 0.0

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
    id: Optional[int] = None,
) -> FoodMeasurementEntity:
    return FoodMeasurementEntity(
        id=id, food_id=food_id, weight=weight
    )
