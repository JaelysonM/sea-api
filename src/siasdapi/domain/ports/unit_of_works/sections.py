from src.siasdapi.domain.ports.repositories.sections import (
    SectionRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class SectionUnitOfWorkInterface(
    DefaultUnitOfWorkInterface
):
    sections: SectionRepositoryInterface

    def __enter__(self) -> "SectionUnitOfWorkInterface":
        return self
