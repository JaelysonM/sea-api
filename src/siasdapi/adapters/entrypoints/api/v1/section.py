from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
)
from fastapi.security import HTTPBearer
from src.siasdapi.domain.ports.use_cases.sections import (
    SectionServiceInterface,
)

from src.siasdapi.config.containers import Container
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
)
from src.siasdapi.domain.dtos.sections import (
    SectionCreateInputDto,
    SectionOutputDto,
    SectionPaginationData,
    SectionPaginationParams,
    SectionUpdateInputDto,
)
from src.siasdapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    Or,
    IsAdministrator,
    IsAuthenticated,
    IsCustomer,
    HasObjectCreatePermission,
    HasObjectEditPermission,
    HasObjectDeletePermission,
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
                                    resource="section"
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
    section: SectionCreateInputDto,
    section_service: SectionServiceInterface = Depends(
        Provide[Container.section_service]
    ),
):
    return section_service.create(section)


@router.get("", response_model=SectionPaginationData)
@inject
def get_all(
    params: SectionPaginationParams = Depends(),
    section_service: SectionServiceInterface = Depends(
        Provide[Container.section_service]
    ),
):

    return section_service.get_all(params)


@router.get(
    "/{id}",
    response_model=SectionOutputDto,
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
def get_section(
    id: int,
    section_service: SectionServiceInterface = Depends(
        Provide[Container.section_service]
    ),
):

    return section_service.get_section(id)


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
                                    resource="section"
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
def edit_section(
    id: int,
    section: SectionUpdateInputDto,
    section_service: SectionServiceInterface = Depends(
        Provide[Container.section_service]
    ),
):

    return section_service.update_section(id, section)


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
                                    resource="section"
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
def delete_section(
    id: int,
    section_service: SectionServiceInterface = Depends(
        Provide[Container.section_service]
    ),
):
    return section_service.delete_section(id)
