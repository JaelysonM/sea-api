from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    BackgroundTasks,
)
from fastapi.security import HTTPBearer
from src.seaapi.domain.ports.use_cases.stores import (
    StoreServiceInterface,
)

from src.seaapi.config.containers import Container
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.seaapi.domain.dtos.stores import (
    StoreCreateInputDto,
    StoreOutputDto,
    StorePaginationData,
    StorePaginationParams,
    StoreUpdateInputDto,
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
                                    resource="store"
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
    store: StoreCreateInputDto,
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):
    return store_service.create(store)


@router.get(
    "",
    response_model=StorePaginationData,
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
                                    resource="store"
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
    params: StorePaginationParams = Depends(),
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):

    return store_service.get_all(params)


@router.get("/{id}", response_model=StoreOutputDto)
@inject
def get_store(
    id: int,
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):

    return store_service.get_store(id)


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
                                    resource="store"
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
def edit_store(
    id: int,
    store: StoreUpdateInputDto,
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):

    return store_service.update_store(id, store)


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
                                    resource="store"
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
def delete_store(
    id: int,
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):
    return store_service.delete_store(id)


@router.post(
    "{id}/icon",
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
                                IsCustomer(),
                                HasObjectEditPermission(
                                    resource="store"
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
def update_store_icon(
    id: int,
    background_tasks: BackgroundTasks,
    file: UploadFile,
    store_service: StoreServiceInterface = Depends(
        Provide[Container.store_service]
    ),
):
    return store_service.update_store_icon(
        id_=id,
        file=convert_upload_file_to_domain(file),
        scheduler=background_tasks,
    )
