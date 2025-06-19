from typing import List, Optional
from pydantic import BaseModel
from src.siasdapi.domain.dtos.mics import (
    partial,
    PaginationParams,
    PaginationData,
)
from src.siasdapi.domain.dtos.stores import StoreOutputDto
from src.siasdapi.domain.dtos.products import (
    ProductOutputDto,
)


class SectionCreateInputDto(BaseModel):
    store_id: int
    title: str
    description: Optional[str]


@partial
class SectionUpdateInputDto(BaseModel):
    title: Optional[str]
    description: Optional[str]


class SectionOutputDto(BaseModel):
    id: int
    store: StoreOutputDto
    title: str
    description: Optional[str]
    products: List[ProductOutputDto]

    class Config:
        orm_mode = True


class SectionPaginationData(PaginationData):
    data: List[SectionOutputDto]


class SectionPaginationParams(PaginationParams):
    store_id: Optional[int]
    name: Optional[str]
    description: Optional[str]
