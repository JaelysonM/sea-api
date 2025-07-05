from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from src.seaapi.domain.dtos.mics import (
    PaginationParams,
    PaginationData,
)
from src.seaapi.domain.dtos.foods import (
    FoodOutputDto,
)


class FoodMeasurementCreateInputDto(BaseModel):
    serial: str
    weight: float


class FoodMeasurementOutputDto(BaseModel):
    id: int
    food: FoodOutputDto
    weight: float


class MealCreateInputDto(BaseModel):
    user_identifier: int


class MealOutputDto(BaseModel):
    id: int
    created_at: datetime

    finished: bool
    final_price: float
    total_calories: float
    total_carbs: float
    total_fat: float
    total_protein: float
    total_weight: float

    food_measurements: List[FoodMeasurementOutputDto]

    class Config:
        orm_mode = True


class MealPaginationData(PaginationData):
    data: List[MealOutputDto]


class MealPaginationParams(PaginationParams):
    finished: Optional[bool]
    user_id: Optional[int]
