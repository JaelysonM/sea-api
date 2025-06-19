from typing import List, Tuple
from src.seaapi.domain.entities.base import BaseEntity
from src.seaapi.domain.ports.repositories import (
    BaseRepositoryInterface,
)
from src.seaapi.domain.ports.unit_of_works import (
    DefaultUnitOfWorkInterface,
)
from src.seaapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


def custom_integer_parts(
    number, upper_part, lower_part
) -> Tuple[int, int]:
    if (
        upper_part < 0
        or upper_part > 100
        or lower_part < 0
        or lower_part > 100
    ):
        raise ValueError(
            "Os valores de upper_part e lower_part "
            "devem estar entre 0 e 100."
        )

    number = abs(number)
    total_parts = upper_part + lower_part
    if total_parts == 0:
        raise ValueError(
            "A soma de upper_part e lower_part não pode ser zero."
        )

    lower_half = int(number * (lower_part / total_parts))
    return (number - lower_half, lower_half)


def calculate_difference(
    old_ids, new_ids
) -> Tuple[int, int]:
    removed_ids = set(old_ids) - set(new_ids)
    added_ids = set(new_ids) - set(old_ids)
    return list(removed_ids), list(added_ids)


def update_entity_list(
    target_entity: BaseEntity,
    entity_class: BaseEntity,
    target_field: int,
    repository: Tuple[str, BaseRepositoryInterface],
    ids: List[int],
    uow: DefaultUnitOfWorkInterface = None,
    active_field: str = "ativo",
    cross_id: int = None,
    expunge_method=None,
    expunge=True,
) -> Tuple[List[int], List[int]]:
    def run():

        old_ids = [
            item.id
            for item in getattr(target_entity, target_field)
        ]
        removed, added = calculate_difference(old_ids, ids)
        if uow is not None:
            repository_instance = getattr(uow, repository)
        else:
            repository_instance = repository

        for remove in removed:
            entity = repository_instance.find_by_id(remove)
            getattr(target_entity, target_field).remove(
                entity
            )
        for add in added:
            entity = check_or_get_entity_if_exists(
                active_field=active_field,
                cross_id=cross_id,
                entity_class=entity_class,
                id_=add,
                repository=repository,
                uow=uow,
            )
            if expunge:
                if uow is None:
                    expunge_method()
                else:
                    uow.expunge()
            getattr(target_entity, target_field).append(
                entity
            )
        return removed, added

    if uow is not None:
        with uow:
            return run()
    else:
        return run()
