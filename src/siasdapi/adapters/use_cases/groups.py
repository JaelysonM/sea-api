from src.siasdapi.domain.entities import (
    PermissionEntity,
    GroupEntity,
)
from src.siasdapi.domain.entities.group_entity import (
    group_model_factory,
)
from src.siasdapi.domain.dtos.groups import (
    GroupCreateInputDto,
    GroupUpdateInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationData,
    PaginationOptions,
    PaginationParams,
)

from src.siasdapi.domain.ports.unit_of_works.groups import (
    GroupUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.unit_of_works.permissions import (
    PermissionUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.use_cases.groups import (
    GroupServiceInterface,
)
from src.siasdapi.domain.shared.utils import (
    update_entity_list,
)
from src.siasdapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class GroupService(GroupServiceInterface):
    def __init__(
        self,
        uow: GroupUnitOfWorkInterface,
        permission_uow: PermissionUnitOfWorkInterface,
    ):
        self.uow = uow
        self.permission_uow = permission_uow

    def _create(
        self, group: GroupCreateInputDto
    ) -> SuccessResponse:
        with self.uow:
            new_group = group_model_factory(
                name=group.name,
                default=group.default,
            )
            update_entity_list(
                ids=group.permissions,
                target_entity=new_group,
                target_field="permissions",
                entity_class=PermissionEntity,
                repository="permissions",
                uow=self.permission_uow,
            )

            self.uow.groups.create(new_group)
            self.uow.commit()
            return SuccessResponse(
                message="Cargo cadastrado com sucesso!",
                code="group_registered",
                status_code=201,
            )

    def _update_group(
        self, id_: int, group: GroupUpdateInputDto
    ) -> SuccessResponse:
        with self.uow:
            existing_group = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.groups,
                entity_class=GroupEntity,
            )

            special_fields = [
                "permissions",
            ]

            for field, value in group.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_group, field, value)

            update_entity_list(
                ids=group.permissions,
                target_entity=existing_group,
                target_field="permissions",
                entity_class=PermissionEntity,
                repository="permissions",
                uow=self.permission_uow,
            )
            self.uow.commit()

            return SuccessResponse(
                message="Dados do grupo atualizados com sucesso!",
                code="group_updated",
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size

            groups, results = self.uow.groups.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size

            return PaginationData(
                data=groups,
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )
