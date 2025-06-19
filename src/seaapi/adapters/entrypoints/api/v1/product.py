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
from src.seaapi.domain.ports.use_cases.products import (
    ProductServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.products import (
    ProductCreateInputDto,
    ProductOutputDto,
    ProductPaginationData,
    ProductPaginationParams,
    ProductUpdateInputDto,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
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
    product_service: ProductServiceInterface = Depends(
        Provide[Container.product_service]
    ),
):
    return product_service.create(
        ProductCreateInputDto(
            name=name,
            description=description,
            photo=convert_upload_file_to_domain(photo),
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