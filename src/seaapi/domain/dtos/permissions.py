from typing import List, Optional
from pydantic import BaseModel
from src.seaapi.domain.dtos.mics import (
    PaginationData,
    PaginationParams,
)


class PermissionCreateInputDto(BaseModel):
    name: str
    code: str


class PermissionOutputDto(BaseModel):
    id: int
    name: str
    code: str

    class Config:  # to convert non dict obj to json
        orm_mode = True


class PermissionPaginationData(PaginationData):
    data: List[PermissionOutputDto]


class PermissionPaginationParams(PaginationParams):
    name: Optional[str]
    code: Optional[str]
