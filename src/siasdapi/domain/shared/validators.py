from pydantic import BaseModel, validator
from typing import Tuple
from src.siasdapi.domain.ports.shared.exceptions import (
    EntityNotFoundOrDeletedException,
)
from src.siasdapi.domain.entities.base import BaseEntity
from src.siasdapi.domain.ports.repositories import (
    BaseRepositoryInterface,
)
from src.siasdapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)
from src.siasdapi.config.settings import Settings


class VideoFile(BaseModel):
    file: str

    @validator("file")
    def validate_file_extensions(cls, value):
        allowed_video_extensions = (
            Settings.VIDEO_ACCEPTED_FORMATS
        )
        if not any(
            value.lower().endswith(ext)
            for ext in allowed_video_extensions
        ):
            allowed_formats = ", ".join(
                ext[1:] for ext in allowed_video_extensions
            )
            raise ValueError(
                f"Formato de vídeo inválido do arquivo {value}."
                + f" Formatos aceitos: {allowed_formats}"
            )
        return value


def check_or_get_entity_if_exists(
    id_: int,
    repository: Tuple[str, BaseRepositoryInterface],
    entity_class: BaseEntity,
    uow: DefaultUnitOfWorkInterface = None,
    cross_id: int = None,
    active_field: str = "ativo",
) -> BaseEntity:
    def run():
        composite_field = None
        if entity_class is not None and hasattr(
            entity_class.Meta, "composite_field"
        ):
            composite_field = (
                entity_class.Meta.composite_field
            )
        final_active_field = active_field
        if (
            entity_class is not None
            and hasattr(entity_class.Meta, "active_field")
            and final_active_field is not None
        ):
            final_active_field = (
                entity_class.Meta.active_field
            )

        if uow is not None:
            repository_instance = getattr(uow, repository)
        else:
            repository_instance = repository
        if (
            cross_id is not None
            and composite_field is not None
        ):
            existing_entity = (
                repository_instance.find_by_id(
                    id_, **{composite_field: cross_id}
                )
            )
        else:
            existing_entity = (
                repository_instance.find_by_id(id_)
            )
        if not existing_entity or (
            final_active_field is not None
            and not getattr(
                existing_entity, final_active_field
            )
        ):
            raise EntityNotFoundOrDeletedException(
                entity=entity_class,
                id=id_,
                deleted=existing_entity is not None,
            )
        return existing_entity

    if uow is not None:
        with uow:
            return run()
    else:
        return run()
