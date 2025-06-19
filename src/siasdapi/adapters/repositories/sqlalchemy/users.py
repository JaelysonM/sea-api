from src.siasdapi.domain.entities import UserEntity
from src.siasdapi.domain.ports.repositories.users import (
    UserRepositoryInterface,
)

from src.siasdapi.adapters.repositories.sqlalchemy.shared import (
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
