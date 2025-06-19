from typing import Optional
from dataclasses import dataclass, asdict
from src.siasdapi.domain.ports.services.storage import (
    StorageServiceInterface,
)


@dataclass
class StoreConfigEntity:
    id: int
    supports_dynamic_pricing: bool
    icon: Optional[str]

    class Meta:
        verbose = "Configuração da Loja"
        display_name = "StoreConfig"
        name = "store_config"
        filters = ["supports_dynamic_pricing", "icon"]
        joins = []

    def to_beautiful_dict(
        self, storage_service: StorageServiceInterface
    ):
        config_dict = self.to_dict()

        if self.icon is not None:
            config_dict["icon"] = storage_service.get(
                self.icon, expires=3000
            )
        return config_dict

    def to_dict(self):
        return asdict(self)


def store_config_model_factory(
    supports_dynamic_pricing: bool,
    icon: Optional[str] = None,
    id: int = None,
) -> StoreConfigEntity:
    return StoreConfigEntity(
        id=id,
        icon=icon,
        supports_dynamic_pricing=supports_dynamic_pricing,
    )
