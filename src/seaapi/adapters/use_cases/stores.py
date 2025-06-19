from typing import Union, List
from datetime import datetime
from src.seaapi.domain.entities import (
    StoreEntity,
)
from src.seaapi.domain.dtos.stores import (
    StoreCreateInputDto,
    StoreOutputDto,
    StoreUpdateInputDto,
    StoreScheduleCreateInputDto,
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
from src.seaapi.domain.entities.store_entity import (
    store_model_factory,
)
from src.seaapi.domain.entities.store_config_entity import (
    store_config_model_factory,
)
from src.seaapi.domain.entities.store_schedule_entity import (
    store_schedule_model_factory,
)
from src.seaapi.domain.dtos.mics import UploadedFile

from src.seaapi.domain.ports.unit_of_works.stores import (
    StoreUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.stores import (
    StoreServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    IdentifierExistsException,
    NotAuthorizedException,
)


from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class StoreService(StoreServiceInterface):
    def __init__(
        self,
        uow: StoreUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.storage_service = storage_service

    def _create_or_update_store_schedule(
        self,
        schedules: List[StoreScheduleCreateInputDto],
        store: StoreEntity = None,
    ):
        store_id = store.id

        existing_entities = store.schedules

        existing_entities_set = {
            (
                getattr(entry, "day_of_week"),
                getattr(entry, "store_id"),
            ): entry
            for entry in existing_entities
        }

        store_schedules_set = [
            (
                getattr(entry, "day_of_week"),
                store_id,
            )
            for entry in schedules
        ]
        for store_schedule_entity in existing_entities:
            key = (
                getattr(
                    store_schedule_entity, "day_of_week"
                ),
                getattr(store_schedule_entity, "store_id"),
            )
            if key not in store_schedules_set:
                self.uow.stores.delete(
                    store_schedule_entity
                )
        for schedule_dto in schedules:
            key = (
                getattr(schedule_dto, "day_of_week"),
                store_id,
            )
            target_entity = existing_entities_set.get(
                key, None
            )

            if (
                store_id is None
                or key not in existing_entities_set
            ):
                entity = store_schedule_model_factory(
                    store_id=store_id,
                    opens_at=schedule_dto.opens_at,
                    closes_at=schedule_dto.closes_at,
                    day_of_week=schedule_dto.day_of_week,
                    is_closed=schedule_dto.is_closed,
                )
                store.schedules.append(entity)

            elif key in existing_entities_set:
                target_entity.opens_at = (
                    schedule_dto.opens_at
                )
                target_entity.closes_at = (
                    schedule_dto.closes_at
                )
                target_entity.is_closed = (
                    schedule_dto.is_closed
                )

    def _create(
        self, store: StoreCreateInputDto
    ) -> SuccessResponse:

        with self.uow:
            store_ = self.uow.stores.find_by_identifier(
                store.identifier
            )
            if store_ is not None:
                raise IdentifierExistsException()

            new_store = store_model_factory(
                name=store.name,
                address=store.address,
                identifier=store.identifier,
                zipcode=store.zipcode,
            )
            if store.store_config is not None:
                new_store.store_config = store_config_model_factory(
                    supports_dynamic_pricing=store.store_config.supports_dynamic_pricing
                )
            if store.schedules is not None:
                self._create_or_update_store_schedule(
                    schedules=store.schedules,
                    store=new_store,
                )

            self.uow.stores.create(new_store)
            self.uow.commit()

            return SuccessResponse(
                message="Loja cadastrada com sucesso!",
                code="store_registered",
                status_code=201,
            )

    def _update_store(
        self, id_: int, store: StoreUpdateInputDto
    ) -> SuccessResponse:
        with self.uow:
            existing_store = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.stores,
                entity_class=StoreEntity,
            )

            special_fields = [
                "identifier",
                "schedules",
                "store_config",
            ]

            for field, value in store.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_store, field, value)
            if (
                store.identifier is not None
                and store.identifier
                != existing_store.identifier
            ):
                store_ = self.uow.stores.find_by_identifier(
                    identifier=store.identifier
                )
                is_available = store_ is None

                if not is_available:
                    raise IdentifierExistsException()

                existing_store.identifier = store.identifier

            if store.store_config is not None:
                store_config = existing_store.store_config
                store_config.supports_dynamic_pricing = (
                    store.store_config.supports_dynamic_pricing
                )
            if store.schedules is not None:
                self._create_or_update_store_schedule(
                    schedules=store.schedules,
                    store=existing_store,
                )

            existing_store.updated_at = datetime.now()
            self.uow.commit()

            return SuccessResponse(
                message="Dados do usuário atualizados com sucesso!",
                code="store_updated",
            )

    def _update_store_icon(
        self,
        id_: int,
        icon: UploadedFile,
        scheduler=None,
    ) -> SuccessResponse:
        with self.uow:
            existent_store = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.stores,
                entity_class=StoreEntity,
            )
            existent_store.upload_icon(
                storage_service=self.storage_service,
                file=icon,
                scheduler=scheduler,
            )
            existent_store.updated_at = datetime.now()
            self.uow.commit()

        return SuccessResponse(
            message="Ícone da loja atualizado com sucesso!",
            code="store_icon_updated",
        )

    def _get_store(
        self, id_: int, entity: bool = False
    ) -> Union[StoreEntity, StoreOutputDto]:
        with self.uow:
            store_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.stores,
                entity_class=StoreEntity,
            )
            if entity:
                return store_
            return StoreOutputDto(
                **store_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            stores, results = self.uow.stores.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size

            return PaginationData(
                data=[
                    StoreOutputDto(
                        **store.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for store in stores
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _delete_store(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()
        with self.uow:
            existing_store = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.stores,
                entity_class=StoreEntity,
            )

            self.uow.stores.delete(existing_store)

            self.uow.commit()

            return SuccessResponse(
                message="Loja removida com sucesso!",
                code="store_removed",
            )
