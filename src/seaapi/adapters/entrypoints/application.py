import sys
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
from src.seaapi.adapters.entrypoints.api.shared.rate_limit_middleware import (
    RateLimitMiddleware,
)
from starlette.middleware.authentication import (
    AuthenticationMiddleware,
)

logger = logging.getLogger(__name__)


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

    if settings.RATE_LIMITING_ENABLED:
        rate_limiter = app_.container.rate_limiter()

        custom_limits = {
            "POST:/v1/auth/login": {
                "max_requests": 5,
                "window_seconds": 300,
            },
            "POST:/v1/auth/refresh": {
                "max_requests": 10,
                "window_seconds": 300,
            },
            "POST:/v1/foods": {
                "max_requests": 20,
                "window_seconds": 3600,
            },
            "POST:/v1/foods/calculate-nutrition": {
                "max_requests": 5,
                "window_seconds": 120,
            },
            "PUT:/v1/foods": {
                "max_requests": 30,
                "window_seconds": 3600,
            },
            "DELETE:/v1/foods": {
                "max_requests": 10,
                "window_seconds": 3600,
            },
            "GET:/v1/foods": {
                "max_requests": 200,
                "window_seconds": 3600,
            },
            "GET:/v1/auth/me": {
                "max_requests": 100,
                "window_seconds": 3600,
            },
            "GET:/v1/auth/meals/current": {
                "max_requests": 100,
                "window_seconds": 60,
            },
        }
        exempt_endpoints = [
            "GET:/docs",
            "GET:/redoc",
            "GET:/openapi.json",
            "GET:/health",
        ]

        app_.add_middleware(
            RateLimitMiddleware,
            rate_limiter=rate_limiter,
            default_max_requests=settings.RATE_LIMITING_DEFAULT_MAX_REQUESTS,
            default_window_seconds=settings.RATE_LIMITING_DEFAULT_WINDOW_SECONDS,
            custom_limits=custom_limits,
            exempt_endpoints=exempt_endpoints,
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
