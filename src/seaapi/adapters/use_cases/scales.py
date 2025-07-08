from typing import Union
from src.seaapi.domain.entities import (
    ScaleEntity,
)
from src.seaapi.domain.dtos.scales import (
    ScaleCreateInputDto,
    ScaleOutputDto,
    ScaleUpdateInputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
    PaginationOptions,
)
from src.seaapi.domain.ports.services.storage import (
    StorageServiceInterface,
)
from src.seaapi.domain.entities.scale_entity import (
    scale_model_factory,
)
from src.seaapi.domain.ports.unit_of_works.scales import (
    ScaleUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.scales import (
    ScaleServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    NotAuthorizedException,
)


from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class ScaleService(ScaleServiceInterface):
    def __init__(
        self,
        uow: ScaleUnitOfWorkInterface,
        scale_uow: ScaleUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.scale_uow = scale_uow
        self.storage_service = storage_service

    def _create(
        self, scale: ScaleCreateInputDto
    ) -> SuccessResponse:

        with self.uow:
            new_scale = scale_model_factory(
                name=scale.name, serial=scale.serial
            )

            self.uow.scales.create(new_scale)

            self.uow.commit()

            return SuccessResponse(
                message="Balança criada com sucesso!",
                code="scale_registered",
                status_code=201,
            )

    def _update_scale(
        self,
        id_: int,
        scale: ScaleUpdateInputDto,
    ) -> SuccessResponse:
        with self.uow:
            existing_scale = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.scales,
                entity_class=ScaleEntity,
            )
            for field, value in scale.dict(
                exclude_unset=True
            ).items():
                setattr(existing_scale, field, value)
            self.uow.commit()

            return SuccessResponse(
                message="Dados da balança atualizados com sucesso!",
                code="scale_updated",
            )

    def _get_scale(
        self, id_: int, entity: bool = False
    ) -> Union[ScaleEntity, ScaleOutputDto]:
        with self.uow:
            scale_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.scales,
                entity_class=ScaleEntity,
            )
            if entity:
                return scale_
            return ScaleOutputDto(
                **scale_.to_dict(),
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            scales, results = self.uow.scales.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    ScaleOutputDto(**scale.to_dict())
                    for scale in scales
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _delete_scale(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()
        with self.uow:
            existing_scale = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.scales,
                entity_class=ScaleEntity,
            )

            self.uow.scales.delete(existing_scale)

            self.uow.commit()

            return SuccessResponse(
                message="Balança removida com sucesso!",
                code="scale_removed",
            )
