import pytest
import os
from typing import Any, Generator
from datetime import datetime, timedelta, date
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.seaapi.adapters.db.orm import metadata
from src.seaapi.adapters.entrypoints.application import (
    app as original_app,
)
from src.seaapi.config.settings import settings
from tests.fake_container import Container
from tests.utils.auth import (
    authentication_token_from_superuser,
    refresh_token_from_superuser,
)
from tests.utils.video import (
    create_fake_video_and_temporary_file,
)

engine = create_engine(
    settings.TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
)
# Use connect_args parameter only with sqlite
SessionTesting = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

migrations_applied = False


def delete_database_file():
    if settings.TEST_DATABASE_URL.startswith("sqlite:///"):
        db_file = settings.TEST_DATABASE_URL[
            len("sqlite:///") :
        ]

        if os.path.isfile(db_file):
            os.remove(db_file)


@pytest.fixture(scope="package")
def get_fake_container():
    return Container()


@pytest.fixture(scope="package")
def app():
    metadata.create_all(engine)
    yield original_app
    metadata.drop_all(engine)
    delete_database_file()


@pytest.fixture
def get_user_model_dict():
    now = datetime.now()
    return {
        "id": 1,
        "first_name": "3D-Fans",
        "last_name": "QA",
        "email": "testing@3dfans.com.br",
        "password": "password",
        "is_active": True,
        "is_super_user": False,
        "cliente_id": None,
        "created_at": now,
        "updated_at": now,
        "deleted_at": None,
        "last_login": now,
    }


@pytest.fixture
def get_create_user_dict():
    return {
        "first_name": "Joseph",
        "last_name": "Tester",
        "email": "joseph@tester.com",
        "password": "D4ntForgotPass#",
    }


@pytest.fixture(scope="module")
def superuser_refresh_token(
    client: TestClient,
    get_fake_container,
    app,
):
    with app.container.user_service.override(
        get_fake_container.user_service
    ):
        return refresh_token_from_superuser(client=client)


@pytest.fixture(scope="module")
def superuser_tokens(
    client: TestClient,
    get_fake_container,
    app,
):
    with app.container.user_service.override(
        get_fake_container.user_service
    ):
        return authentication_token_from_superuser(
            client=client
        )


@pytest.fixture(scope="module")
def client(
    app: FastAPI,
) -> Generator[TestClient, Any, None]:
    os.environ["USING_TESTCLIENT"] = "true"
    """
    Create a new FastAPI TestClient that uses the `db_session` fixture to override
    the `get_db` dependency that is injected into routes.
    """

    with TestClient(app) as client:
        yield client
