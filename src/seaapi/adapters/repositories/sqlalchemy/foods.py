from typing import Optional
from src.seaapi.domain.ports.repositories.foods import (
    FoodRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)

from src.seaapi.domain.entities import (
    FoodEntity,
    ScaleEntity,
)


class FoodSqlAlchemyRepository(
    FoodRepositoryInterface, DefaultAlchemyRepository
):
    def _find_food_by_scale_serial(
        self, scale_serial: str
    ) -> Optional[FoodEntity]:
        query = (
            self.session.query(FoodEntity)
            .join(
                ScaleEntity,
                FoodEntity.scale_id == ScaleEntity.id,
            )
            .filter(ScaleEntity.serial == scale_serial)
        )
        return query.first() if query.count() > 0 else None
