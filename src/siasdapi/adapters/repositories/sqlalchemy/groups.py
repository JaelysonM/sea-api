from src.siasdapi.domain.ports.repositories.groups import (
    GroupRepositoryInterface,
)
from src.siasdapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class GroupSqlAlchemyRepository(
    GroupRepositoryInterface, DefaultAlchemyRepository
):
    pass
