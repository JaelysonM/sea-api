from typing import Optional
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.adapters.entrypoints.api.shared.middlewares import (
    get_user,
)
from src.seaapi.domain.ports.use_cases.meals import (
    MealServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.entities.user_entity import (
    UserEntity,
)
from src.seaapi.domain.dtos.meals import (
    MealOutputDto,
    MealPaginationData,
    MealPaginationParams,
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
    response_model=MealPaginationData,
    dependencies=[
        Depends(
            PermissionsDependency(And([IsAuthenticated()]))
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_user_meals(
    params: MealPaginationParams = Depends(),
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
    user: UserEntity = Depends(get_user),
):
    user_id = user.id
    return meal_service.get_user_meals(
        user_id=user_id, params=params
    )


@router.get(
    "/current",
    response_model=Optional[MealOutputDto],
    dependencies=[
        Depends(
            PermissionsDependency(And([IsAuthenticated()]))
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_current_meal(
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
    user: UserEntity = Depends(get_user),
):
    user_id = user.id
    return meal_service.get_current_meal(user_id=user_id)


@router.get(
    "/{id}",
    response_model=MealOutputDto,
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
def get_user_meal(
    id: int,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
    user: UserEntity = Depends(get_user),
):
    user_id = user.id if user else None
    return meal_service.get_user_meal(
        user_id=user_id, id_=id
    )
