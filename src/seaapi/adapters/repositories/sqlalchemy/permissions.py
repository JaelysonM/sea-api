from src.seaapi.domain.entities import (
    PermissionEntity,
)
from src.seaapi.domain.ports.repositories.permissions import (
    PermissionRepositoryInterface,
)
from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)


class PermissionSqlAlchemyRepository(
    PermissionRepositoryInterface, DefaultAlchemyRepository
):
    def _delete(self, permission):  # pragma: no cover
        raise Exception("Permission deletion not allowed")

    def _find_by_code(self, code: str) -> PermissionEntity:
        return (
            self.session.query(PermissionEntity)
            .filter_by(code=code)
            .first()
        )
