from typing import List, Optional, Set
from datetime import datetime
from pydantic import BaseModel, EmailStr
from src.seaapi.domain.dtos.groups import (
    ReducedGroupDto,
)
from src.seaapi.domain.dtos.mics import (
    PaginationData,
    PaginationParams,
    StrongPassword,
    partial,
)


# properties required during user creation
class UserCreateInputDto(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    password: StrongPassword
    is_active: bool = True
    is_super_user: bool = False
    groups: Optional[Set[int]]


@partial
class UserSoftUpdateInputDto(BaseModel):
    first_name: str
    last_name: str

    email: EmailStr
    password: str
    new_password: StrongPassword


@partial
class UserUpdateInputDto(UserSoftUpdateInputDto):
    is_active: bool = True
    is_super_user: bool = False
    groups: Set[int]


class UserLoginInputDto(BaseModel):
    email: EmailStr
    password: str


class UserForgotPasswordInputDto(BaseModel):
    email: EmailStr


class UserRecoverPasswordInputDto(BaseModel):
    new_password: StrongPassword


class UserOutputDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    is_active: bool
    is_super_user: bool
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime]
    permissions: List[str]
    groups: List[ReducedGroupDto]

    class Config:  # to convert non dict obj to json
        orm_mode = True


class ReducedUserDto(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr


class UserPaginationData(PaginationData):
    data: List[UserOutputDto]


class UserPaginationParams(PaginationParams):
    id: Optional[int]
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    is_active: Optional[bool]
    is_super_user: Optional[bool]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    groups: Optional[str]
