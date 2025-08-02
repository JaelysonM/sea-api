from typing import Optional
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    Form,
    UploadFile,
    File,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.foods import (
    FoodServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.foods import (
    FoodCreateInputDto,
    FoodOutputDto,
    FoodPaginationData,
    FoodPaginationParams,
    FoodUpdateInputDto,
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
from src.seaapi.adapters.entrypoints.api.shared.utils import (
    convert_upload_file_to_domain,
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
                                    resource="food"
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
    photo: Optional[UploadFile],
    name: str = Form(),
    description: Optional[str] = Form(None),
    calories: float = Form(),
    carbs: float = Form(),
    fat: float = Form(),
    protein: float = Form(),
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):
    return food_service.create(
        FoodCreateInputDto(
            name=name,
            description=description,
            calories=calories,
            carbs=carbs,
            fat=fat,
            protein=protein,
            photo=convert_upload_file_to_domain(photo),
        ),
    )


@router.get(
    "",
    response_model=FoodPaginationData,
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
                                    resource="food"
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
    params: FoodPaginationParams = Depends(),
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):

    return food_service.get_all(params)


@router.get("/{id}", response_model=FoodOutputDto)
@inject
def get_food(
    id: int,
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):

    return food_service.get_food(id)


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
                                    resource="food"
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
def edit_food(
    id: int,
    background_tasks: BackgroundTasks,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    calories: Optional[float] = Form(None),
    carbs: Optional[float] = Form(None),
    fat: Optional[float] = Form(None),
    protein: Optional[float] = Form(None),
    scale_id: Optional[int] = Form(None),
    photo: Optional[UploadFile] = File(None),
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):

    converted_file = (
        convert_upload_file_to_domain(photo)
        if photo is not None
        else None
    )

    raw = {
        "name": name,
        "description": description,
        "calories": calories,
        "carbs": carbs,
        "fat": fat,
        "protein": protein,
        "scale_id": scale_id,
        "photo": converted_file,
    }

    update_data = {
        k: v for k, v in raw.items() if v is not None
    }

    return food_service.update_food(
        id,
        FoodUpdateInputDto(**update_data),
        background_tasks,
    )


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
                                    resource="food"
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
def delete_food(
    id: int,
    food_service: FoodServiceInterface = Depends(
        Provide[Container.food_service]
    ),
):
    return food_service.delete_food(id)
