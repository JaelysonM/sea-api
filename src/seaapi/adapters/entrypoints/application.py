import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
from src.seaapi.adapters.db.orm import (
    start_mappers,
)
from src.seaapi.adapters.entrypoints.api.base import (
    api_router,
)
from src.seaapi.config import (
    settings,
)
from src.seaapi.config.containers import (
    Container,
)
from src.seaapi.adapters.entrypoints.api.handlers import (
    register_handlers,
)
from src.seaapi.adapters.entrypoints.api.shared.middlewares import (
    BearerTokenAuthBackend,
)
from starlette.middleware.authentication import (
    AuthenticationMiddleware,
)


def include_router(app_):
    app_.include_router(api_router)


def register_middleware(app_):
    app_.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app_.add_middleware(
        AuthenticationMiddleware,
        backend=BearerTokenAuthBackend(),
    )


def setup_migrations():
    alembic_cfg = Config(
        "src/seaapi/adapters/db/alembic.ini"
    )
    alembic_cfg.set_main_option(
        "sqlalchemy.url", settings.TEST_DATABASE_URL
    )
    alembic_cfg.set_main_option("ci", "true")
    target_revision = "head"
    command.upgrade(alembic_cfg, target_revision)


def start_application():
    container = Container()
    app_ = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
    )
    app_.container = container
    include_router(app_)
    register_handlers(app_)
    register_middleware(app_)
    from_test = "pytest" in sys.argv[0]
    if from_test:
        setup_migrations()
    start_mappers(from_test=from_test)

    return app_


app = start_application()
