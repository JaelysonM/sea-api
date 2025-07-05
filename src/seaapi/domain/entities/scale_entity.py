from dataclasses import dataclass
from typing import Optional

from src.seaapi.domain.entities.base import BaseEntity


@dataclass
class ScaleEntity(BaseEntity):
    id: int
    name: str
    serial: str

    class Meta:
        verbose = "Balança"
        display_name = "Scale"
        name = "Scale"
        search = ["name", "serial"]
        filters = ["id", "name", "serial"]
        composite_field = None
        active_field = None
        joins = []


def scale_model_factory(
    name: str,
    serial: str,
    id: Optional[int] = None,
) -> ScaleEntity:
    return ScaleEntity(id=id, name=name, serial=serial)
