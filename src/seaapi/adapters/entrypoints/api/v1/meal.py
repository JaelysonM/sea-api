from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.meals import (
    MealServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.meals import (
    MealOutputDto,
    MealFinishInputDto,
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
    "/measurements",
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
    food_measurement: FoodMeasurementCreateInputDto,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):
    return meal_service.add_meal_food_measurement(
        food_measurement=food_measurement
    )


@router.post(
    "/{plate_identifier}/finish",
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
    finish_meal: MealFinishInputDto,
    meal_service: MealServiceInterface = Depends(
        Provide[Container.meal_service]
    ),
):
    return meal_service.finish_meal(finish_meal)
