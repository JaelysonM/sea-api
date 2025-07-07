from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.foods import (
    FoodServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.foods import (
    FoodPaginationData,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    IsAuthenticated,
)


router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/menu",
    response_model=FoodPaginationData,
    dependencies=[
        Depends(
            PermissionsDependency(And([IsAuthenticated()]))
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_current_menu(
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):

    return food_service.get_current_menu()
