from src.seaapi.adapters.db.models.base import (
    TablesRegistration,
)


class GeneralTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):
        pass

    def register(self):

        super().register()
