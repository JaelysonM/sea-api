from sqlalchemy.orm import Session
from src.seaapi.adapters.repositories.sqlalchemy.foods import (
    FoodSqlAlchemyRepository,
)
from src.seaapi.domain.ports.unit_of_works.foods import (
    FoodUnitOfWorkInterface,
)

from src.seaapi.adapters.unit_of_works.shared import (
    DefaultAlchemyUnitOfWork,
)


class FoodSqlAlchemyUnitOfWork(
    DefaultAlchemyUnitOfWork, FoodUnitOfWorkInterface
):
    def __enter__(self):
        self.session: Session = self.session_factory()
        self.foods = FoodSqlAlchemyRepository(self.session)
        return super().__enter__()
