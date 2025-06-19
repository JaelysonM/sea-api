from time import time
from datetime import datetime, date
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List

from src.siasdapi.domain.entities.base import (
    BaseEntity,
)
from src.siasdapi.domain.entities.store_config_entity import (
    StoreConfigEntity,
)
from src.siasdapi.domain.entities.store_schedule_entity import (
    StoreScheduleEntity,
)
from src.siasdapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.siasdapi.domain.ports.shared.exceptions import (
    CannotStorageFileException,
)
from src.siasdapi.domain.dtos.mics import UploadedFile
from src.siasdapi.domain.shared.arrays import find


@dataclass
class StoreEntity(BaseEntity):
    id: int
    name: str
    identifier: str
    address: str
    zipcode: str
    created_at: datetime
    updated_at: datetime

    store_config_id: Optional[int]

    store_config: Optional[StoreConfigEntity] = None
    schedules: List[StoreScheduleEntity] = field(
        default_factory=list
    )

    class Meta:
        verbose = "Loja"
        display_name = "Store"
        name = "store"
        search = ["name", "identifier"]
        filters = [
            "name",
            "identifier",
            "address",
            "zipcode",
            "created_at",
            "updated_at",
        ]
        composite_field = None
        active_field = None
        joins = []

    def get_date_schedule(
        self, date: date
    ) -> StoreScheduleEntity:

        week_day = date.weekday()
        week_day = (week_day + 1) % 7 + 1

        found = find(
            self.schedules,
            lambda x: x.day_of_week == week_day,
        )
        return found

    def upload_icon(
        self,
        storage_service: StorageServiceInterface,
        file: UploadedFile = None,
        scheduler=None,
    ):
        now = time()
        icon_path = (
            f"icons/stores/{self.id}/{now}_{file.filename}"
        )

        self.store_config.icon = icon_path

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
        store_dict = self.to_dict()

        store_dict["store_config"] = (
            self.store_config.to_beautiful_dict(
                storage_service=storage_service
            )
            if self.store_config
            else None
        )
        store_dict["schedules"] = [
            s.to_dict() for s in self.schedules
        ]
        return store_dict


def store_model_factory(
    name: str,
    identifier: str,
    address: str,
    zipcode: str,
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
    store_config_id: int = None,
    id: Optional[int] = None,
) -> StoreEntity:
    return StoreEntity(
        id=id,
        name=name,
        identifier=identifier,
        address=address,
        zipcode=zipcode,
        store_config_id=store_config_id,
        created_at=created_at,
        updated_at=updated_at,
    )
