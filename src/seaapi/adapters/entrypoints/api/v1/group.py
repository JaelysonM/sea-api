from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.groups import (
    GroupServiceInterface,
)
from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.groups import (
    GroupCreateInputDto,
    GroupUpdateInputDto,
    GroupPaginationData,
    GroupPaginationParams,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    Or,
    IsAuthenticated,
    IsAdministrator,
    HasObjectReadPermission,
    HasObjectCreatePermission,
    HasObjectEditPermission,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "",
    response_model=GroupPaginationData,
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
                                    resource="group"
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
    params: GroupPaginationParams = Depends(),
    group_service: GroupServiceInterface = Depends(
        Provide[Container.group_service]
    ),
):

    return group_service.get_all(params)


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
                                    resource="group"
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
    group: GroupCreateInputDto,
    group_service: GroupServiceInterface = Depends(
        Provide[Container.group_service]
    ),
):
    return group_service.create(group)


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
                                    resource="group"
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
def edit_group(
    id: int,
    group: GroupUpdateInputDto,
    group_service: GroupServiceInterface = Depends(
        Provide[Container.group_service]
    ),
):
    return group_service.update_group(id_=id, group=group)
