from src.seaapi.domain.entities.token_entity import (
    token_model_factory,
)
from src.seaapi.domain.dtos.tokens import (
    TokenCreateInputDto,
    TokenOutputDto,
)
from src.seaapi.domain.ports.unit_of_works.tokens import (
    TokenUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.tokens import (
    TokenServiceInterface,
)
from src.seaapi.domain.entities import TokenEntity


class TokenService(TokenServiceInterface):
    def __init__(self, uow: TokenUnitOfWorkInterface):
        self.uow = uow

    def _create(
        self, token: TokenCreateInputDto
    ) -> TokenOutputDto:
        with self.uow:
            new_token = token_model_factory(
                token=token.token,
                type=token.type,
                expiration=token.expiration,
                reference=token.reference,
            )
            self.uow.tokens.create(new_token)
            self.uow.commit()
            return TokenOutputDto.from_orm(new_token)

    def _delete(self, token: TokenEntity):
        with self.uow:
            self.uow.tokens.delete(token)
            self.uow.commit()
