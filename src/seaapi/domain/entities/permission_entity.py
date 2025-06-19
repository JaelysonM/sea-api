from dataclasses import dataclass
from src.seaapi.domain.entities.base import BaseEntity


@dataclass
class PermissionEntity(BaseEntity):

    id: int
    name: str
    code: str

    def __eq__(self, other):
        if not isinstance(other, PermissionEntity):
            return False
        return self.code == other.code

    def __hash__(self):
        return hash((self.id, self.name, self.code))

    class Meta:
        masculine = False
        verbose = "Permissão"
        display_name = "Permission"
        name = "permission"
        search = ["name", "code"]
        filters = [
            "name",
            "code",
        ]
        composite_field = None
        active_field = None


def permission_model_factory(
    name: str,
    code: str,
    id: int = None,
) -> PermissionEntity:

    return PermissionEntity(id=id, name=name, code=code)
