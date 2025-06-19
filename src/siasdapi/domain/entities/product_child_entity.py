from dataclasses import dataclass
from typing import Optional

from src.siasdapi.domain.entities.base import (
    BaseEntity,
)
from src.siasdapi.domain.entities.store_entity import (
    StoreEntity,
)


@dataclass
class ProductChildEntity(BaseEntity):
    id: int
    product_id: int
    name: str
    description: Optional[str]

    min_price: float
    max_price: float

    duration: int

    class Meta:
        verbose = "Variante do Produto"
        display_name = "ProductChild"
        name = "product_child"
        search = ["name", "description"]
        filters = [
            "id",
            "product_id",
            "name",
            "description",
            "max_price",
            "min_price",
        ]
        composite_field = None
        active_field = None
        joins = []


def product_child_model_factory(
    product_id: int,
    name: str,
    min_price: float,
    max_price: float,
    duration: int,
    description: str = None,
    id: Optional[int] = None,
) -> StoreEntity:
    return ProductChildEntity(
        id=id,
        name=name,
        description=description,
        min_price=min_price,
        max_price=max_price,
        duration=duration,
        product_id=product_id,
    )
