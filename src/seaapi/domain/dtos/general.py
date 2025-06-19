from pydantic import BaseModel
from src.seaapi.domain.dtos.mics import (
    PaginationData,
    PaginationParams,
)
from typing import List, Optional


class CidadeOutputDto(BaseModel):
    id: int
    nome: str
    estado: str
    estado_sigla: str
    ibge: str


class CidadePaginationData(PaginationData):
    data: List[CidadeOutputDto]


class CidadePaginationParams(PaginationParams):
    nome: Optional[str]
    ibge: Optional[str]
    uf_id: Optional[int]
