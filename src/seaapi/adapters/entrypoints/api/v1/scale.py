from typing import Optional
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    Form,
    UploadFile,
    File,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.scales import (
    ScaleServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.scales import (
    ScaleCreateInputDto,
    ScaleOutputDto,
    ScalePaginationData,
    ScalePaginationParams,
    ScaleUpdateInputDto,
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
                                    resource="scale"
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
    scale_service: ScaleServiceInterface = Depends(
        Provide[Container.scale_service]
    ),
):
    return scale_service.create(
        ScaleCreateInputDto(
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
    response_model=ScalePaginationData,
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
                                    resource="scale"
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
    params: ScalePaginationParams = Depends(),
    scale_service: ScaleServiceInterface = Depends(
        Provide[Container.scale_service]
    ),
):

    return scale_service.get_all(params)


@router.get("/{id}", response_model=ScaleOutputDto)
@inject
def get_scale(
    id: int,
    scale_service: ScaleServiceInterface = Depends(
        Provide[Container.scale_service]
    ),
):

    return scale_service.get_scale(id)


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
                                    resource="scale"
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
def edit_scale(
    id: int,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    calories: Optional[float] = Form(None),
    carbs: Optional[float] = Form(None),
    fat: Optional[float] = Form(None),
    protein: Optional[float] = Form(None),
    scale_id: Optional[int] = Form(None),
    photo: Optional[UploadFile] = File(None),
    scale_service: ScaleServiceInterface = Depends(
        Provide[Container.scale_service]
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

    return scale_service.update_scale(
        id,
        ScaleUpdateInputDto(**update_data),
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
                                    resource="scale"
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
def delete_scale(
    id: int,
    scale_service: ScaleServiceInterface = Depends(
        Provide[Container.scale_service]
    ),
):
    return scale_service.delete_scale(id)
