from src.seaapi.domain.ports.repositories.scales import (
    ScaleRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class ScaleSqlAlchemyRepository(
    ScaleRepositoryInterface, DefaultAlchemyRepository
):
    pass
