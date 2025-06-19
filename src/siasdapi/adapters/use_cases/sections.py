from typing import Union
from datetime import datetime
from src.siasdapi.domain.entities import (
    SectionEntity,
)
from src.siasdapi.domain.dtos.sections import (
    SectionCreateInputDto,
    SectionOutputDto,
    SectionUpdateInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
    PaginationOptions,
)
from src.siasdapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.siasdapi.domain.entities.section_entity import (
    section_model_factory,
)
from src.siasdapi.domain.entities.store_entity import (
    StoreEntity,
)

from src.siasdapi.domain.ports.unit_of_works.stores import (
    StoreUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.unit_of_works.sections import (
    SectionUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.use_cases.sections import (
    SectionServiceInterface,
)
from src.siasdapi.domain.ports.shared.exceptions import (
    NotAuthorizedException,
)


from src.siasdapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class SectionService(SectionServiceInterface):
    def __init__(
        self,
        uow: SectionUnitOfWorkInterface,
        store_uow: StoreUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.store_uow = store_uow
        self.storage_service = storage_service

    def _create(
        self, section: SectionCreateInputDto
    ) -> SuccessResponse:

        with self.uow:
            check_or_get_entity_if_exists(
                id_=section.store_id,
                entity_class=StoreEntity,
                active_field=None,
                repository="stores",
                uow=self.store_uow,
            )
            new_section = section_model_factory(
                title=section.title,
                description=section.description,
                store_id=section.store_id,
            )

            self.uow.sections.create(new_section)
            self.uow.commit()

            return SuccessResponse(
                message="Seção da loja criada com sucesso!",
                code="section_registered",
                status_code=201,
            )

    def _update_section(
        self, id_: int, section: SectionUpdateInputDto
    ) -> SuccessResponse:
        with self.uow:
            existing_section = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    repository=self.uow.sections,
                    entity_class=SectionEntity,
                )
            )

            special_fields = []

            for field, value in section.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_section, field, value)

            existing_section.updated_at = datetime.now()
            self.uow.commit()

            return SuccessResponse(
                message="Dados da seçåo da loja atualizadas com sucesso!",
                code="section_updated",
            )

    def _get_section(
        self, id_: int, entity: bool = False
    ) -> Union[SectionEntity, SectionOutputDto]:
        with self.uow:
            section_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.sections,
                entity_class=SectionEntity,
            )
            if entity:
                return section_
            return SectionOutputDto(
                **section_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            sections, results = self.uow.sections.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    SectionOutputDto(
                        **section.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for section in sections
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _delete_section(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()
        with self.uow:
            existing_section = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    repository=self.uow.sections,
                    entity_class=SectionEntity,
                )
            )

            self.uow.sections.delete(existing_section)

            self.uow.commit()

            return SuccessResponse(
                message="Seção da Loja removida com sucesso!",
                code="section_removed",
            )
