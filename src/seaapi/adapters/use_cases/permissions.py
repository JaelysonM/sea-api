from src.seaapi.domain.entities.permission_entity import (
    permission_model_factory,
)
from src.seaapi.domain.dtos.permissions import (
    PermissionCreateInputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationData,
    PaginationOptions,
    PaginationParams,
)

from src.seaapi.domain.ports.unit_of_works.permissions import (
    PermissionUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.permissions import (
    PermissionServiceInterface,
)


class PermissionService(PermissionServiceInterface):
    def __init__(self, uow: PermissionUnitOfWorkInterface):
        self.uow = uow

    def _create(
        self, permission: PermissionCreateInputDto
    ) -> SuccessResponse:
        with self.uow:
            permission_ = self.uow.permissions.find_by_code(
                permission.code
            )
            if permission_ is None:
                new_permission = permission_model_factory(
                    name=permission.name,
                    code=permission.code,
                )
                self.uow.permissions.create(new_permission)
            self.uow.commit()
            return SuccessResponse(
                message="Permissão cadastrada com sucesso!",
                code="group_registered",
                status_code=201,
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            (
                permissions,
                results,
            ) = self.uow.permissions.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size

            return PaginationData(
                data=permissions,
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )
