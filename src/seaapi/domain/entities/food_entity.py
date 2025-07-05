from time import time
from dataclasses import dataclass, field
from typing import Optional

from src.seaapi.domain.entities.base import BaseEntity
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    CannotStorageFileException,
)
from src.seaapi.domain.entities.scale_entity import (
    ScaleEntity,
)
from src.seaapi.domain.dtos.mics import UploadedFile


@dataclass
class FoodEntity(BaseEntity):
    id: int
    name: str
    description: Optional[str]
    photo: Optional[str]
    protein: float
    carbs: float
    fat: float

    calories: float

    scale_id: Optional[int]

    scale: Optional[ScaleEntity] = field(
        default=None,
    )

    class Meta:
        verbose = "Comida"
        display_name = "Food"
        name = "food"
        search = ["name", "description"]
        filters = [
            "id",
            "name",
            "description",
            "protein",
            "carbs",
            "fat",
            "calories",
        ]
        composite_field = None
        active_field = None
        joins = []

    def set_scale(self, scale_id: int) -> bool:
        if scale_id == 0:
            self.scale_id = None
            return False
        else:
            self.scale_id = scale_id
        return True

    def upload_photo(
        self,
        storage_service: StorageServiceInterface,
        file: UploadedFile = None,
        replace: bool = False,
    ):
        now = time()
        icon_path = (
            f"photos/meals/{self.id}/{now}_{file.filename}"
        )

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
        meal_dict = self.to_dict()

        if self.photo is not None:
            meal_dict["photo"] = storage_service.get(
                self.photo, expires=3000
            )

        return meal_dict


def food_model_factory(
    name: str,
    protein: float,
    carbs: float,
    fat: float,
    calories: float,
    description: Optional[str] = None,
    photo: Optional[str] = None,
    scale_id: Optional[int] = None,
    id: Optional[int] = None,
) -> FoodEntity:
    return FoodEntity(
        id=id,
        name=name,
        description=description,
        photo=photo,
        protein=protein,
        carbs=carbs,
        fat=fat,
        calories=calories,
        scale_id=scale_id,
    )
