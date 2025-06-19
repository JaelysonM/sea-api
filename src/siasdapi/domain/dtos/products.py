from datetime import date, time
from typing import List, Optional
from pydantic import BaseModel
from src.siasdapi.domain.dtos.mics import (
    partial,
    PaginationParams,
    PaginationData,
    UploadedFile,
)


class ProductScheduleInputDto(BaseModel):
    date: date
    child_id: int


class ProductScheduleTime(BaseModel):
    price: float
    time: str


class ProductScheduleOutputDto(BaseModel):
    best_time: Optional[time]
    closed: bool
    available_times: List[ProductScheduleTime]


class ProductChildOutputDto(BaseModel):
    id: int
    name: str
    description: Optional[str]
    min_price: float
    max_price: float

    duration: int


class ProductChildCreateInputDto(BaseModel):
    name: str
    description: Optional[str]
    min_price: float
    max_price: float
    duration: int


class ProductCreateInputDto(BaseModel):
    section_id: int
    name: str
    description: Optional[str]
    photo: Optional[UploadedFile]


@partial
class ProductUpdateInputDto(BaseModel):
    name: Optional[str]
    section_id: Optional[int]
    description: Optional[str]
    photo: Optional[UploadedFile]


class ProductOutputDto(BaseModel):
    id: int
    name: str
    start_price: float
    max_duration: int
    min_duration: int
    description: Optional[str]
    photo: Optional[str]
    children: List[ProductChildOutputDto]

    class Config:
        orm_mode = True


class ProductPaginationData(PaginationData):
    data: List[ProductOutputDto]


class ProductPaginationParams(PaginationParams):
    store_id: Optional[int]
    section_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
