from typing import Optional
from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    Form,
    BackgroundTasks,
    UploadFile,
)
from fastapi.security import HTTPBearer
from src.siasdapi.domain.ports.use_cases.products import (
    ProductServiceInterface,
)

from src.siasdapi.config.containers import Container
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.siasdapi.domain.dtos.products import (
    ProductCreateInputDto,
    ProductOutputDto,
    ProductPaginationData,
    ProductPaginationParams,
    ProductUpdateInputDto,
    ProductChildCreateInputDto,
    ProductScheduleInputDto,
    ProductScheduleOutputDto,
)
from src.siasdapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    Or,
    IsAdministrator,
    IsAuthenticated,
    IsCustomer,
    HasObjectCreatePermission,
    HasObjectReadPermission,
    HasObjectEditPermission,
    HasObjectDeletePermission,
)
from src.siasdapi.adapters.entrypoints.api.shared.utils import (
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
                                    resource="product"
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
    background_tasks: BackgroundTasks,
    photo: Optional[UploadFile],
    name: str = Form(),
    description: Optional[str] = Form(None),
    store_id: int = Form(),
    section_id: int = Form(),
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):
    return product_service.create(
        ProductCreateInputDto(
            name=name,
            section_id=section_id,
            description=description,
            photo=convert_upload_file_to_domain(photo),
            store_id=store_id,
        ),
        scheduler=background_tasks,
    )


@router.get(
    "",
    response_model=ProductPaginationData,
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
                                    resource="product"
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
    params: ProductPaginationParams = Depends(),
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):

    return product_service.get_all(params)


@router.get("/{id}", response_model=ProductOutputDto)
@inject
def get_product(
    id: int,
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):

    return product_service.get_product(id)


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
                                IsCustomer(),
                                HasObjectEditPermission(
                                    resource="product"
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
def edit_product(
    id: int,
    background_tasks: BackgroundTasks,
    name: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    section_id: Optional[int] = Form(None),
    photo: Optional[UploadFile] = Depends(),
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):

    return product_service.update_product(
        id,
        ProductUpdateInputDto(
            name=name,
            description=description,
            photo=convert_upload_file_to_domain(photo),
            section_id=section_id,
        ),
        scheduler=background_tasks,
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
                                IsCustomer(),
                                HasObjectDeletePermission(
                                    resource="product"
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
def delete_product(
    id: int,
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):
    return product_service.delete_product(id)


@router.post(
    "{id}/child",
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
                                    resource="product"
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
def create_child(
    id: int,
    product_child: ProductChildCreateInputDto,
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):
    return product_service.create_child(
        id=id, product_child=product_child
    )


@router.get(
    "/{id}/schedule",
    response_model=ProductScheduleOutputDto,
    status_code=200,
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
def get_product_schedule(
    id: int,
    product_schedule: ProductScheduleInputDto = Depends(),
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):
    return product_service.get_product_schedule(
        id_=id, product_schedule=product_schedule
    )
