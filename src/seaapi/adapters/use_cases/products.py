import random
from typing import Union
from datetime import datetime, timedelta
from src.seaapi.domain.entities import (
    ProductEntity,
)
from src.seaapi.domain.dtos.products import (
    ProductCreateInputDto,
    ProductOutputDto,
    ProductUpdateInputDto,
    ProductChildCreateInputDto,
    ProductScheduleOutputDto,
    ProductScheduleInputDto,
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
from src.seaapi.domain.entities.product_entity import (
    product_model_factory,
)
from src.seaapi.domain.entities.product_child_entity import (
    product_child_model_factory,
)
from src.seaapi.domain.entities.section_entity import (
    SectionEntity,
)

from src.seaapi.domain.entities.store_entity import (
    StoreEntity,
)
from src.seaapi.domain.ports.unit_of_works.stores import (
    StoreUnitOfWorkInterface,
)
from src.seaapi.domain.ports.unit_of_works.sections import (
    SectionUnitOfWorkInterface,
)
from src.seaapi.domain.ports.unit_of_works.products import (
    ProductUnitOfWorkInterface,
)
from src.seaapi.domain.ports.use_cases.products import (
    ProductServiceInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    NotAuthorizedException,
    EntityNotFoundException,
)


from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)

from src.seaapi.domain.shared.scheduler import Scheduler


class ProductService(ProductServiceInterface):
    def __init__(
        self,
        uow: ProductUnitOfWorkInterface,
        store_uow: StoreUnitOfWorkInterface,
        section_uow: SectionUnitOfWorkInterface,
        storage_service: StorageServiceInterface,
    ):
        self.uow = uow
        self.store_uow = store_uow
        self.section_uow = section_uow
        self.storage_service = storage_service

    def _create(
        self, product: ProductCreateInputDto, scheduler
    ) -> SuccessResponse:

        with self.uow:
            check_or_get_entity_if_exists(
                id_=product.section_id,
                entity_class=SectionEntity,
                active_field=None,
                repository="sections",
                uow=self.section_uow,
            )
            new_product = product_model_factory(
                name=product.name,
                description=product.description,
                section_id=product.section_id,
            )

            self.uow.products.create(new_product)

            self.uow.commit()

            if product.photo is not None:
                new_product.upload_photo(
                    storage_service=self.storage_service,
                    scheduler=scheduler,
                    file=product.photo,
                    replace=True,
                )

            self.uow.commit()

            return SuccessResponse(
                message="Produto da loja criada com sucesso!",
                code="product_registered",
                status_code=201,
            )

    def _set_fake_movimentation(self, scheduler: Scheduler):
        start_date = datetime(2025, 1, 1)
        peak_hours = [8, 12, 18, 20]
        normal_hours = [
            h for h in range(4, 24) if h not in peak_hours
        ]
        distribution = [
            0.6,
            0.4,
        ]

        for _ in range(5000):
            date = (
                start_date
                + timedelta(days=random.randint(0, 30))
            ).strftime("%Y-%m-%d")

            if (
                random.random() < distribution[0]
            ):  # Escolher horário de pico
                hour = random.choice(peak_hours)
            else:  # Escolher horário normal
                hour = random.choice(normal_hours)

            minute = random.choice([0, 10, 20, 30, 40, 50])
            duration = random.choice([20, 30, 40, 60])

            scheduler.add_appointment(
                date, f"{hour:02d}:{minute:02d}", duration
            )
        scheduler.add_appointment("2025-02-06", "08:00", 90)
        scheduler.add_appointment("2025-02-06", "08:00", 45)
        scheduler.add_appointment(
            "2025-02-06", "12:30", 120
        )
        scheduler.add_appointment("2025-02-06", "12:40", 90)

    def _get_product_schedule(
        self,
        id_: int,
        product_schedule: ProductScheduleInputDto,
    ) -> ProductScheduleOutputDto:
        with self.uow:
            product: ProductEntity = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    entity_class=ProductEntity,
                    active_field=None,
                    repository=self.uow.products,
                )
            )

            section: SectionEntity = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    entity_class=SectionEntity,
                    active_field=None,
                    uow=self.section_uow,
                    repository="sections",
                )
            )

            store: StoreEntity = section.store

            store_schedule = store.get_date_schedule(
                product_schedule.date
            )
            if (
                store_schedule is None
                or store_schedule.is_closed
            ):
                return ProductScheduleOutputDto(
                    available_times=[],
                    closed=store_schedule.is_closed,
                )

            child = product.get_child(
                product_schedule.child_id
            )

            if child is None:
                raise EntityNotFoundException()

            scheduler = Scheduler(
                work_start=str(store_schedule.opens_at),
                work_end=str(store_schedule.closes_at),
                max_price=child.max_price,
                min_price=child.min_price,
                avg_threshold=0.3,
            )
            self._set_fake_movimentation(
                scheduler=scheduler
            )
            best_time, slots = scheduler.suggest_schedule(
                date=product_schedule.date,
                duration=child.duration,
                now=datetime.now(),
            )

            return ProductScheduleOutputDto(
                available_times=slots,
                best_time=best_time,
                closed=store_schedule.is_closed,
            )

    def _create_child(
        self,
        id: int,
        product_child: ProductChildCreateInputDto,
    ) -> SuccessResponse:

        with self.uow:
            check_or_get_entity_if_exists(
                id_=id,
                entity_class=ProductEntity,
                active_field=None,
                repository=self.uow.products,
            )
            new_product_child = product_child_model_factory(
                name=product_child.name,
                description=product_child.description,
                product_id=id,
                duration=product_child.duration,
                max_price=product_child.max_price,
                min_price=product_child.min_price,
            )

            self.uow.products.create(new_product_child)

            self.uow.commit()

            return SuccessResponse(
                message=f"Variante do {id} Produto da loja criada com sucesso!",
                code="product_child_registered",
                status_code=201,
            )

    def _update_product(
        self,
        id_: int,
        product: ProductUpdateInputDto,
        scheduler,
    ) -> SuccessResponse:
        with self.uow:
            existing_product = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    repository=self.uow.products,
                    entity_class=ProductEntity,
                )
            )

            special_fields = ["photo"]

            for field, value in product.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_product, field, value)
            if product.photo is not None:
                existing_product.upload_photo(
                    storage_service=self.storage_service,
                    scheduler=scheduler,
                    file=product.photo,
                    replace=True,
                )

            existing_product.updated_at = datetime.now()
            self.uow.commit()

            return SuccessResponse(
                message="Dados do produto da loja atualizados com sucesso!",
                code="product_updated",
            )

    def _get_product(
        self, id_: int, entity: bool = False
    ) -> Union[ProductEntity, ProductOutputDto]:
        with self.uow:
            product_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.products,
                entity_class=ProductEntity,
            )
            if entity:
                return product_
            return ProductOutputDto(
                **product_.to_beautiful_dict(
                    storage_service=self.storage_service
                ),
            )

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            products, results = self.uow.products.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size
            return PaginationData(
                data=[
                    ProductOutputDto(
                        **product.to_beautiful_dict(
                            storage_service=self.storage_service
                        )
                    )
                    for product in products
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _delete_product(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()
        with self.uow:
            existing_product = (
                check_or_get_entity_if_exists(
                    id_=id_,
                    repository=self.uow.products,
                    entity_class=ProductEntity,
                )
            )

            self.uow.products.delete(existing_product)

            self.uow.commit()

            return SuccessResponse(
                message="Produto da Loja removido com sucesso!",
                code="product_removed",
            )
