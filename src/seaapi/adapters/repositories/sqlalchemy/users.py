from src.seaapi.domain.entities import UserEntity
from src.seaapi.domain.ports.repositories.users import (
    UserRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class UserSqlAlchemyRepository(
    UserRepositoryInterface, DefaultAlchemyRepository
):
    def _find_by_email(self, email: str) -> UserEntity:
        return (
            self.session.query(UserEntity)
            .filter_by(email=email)
            .first()
        )

    def _is_available(self, email: str) -> bool:
        user = (
            self.session.query(UserEntity)
            .filter_by(email=email)
            .first()
        )
        return user is None
