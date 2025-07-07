from typing import List, Optional
from pydantic import BaseModel
from src.seaapi.domain.dtos.scales import ScaleOutputDto

from src.seaapi.domain.dtos.mics import (
    partial,
    PaginationParams,
    PaginationData,
    UploadedFile,
    FilterValue,
)


class FoodCreateInputDto(BaseModel):
    name: str
    description: Optional[str]
    photo: Optional[UploadedFile]
    protein: float
    carbs: float
    fat: float
    calories: float


@partial
class FoodUpdateInputDto(BaseModel):
    name: Optional[str]
    description: Optional[str]
    photo: Optional[UploadedFile]
    protein: float
    carbs: float
    fat: float
    calories: float

    scale_id: Optional[int]


class FoodOutputDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    photo: Optional[str]
    protein: float
    carbs: float
    fat: float
    calories: float
    scale: Optional[ScaleOutputDto]

    class Config:
        orm_mode = True


class FoodPaginationData(PaginationData):
    data: List[FoodOutputDto]


class FoodPaginationParams(PaginationParams):
    name: Optional[str]
    description: Optional[str]
    scale_id: FilterValue[int]
