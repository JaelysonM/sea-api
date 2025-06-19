import abc

from src.siasdapi.domain.dtos.tokens import (
    TokenCreateInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.siasdapi.domain.entities import TokenEntity


class TokenServiceInterface(abc.ABC):
    def create(
        self, token: TokenCreateInputDto
    ) -> SuccessResponse:
        return self._create(token)

    def delete(self, token: TokenEntity):
        return self._delete(token)

    @abc.abstractmethod
    def _create(
        self, token: TokenCreateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete(self, token: TokenEntity):
        raise NotImplementedError
