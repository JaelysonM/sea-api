from sqlalchemy.orm import Session
from src.seaapi.adapters.repositories.sqlalchemy.meals import (
    MealSqlAlchemyRepository,
)
from src.seaapi.domain.ports.unit_of_works.meals import (
    MealUnitOfWorkInterface,
)

from src.seaapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class MealSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, MealUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.meals = MealSqlAlchemyRepository(self.session)
        return super().__enter__()
