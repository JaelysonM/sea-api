from pydantic import BaseModel
from datetime import datetime


class Tokens(BaseModel):
    access_token: str
    refresh_token: str


class RefreshTokenDto(BaseModel):
    refresh_token: str


class TokenOutputDto(BaseModel):
    type: str
    token: str
    reference: int
    expiration: datetime
    created_at: datetime

    class Config:  # to convert non dict obj to json
        orm_mode = True


class TokenCreateInputDto(BaseModel):
    type: str
    token: str
    reference: int
    expiration: datetime
