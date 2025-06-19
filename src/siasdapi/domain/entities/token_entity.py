from dataclasses import dataclass
from src.siasdapi.domain.entities.base import BaseEntity
from datetime import datetime


@dataclass
class TokenEntity(BaseEntity):

    id: int
    type: str
    token: str
    reference: int
    expiration: datetime
    created_at: datetime

    def __eq__(self, other):
        if not isinstance(other, TokenEntity):
            return False
        return (
            self.token == other.token
            and self.type == other.type
        )

    def __hash__(self):
        return hash(
            (
                self.id,
                self.type,
                self.token,
                self.reference,
                self.expiration,
                self.created_at,
            )
        )

    class Meta:
        masculine = True
        verbose = "Token"
        display_name = "Token"
        name = "token"
        composite_field = None
        active_field = None


def token_model_factory(
    type: str,
    token: str,
    reference: int,
    expiration: datetime,
    id: int = None,
    created_at: datetime = datetime.now(),
) -> TokenEntity:

    return TokenEntity(
        id=id,
        token=token,
        type=type,
        reference=reference,
        expiration=expiration,
        created_at=created_at,
    )
