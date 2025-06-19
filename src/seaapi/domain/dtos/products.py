from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel
from src.seaapi.domain.dtos.mics import (
    partial,
    PaginationParams,
    PaginationData,
    UploadedFile,
)


class ProductScheduleTime(BaseModel):
    price: float
    time: str


class ProductScheduleOutputDto(BaseModel):
    best_time: Optional[time]
    closed: bool
    available_times: List[ProductScheduleTime]


class ProductCreateInputDto(BaseModel):
    name: str
    description: Optional[str]
    photo: Optional[UploadedFile]


@partial
class ProductUpdateInputDto(BaseModel):
    name: Optional[str]
    description: Optional[str]
    photo: Optional[UploadedFile]


class ProductOutputDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    photo: Optional[str]

    class Config:
        orm_mode = True


class ProductPaginationData(PaginationData):
    data: List[ProductOutputDto]


class ProductPaginationParams(PaginationParams):
    name: Optional[str]
    description: Optional[str]
