from src.seaapi.domain.ports.repositories.sections import (
    SectionRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class SectionSqlAlchemyRepository(
    SectionRepositoryInterface, DefaultAlchemyRepository
):
    pass
