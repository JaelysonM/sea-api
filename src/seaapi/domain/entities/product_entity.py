from time import time
from dataclasses import dataclass, field
from typing import Optional, List

from src.seaapi.domain.entities.base import (
    BaseEntity,
)
from src.seaapi.domain.entities.product_child_entity import (
    ProductChildEntity,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    CannotStorageFileException,
)
from src.seaapi.domain.shared.arrays import find
from src.seaapi.domain.dtos.mics import UploadedFile


@dataclass
class ProductEntity(BaseEntity):
    id: int
    section_id: int

    name: str
    description: Optional[str]

    photo: Optional[str]
    children: List[ProductChildEntity] = field(
        default_factory=list
    )

    class Meta:
        verbose = "Produto da Loja"
        display_name = "Product"
        name = "product"
        search = ["name", "description"]
        filters = [
            "id",
            "section_id",
            "name",
            "description",
        ]
        composite_field = None
        active_field = None
        joins = []

    def get_child(self, id: int) -> ProductChildEntity:
        return find(self.children, lambda x: x.id == id)

    def upload_photo(
        self,
        storage_service: StorageServiceInterface,
        file: UploadedFile = None,
        scheduler=None,
        replace: bool = False,
    ):
        now = time()
        icon_path = f"photos/products/{self.id}/{now}_{file.filename}"

        if replace and self.photo is not None:
            storage_service.delete(self.photo)

        self.photo = icon_path

        try:
            storage_service.upload(
                path=icon_path,
                content=file.content,
            )
        except Exception as e:  # pragma: no cover
            print(e)
            raise CannotStorageFileException()

    @property
    def max_duration(self):
        if len(self.children) == 0:
            return 0

        return max(
            self.children, key=lambda x: x.duration
        ).duration

    @property
    def min_duration(self):
        if len(self.children) == 0:
            return 0

        return min(
            self.children, key=lambda x: x.duration
        ).duration

    @property
    def start_price(self):
        if len(self.children) == 0:
            return 0

        return min(
            self.children, key=lambda x: x.min_price
        ).min_price

    def to_beautiful_dict(
        self, storage_service: StorageServiceInterface
    ):
        product_dict = self.to_dict()

        product_dict["start_price"] = self.start_price
        product_dict["max_duration"] = self.max_duration
        product_dict["min_duration"] = self.min_duration

        if self.photo is not None:
            product_dict["photo"] = storage_service.get(
                self.photo, expires=3000
            )

        return product_dict


def product_model_factory(
    section_id: int,
    name: str,
    description: str = None,
    photo: str = None,
    id: Optional[int] = None,
) -> ProductEntity:
    return ProductEntity(
        id=id,
        name=name,
        description=description,
        photo=photo,
        section_id=section_id,
    )
