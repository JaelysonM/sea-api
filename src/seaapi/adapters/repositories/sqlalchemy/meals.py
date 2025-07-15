from typing import Optional
from src.seaapi.domain.ports.repositories.meals import (
    MealRepositoryInterface,
)

from src.seaapi.adapters.repositories.sqlalchemy.shared import (
    DefaultAlchemyRepository,
)
from src.seaapi.domain.entities.meal_entity import (
    MealEntity,
)


class MealSqlAlchemyRepository(
    MealRepositoryInterface, DefaultAlchemyRepository
):
    def _exists_non_finished_meal(
        self, user_id: int
    ) -> bool:
        return (
            self.session.query(MealEntity)
            .filter(
                MealEntity.user_id == user_id,
                MealEntity.finished.is_(False),
            )
            .count()
            > 0
        )

    def _find_current_meal(
        self, user_id: int
    ) -> Optional[MealEntity]:
        return (
            self.session.query(MealEntity)
            .filter(
                MealEntity.user_id == user_id,
                MealEntity.finished.is_(False),
            )
            .first()
        )

    def _find_meal_by_plate(
        self, plate_identifier: str
    ) -> Optional[MealEntity]:
        return (
            self.session.query(MealEntity)
            .filter(
                MealEntity.plate_identifier
                == plate_identifier,
                MealEntity.finished.is_(False),
            )
            .first()
        )
