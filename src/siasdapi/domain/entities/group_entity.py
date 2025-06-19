from dataclasses import dataclass, field
from typing import List, Optional
from src.siasdapi.domain.entities.permission_entity import (
    PermissionEntity,
)
from src.siasdapi.domain.entities.base import BaseEntity


@dataclass
class GroupEntity(BaseEntity):

    id: int
    name: str
    default: bool

    permissions: Optional[List[PermissionEntity]] = field(
        default_factory=list
    )

    class Meta:
        masculine = True
        verbose = "Grupo"
        display_name = "Group"
        name = "group"
        search = ["name"]
        filters = [
            "name",
            "default",
        ]
        composite_field = None
        active_field = None

    def __hash__(self):
        return hash((self.id, self.name, self.default))

    def __eq__(self, other):
        if not isinstance(other, GroupEntity):
            return False
        return self.id == other.id


def group_model_factory(
    name: str,
    default: bool,
    id: int = None,
) -> GroupEntity:

    return GroupEntity(id=id, name=name, default=default)
