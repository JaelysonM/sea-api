from typing import List, Optional
from pydantic import BaseModel
from src.seaapi.domain.dtos.mics import (
    partial,
    PaginationParams,
    PaginationData,
)


class ScaleCreateInputDto(BaseModel):
    name: str
    serial: str


@partial
class ScaleUpdateInputDto(BaseModel):
    name: str
    serial: str


class ScaleOutputDto(BaseModel):
    id: int
    name: str
    serial: str
    is_attached: bool

    class Config:
        orm_mode = True


class ScalePaginationData(PaginationData):
    data: List[ScaleOutputDto]


class ScalePaginationParams(PaginationParams):
    name: Optional[str]
    serial: Optional[str]
    is_attached: Optional[bool]
