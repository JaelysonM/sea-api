from typing import Any, Callable
from sqlalchemy.orm import Session

from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)


class DefaultAlchemyUnitOfWork(DefaultUnitOfWorkInterface):
    session: Session

    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def expunge(self):
        self.session.expunge_all()
