from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.permissions import (
    PermissionServiceInterface,
)
from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.permissions import (
    PermissionPaginationData,
    PermissionPaginationParams,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    IsAuthenticated,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "",
    response_model=PermissionPaginationData,
    dependencies=[
        Depends(
            PermissionsDependency(
                And(
                    [
                        IsAuthenticated(),
                    ]
                )
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_all(
    params: PermissionPaginationParams = Depends(),
    permission_service: PermissionServiceInterface = Depends(
        Provide[Container.permission_service]
    ),
):

    return permission_service.get_all(params)
