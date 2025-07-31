from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional, List

from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.entities.food_measurement_entity import (
    FoodMeasurementEntity,
)
from src.seaapi.domain.entities.base import BaseEntity
from src.seaapi.config.settings import settings

from src.seaapi.domain.ports.shared.exceptions import (
    MealAlreadyFinishedException,
)


@dataclass
class MealEntity(BaseEntity):
    id: int
    created_at: datetime
    user_id: int
    final_price: float
    plate_identifier: str

    finished: bool

    food_measurements: List[FoodMeasurementEntity] = field(
        default_factory=list,
    )

    class Meta:
        verbose = "Refeição"
        display_name = "Meal"
        name = "food"
        search = []
        filters = [
            "id",
            "created_at",
            "user_id",
            "final_price",
            "finished",
        ]
        composite_field = "user_id"
        active_field = None
        joins = []
        masculine = False

    @property
    def total_calories(self) -> float:
        # calories por 100g, weight em kg → weight * 1000 g / 100 g = weight * 10
        return sum(
            measurement.per_hundred_grams_calories()
            for measurement in self.valid_food_measurements
        )

    @property
    def total_carbs(self) -> float:
        return sum(
            measurement.per_hundred_grams_carbs()
            for measurement in self.valid_food_measurements
        )

    @property
    def total_fat(self) -> float:
        return sum(
            measurement.per_hundred_grams_fat()
            for measurement in self.valid_food_measurements
        )

    @property
    def total_protein(self) -> float:
        return sum(
            measurement.per_hundred_grams_protein()
            for measurement in self.valid_food_measurements
        )

    @property
    def total_weight(self) -> float:
        # soma em kg, converte pra g
        return sum(
            measurement.weight
            for measurement in self.valid_food_measurements
        )

    def recalculate_final_price(self) -> float:
        if not self.total_weight:
            return 0.0
        return round(
            (self.total_weight / 1000)
            * settings.PRICE_PER_KG,
            2,
        )

    def finish(self) -> None:
        if self.finished:
            raise MealAlreadyFinishedException()
        self.finished = True
        self.final_price = self.recalculate_final_price()

    @property
    def valid_food_measurements(
        self,
    ) -> List[FoodMeasurementEntity]:
        """Returns a list of valid food measurements."""
        return [
            measurement
            for measurement in self.food_measurements
            if measurement.food.scale_id is not None
        ]

    def to_beautiful_dict(
        self,
        storage_service: Optional[
            StorageServiceInterface
        ] = None,
    ) -> dict:
        data = self.to_dict()

        beautiful_food_measurements = [
            measurement.to_beautiful_dict(
                storage_service=storage_service
            )
            for measurement in self.valid_food_measurements
        ]

        data.update(
            {
                "total_calories": self.total_calories,
                "total_carbs": self.total_carbs,
                "total_fat": self.total_fat,
                "total_protein": self.total_protein,
                "total_weight": self.total_weight,
                "food_measurements": beautiful_food_measurements,
            }
        )
        return data

    def add_food_measurement(
        self, food_measurement: FoodMeasurementEntity
    ) -> None:
        if self.finished:
            raise MealAlreadyFinishedException()

        create = True

        # Verify if the food measurement already exists
        for existing_measurement in self.food_measurements:
            if (
                existing_measurement.food_id
                == food_measurement.food_id
            ):
                existing_measurement.weight = (
                    food_measurement.weight
                )
                create = False

        if create:
            self.food_measurements.append(food_measurement)
        self.final_price = self.recalculate_final_price()


def meal_model_factory(
    user_id: int,
    plate_identifier: str,
    final_price: float = 0,
    finished: bool = False,
    created_at: datetime = datetime.now(),
    id: Optional[int] = None,
) -> MealEntity:
    return MealEntity(
        id=id,
        created_at=created_at,
        user_id=user_id,
        plate_identifier=plate_identifier,
        final_price=final_price,
        finished=finished,
    )
