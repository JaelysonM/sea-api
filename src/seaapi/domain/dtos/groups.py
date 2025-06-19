from typing import List, Set, Optional
from pydantic import BaseModel
from src.seaapi.domain.dtos.mics import (
    PaginationData,
    PaginationParams,
    partial,
)
from src.seaapi.domain.dtos.permissions import (
    PermissionOutputDto,
)


class GroupCreateInputDto(BaseModel):
    name: str
    default: bool = False
    permissions: Set[int]


@partial
class GroupUpdateInputDto(GroupCreateInputDto):
    name: str
    default: bool = False
    permissions: Set[int]


class ReducedGroupDto(BaseModel):
    id: int
    name: str
    default: bool


class GroupOutputDto(ReducedGroupDto):
    permissions: List[PermissionOutputDto]

    class Config:  # to convert non dict obj to json
        orm_mode = True


class GroupPaginationData(PaginationData):
    data: List[GroupOutputDto]


class GroupPaginationParams(PaginationParams):
    name: Optional[str]
    default: Optional[bool]
