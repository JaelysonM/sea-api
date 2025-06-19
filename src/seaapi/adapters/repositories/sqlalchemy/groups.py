from src.seaapi.domain.ports.repositories.groups import (
    GroupRepositoryInterface,
)
from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class GroupSqlAlchemyRepository(
    GroupRepositoryInterface, DefaultAlchemyRepository
):
    pass
