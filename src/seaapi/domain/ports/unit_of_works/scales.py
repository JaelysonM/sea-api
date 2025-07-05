from src.seaapi.domain.ports.repositories.scales import (
    ScaleRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class ScaleUnitOfWorkInterface(DefaultUnitOfWorkInterface):
    scales: ScaleRepositoryInterface

    def __enter__(self) -> "ScaleUnitOfWorkInterface":
        return self
