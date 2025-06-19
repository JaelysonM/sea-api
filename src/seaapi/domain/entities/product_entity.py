from time import time
from dataclasses import dataclass
from typing import Optional

from src.seaapi.domain.entities.base import (
    BaseEntity,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    CannotStorageFileException,
)
from src.seaapi.domain.dtos.mics import UploadedFile


@dataclass
class ProductEntity(BaseEntity):
    id: int

    name: str
    description: Optional[str]

    photo: Optional[str]

    class Meta:
        verbose = "Produto da Loja"
        display_name = "Product"
        name = "product"
        search = ["name", "description"]
        filters = [
            "id",
            "name",
            "description",
        ]
        composite_field = None
        active_field = None
        joins = []

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

    def to_beautiful_dict(
        self, storage_service: StorageServiceInterface
    ):
        product_dict = self.to_dict()

        if self.photo is not None:
            product_dict["photo"] = storage_service.get(
                self.photo, expires=3000
            )

        return product_dict


def product_model_factory(
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
    )
