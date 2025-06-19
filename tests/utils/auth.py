from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    Depends,
)
from fastapi.encoders import jsonable_encoder
from fastapi.testclient import TestClient

from src.siasdapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)
from src.siasdapi.config.settings import settings
from tests.fake_container import Container


@inject
def user_authentication_headers(
    client: TestClient,
    email: str,
    password: str,
):
    data = {"email": email, "password": password}
    r = client.post(
        "v1/auth/login/", json=jsonable_encoder(data)
    )
    response = r.json()
    if r.status_code == 200:
        auth_token = response["access_token"]
        return {"Authorization": f"Bearer {auth_token}"}


@inject
def user_refresh_headers(
    client: TestClient,
    email: str,
    password: str,
):
    data = {"email": email, "password": password}
    r = client.post(
        "v1/auth/login/", json=jsonable_encoder(data)
    )
    response = r.json()

    if r.status_code == 200:
        refresh_token = response["refresh_token"]
        return refresh_token


@inject
def authentication_token_from_superuser(
    client: TestClient,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    return user_authentication_headers(
        client=client,
        email=settings.SUPERUSER_EMAIL,
        password=settings.SUPERUSER_PASSWORD,
    )


@inject
def refresh_token_from_superuser(
    client: TestClient,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    """
    Return a valid token for the user with given email.
    If the user doesn't exist it is created first.
    """
    return user_refresh_headers(
        client=client,
        email=settings.SUPERUSER_EMAIL,
        password=settings.SUPERUSER_PASSWORD,
    )
