from src.siasdapi.domain.ports.repositories.sections import (
    SectionRepositoryInterface,
)

from src.siasdapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class SectionSqlAlchemyRepository(
    SectionRepositoryInterface, DefaultAlchemyRepository
):
    pass
