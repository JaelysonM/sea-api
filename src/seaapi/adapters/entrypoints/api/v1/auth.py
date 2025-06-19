from dependency_injector.wiring import (
    Provide,
    inject,
)

from fastapi import (
    APIRouter,
    Depends,
    Request,
    BackgroundTasks,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)
from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.tokens import Tokens
from src.seaapi.domain.dtos.users import (
    UserLoginInputDto,
    UserOutputDto,
    UserForgotPasswordInputDto,
    UserSoftUpdateInputDto,
    UserRecoverPasswordInputDto,
)
from src.seaapi.domain.dtos.mics import SuccessResponse
from src.seaapi.domain.dtos.tokens import RefreshTokenDto
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    IsAuthenticated,
)


router = APIRouter()
auth_scheme = HTTPBearer()


@router.post("/login", response_model=Tokens)
@inject
def login(
    user: UserLoginInputDto,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    tokens = user_service.authenticate_user(user)

    return tokens


@router.get(
    "/me",
    response_model=UserOutputDto,
    dependencies=[
        Depends(
            PermissionsDependency(
                IsAuthenticated(),
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def me(
    request: Request,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.get_authenticated_user(request.user)


@router.put(
    "/me",
    response_model=SuccessResponse,
    dependencies=[
        Depends(
            PermissionsDependency(
                IsAuthenticated(),
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def update_user(
    request: Request,
    user: UserSoftUpdateInputDto,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    user_id = request.user.id
    return user_service.update_user(id_=user_id, user=user)


@router.post("/refresh", response_model=Tokens)
@inject
def refresh_access_token(
    request: Request,
    token: RefreshTokenDto,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.refresh_access_token(
        token=token,
    )


@router.post(
    "/forgot-password", response_model=SuccessResponse
)
@inject
def request_password_change(
    dto: UserForgotPasswordInputDto,
    background_tasks: BackgroundTasks,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    user_service.forgot_password(dto, background_tasks)
    return SuccessResponse(
        message="Email de solicitação de senha enviado com sucesso.",
        code="forgot_password_requested",
    )


@router.put(
    "/change-password/{token}",
    response_model=SuccessResponse,
)
@inject
def password_recover(
    dto: UserRecoverPasswordInputDto,
    token: str,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.recover_password(
        dto=dto,
        token=token,
    )
