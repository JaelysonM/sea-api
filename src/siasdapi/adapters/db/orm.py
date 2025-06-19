from sqlalchemy import MetaData
from sqlalchemy.orm import registry
from src.siasdapi.adapters.db.models import (
    UsersTables,
    StoresTables,
    GeneralTables,
    ProductsTables,
    TablesRegistration,
)
from src.siasdapi.config.containers import Container
from tests.fake_container import Container as FakeContainer

metadata = MetaData()
mapper_registry = registry(metadata=metadata)

general_tables = GeneralTables(mapper_registry)
users_tables = UsersTables(mapper_registry)
stores_tables = StoresTables(mapper_registry)
products_tables = ProductsTables(mapper_registry)


def start_mappers(register=True, from_test=False):
    container = FakeContainer if from_test else Container
    TablesRegistration.inject_container(
        [general_tables, users_tables], container
    )
    if register:
        general_tables.register()
        users_tables.register()
        stores_tables.register()
        products_tables.register()
    else:
        general_tables.create()
        users_tables.create()
        stores_tables.create()
        products_tables.create()


start_mappers(False)
