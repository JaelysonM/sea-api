from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime, time
from src.siasdapi.domain.dtos.mics import (
    CNPJCPF,
    ZipCode,
    partial,
    DayOfWeek,
    PaginationParams,
    PaginationData,
)


class StoreConfigCreateInputDto(BaseModel):
    supports_dynamic_pricing: bool


@partial
class StoreConfigUpdateInputDto(BaseModel):
    supports_dynamic_pricing: Optional[bool]


class StoreScheduleCreateInputDto(BaseModel):
    day_of_week: DayOfWeek
    opens_at: Optional[time]
    closes_at: Optional[time]
    is_closed: bool


class StoreCreateInputDto(BaseModel):
    name: str
    identifier: CNPJCPF
    address: str
    zipcode: ZipCode
    store_config: StoreConfigCreateInputDto
    schedules: List[StoreScheduleCreateInputDto]


@partial
class StoreUpdateInputDto(BaseModel):
    name: Optional[str]
    identifier: Optional[CNPJCPF]
    address: Optional[str]
    zipcode: Optional[ZipCode]
    store_config: Optional[StoreConfigUpdateInputDto]
    schedules: List[StoreScheduleCreateInputDto]


class StoreConfigOutputDto(BaseModel):
    supports_dynamic_pricing: bool
    icon: Optional[str]

    class Config:
        orm_mode = True


class StoreScheduleOutputDto(BaseModel):
    day_of_week: int
    opens_at: Optional[time]
    closes_at: Optional[time]
    is_closed: bool

    class Config:
        orm_mode = True


class StoreOutputDto(BaseModel):
    id: int
    name: str
    identifier: str
    address: str
    zipcode: str
    store_config: StoreConfigOutputDto
    schedules: List[StoreScheduleOutputDto]
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class StorePaginationData(PaginationData):
    data: List[StoreOutputDto]


class StorePaginationParams(PaginationParams):
    name: Optional[str]
    identifier: Optional[str]
    address: Optional[str]
    zipcode: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
