from datetime import datetime
from src.seaapi.domain.entities import (
    TokenEntity,
    UserEntity,
)
from src.seaapi.domain.ports.repositories.tokens import (
    TokenRepositoryInterface,
)
from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class TokenSqlAlchemyRepository(
    TokenRepositoryInterface, DefaultAlchemyRepository
):
    def _find_by_email_and_type(
        self, email: str, type: str
    ) -> TokenEntity:
        return (
            self.session.query(TokenEntity)
            .join(UserEntity)
            .filter(
                UserEntity.email == email,
                TokenEntity.type == type,
                TokenEntity.expiration > datetime.now(),
            )
            .first()
        )

    def _find_by_token_and_type(
        self, token: str, type: str
    ) -> TokenEntity:
        return (
            self.session.query(TokenEntity)
            .filter(
                TokenEntity.token == token,
                TokenEntity.type == type,
                TokenEntity.expiration > datetime.now(),
            )
            .first()
        )
