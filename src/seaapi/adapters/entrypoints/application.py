import sys
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command
import logging
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

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    logger.info("🚀 Iniciando aplicação...")

    # Startup - Inicializar EventBus/MQTT
    try:
        if settings.MESSAGING_ENABLED:
            event_bus = app.container.event_bus()
            await event_bus.start()
            logger.info(
                "✅ EventBus/MQTT conectado com sucesso"
            )
        else:
            logger.info("⚠️  Mensageria desabilitada")
    except Exception as e:
        logger.error(
            f"❌ Erro ao conectar EventBus/MQTT: {e}"
        )
        # Você pode escolher se quer falhar a aplicação ou continuar
        # raise  # Descomente se quiser que a app falhe se não conectar MQTT

    yield  # Aplicação roda aqui

    # Shutdown - Desconectar EventBus/MQTT
    try:
        if settings.MESSAGING_ENABLED:
            event_bus = app.container.event_bus()
            await event_bus.stop()
            logger.info("🔌 EventBus/MQTT desconectado")
    except Exception as e:
        logger.error(
            f"❌ Erro ao desconectar EventBus/MQTT: {e}"
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
        lifespan=lifespan,
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
