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
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    SuccessWithIdResponse,
)
from src.seaapi.domain.entities.user_entity import (
    UserEntity,
)
from src.seaapi.domain.dtos.meals import (
    MealCreateInputDto,
    MealOutputDto,
    MealPaginationData,
    MealPaginationParams,
    FoodMeasurementCreateInputDto,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    Or,
    IsAdministrator,
    IsAuthenticated,
    HasObjectCreatePermission,
    HasObjectReadPermission,
)


router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/user",
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
    "/user/{id}",
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


@router.post(
    "/initialize",
    response_model=SuccessWithIdResponse,
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
                                    resource="meal"
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
def initialize_meal(
    meal: MealCreateInputDto,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):
    return meal_service.initialize_meal(meal)


@router.get(
    "",
    response_model=MealPaginationData,
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
                                    resource="meal"
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
    params: MealPaginationParams = Depends(),
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):

    return meal_service.get_all(params)


@router.get(
    "/{id}",
    response_model=MealOutputDto,
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
                                    resource="meal"
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
def get_meal(
    id: int,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):

    return meal_service.get_meal(id)


@router.post(
    "/{id}/measurements",
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
                                    resource="meal"
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
def add_meal_food_measurement(
    id: int,
    food_measurement: FoodMeasurementCreateInputDto,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):
    return meal_service.add_meal_food_measurement(
        id=id, food_measurement=food_measurement
    )


@router.post(
    "/{id}/finish",
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
                                    resource="meal"
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
def finish_meal(
    id: int,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):
    return meal_service.finish_meal(id)
