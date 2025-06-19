from src.seaapi.domain.entities import StoreEntity
from src.seaapi.domain.ports.repositories.stores import (
    StoreRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class StoreSqlAlchemyRepository(
    StoreRepositoryInterface, DefaultAlchemyRepository
):
    def _find_by_identifier(
        self, identifier: str
    ) -> StoreEntity:
        return (
            self.session.query(StoreEntity)
            .filter_by(identifier=identifier)
            .first()
        )

    def _is_available(self, identifier: str) -> bool:
        store = (
            self.session.query(StoreEntity)
            .filter_by(identifier=identifier)
            .first()
        )
        return store is None
