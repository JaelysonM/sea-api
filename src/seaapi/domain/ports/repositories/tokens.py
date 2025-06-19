from abc import abstractmethod
from src.seaapi.domain.entities import TokenEntity
from src.seaapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)


class TokenRepositoryInterface(
    BaseWriteableRepositoryInterface
):

    entity = TokenEntity

    def find_by_token_and_type(
        self, token: str, type: str
    ) -> TokenEntity:
        token = self._find_by_token_and_type(
            token=token, type=type
        )
        return token

    def find_by_email_and_type(
        self, email: str, type: str
    ) -> TokenEntity:
        token = self._find_by_email_and_type(
            email=email, type=type
        )
        return token

    @abstractmethod
    def _find_by_email_and_type(
        self, email: str, type: str
    ) -> TokenEntity:
        raise NotImplementedError

    @abstractmethod
    def _find_by_token_and_type(
        self, token: str, type: str
    ) -> TokenEntity:
        raise NotImplementedError
