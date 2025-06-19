from dataclasses import dataclass, field
from typing import Optional, List

from src.siasdapi.domain.entities.base import (
    BaseEntity,
)
from src.siasdapi.domain.entities.product_entity import (
    ProductEntity,
)
from src.siasdapi.domain.entities.store_entity import (
    StoreEntity,
)
from src.siasdapi.domain.ports.services.storage import (
    StorageServiceInterface,
)


@dataclass
class SectionEntity(BaseEntity):
    id: int
    store_id: int
    title: str
    description: Optional[str]

    store: Optional[StoreEntity] = field(default=None)

    products: List[ProductEntity] = field(
        default_factory=list
    )

    class Meta:
        verbose = "Seção da Loja"
        display_name = "Section"
        name = "section"
        search = ["title", "description"]
        filters = ["store_id", "title", "description"]
        composite_field = None
        active_field = None
        joins = []

    def to_beautiful_dict(
        self, storage_service: StorageServiceInterface
    ):
        section_dict = self.to_dict()

        section_dict["products"] = [
            product.to_beautiful_dict(storage_service)
            for product in self.products
        ]

        return section_dict


def section_model_factory(
    store_id: int,
    title: str,
    description: str = None,
    id: Optional[int] = None,
) -> SectionEntity:
    return SectionEntity(
        id=id,
        title=title,
        description=description,
        store_id=store_id,
    )
