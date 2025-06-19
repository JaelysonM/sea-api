from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.users import (
    UserCreateInputDto,
    UserOutputDto,
    UserPaginationData,
    UserPaginationParams,
    UserUpdateInputDto,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    Or,
    IsAdministrator,
    IsAuthenticated,
    HasObjectCreatePermission,
    HasObjectReadPermission,
    HasObjectEditPermission,
    HasObjectDeletePermission,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=201,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectCreatePermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def create(
    user: UserCreateInputDto,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.create(user)


@router.get(
    "",
    response_model=UserPaginationData,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectReadPermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_all(
    params: UserPaginationParams = Depends(),
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):

    return user_service.get_all(params)


@router.get(
    "/{id}",
    response_model=UserOutputDto,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectReadPermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_user(
    id: int,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):

    return user_service.get_user(id)


@router.put(
    "/{id}",
    response_model=SuccessResponse,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectEditPermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def edit_user(
    id: int,
    user: UserUpdateInputDto,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):

    return user_service.update_user(id, user)


@router.delete(
    "/{id}",
    response_model=SuccessResponse,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectDeletePermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def delete_user(
    id: int,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.deactivate_user(id)


@router.post(
    "/{id}",
    response_model=SuccessResponse,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                        Or(
                            [
                                IsAdministrator(),
                                HasObjectCreatePermission(
                                    resource="user"
                                ),
                            ]
                        ),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def recover_user(
    id: int,
    user_service: UserServiceInterface = Depends(
        Provide[Container.user_service]
    ),
):
    return user_service.activate_user(id)
