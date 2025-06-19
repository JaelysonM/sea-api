from sqlalchemy.orm import Session, noload
from sqlalchemy import or_, and_, not_, func, desc, asc
from typing import T, Tuple, List
from datetime import date, datetime
from src.siasdapi.domain.ports.repositories import (
    BaseWriteableRepositoryInterface,
)
from src.siasdapi.domain.dtos.mics import (
    PaginationParams,
    default_pagination_params,
    Operator,
)


class DefaultAlchemyRepository(
    BaseWriteableRepositoryInterface
):
    session: Session

    def __init__(self, session: Session):
        super().__init__()
        self.session = session

    def _create(self, entity):
        self.session.add(entity)

    def _delete(self, entity):
        self.session.delete(entity)

    def _find_by_id(self, *args, **kwargs) -> T:
        id_ = args[0]

        composite_field = None
        if self.entity is not None and hasattr(
            self.entity.Meta, "composite_field"
        ):
            composite_field = (
                self.entity.Meta.composite_field
            )
        query = self.session.query(self.entity)
        if (
            kwargs.get(composite_field, None) is not None
        ):  # pragma: no cover
            composite_field_value = kwargs.get(
                composite_field, None
            )
            query = query.filter_by(
                **{composite_field: composite_field_value}
            )
        return query.filter_by(id=id_).first()

    def _count_all(self, **kwargs) -> int:
        query = self.session.query(self.entity)
        composite_field = None
        if self.entity is not None and hasattr(
            self.entity.Meta, "composite_field"
        ):
            composite_field = (
                self.entity.Meta.composite_field
            )

        if (
            kwargs.get(composite_field, None) is not None
        ):  # pragma: no cover
            composite_field_value = kwargs.get(
                composite_field, None
            )
            query = query.filter_by(
                **{composite_field: composite_field_value}
            )
        active_field = None
        if self.entity is not None and hasattr(
            self.entity.Meta, "active_field"
        ):
            active_field = self.entity.Meta.active_field

        if (
            kwargs.get(active_field, None) is not None
        ):  # pragma: no cover
            active_field_value = kwargs.get(
                active_field, None
            )
            query = query.filter_by(
                **{active_field: active_field_value}
            )
        return query.count()

    def _find_all(self, **kwargs) -> Tuple[List[T], int]:
        params: PaginationParams = kwargs.pop(
            "params", default_pagination_params
        )

        search_query = params.search or ""
        page_size = params.page_size
        page = params.page

        query = self.session.query(self.entity)

        if hasattr(self.entity.Meta, "joins"):
            for join in getattr(
                self.entity.Meta, "joins", []
            ):
                query = query.outerjoin(join)

        if hasattr(self.entity.Meta, "no_load"):
            noload_items = []
            for field in getattr(
                self.entity.Meta, "no_load", []
            ):
                noload_items.append(
                    getattr(self.entity, field)
                )
            query = query.options(
                noload(item) for item in noload_items
            )

        composite_field = None
        if self.entity is not None and hasattr(
            self.entity.Meta, "composite_field"
        ):
            composite_field = (
                self.entity.Meta.composite_field
            )

        if (
            kwargs.get(composite_field, None) is not None
        ):  # pragma: no cover
            composite_field_value = kwargs.get(
                composite_field, None
            )
            query = query.filter(
                getattr(self.entity, composite_field)
                == composite_field_value
            )

        if hasattr(self.entity.Meta, "search"):
            clauses = [
                func.lower(
                    getattr(self.entity, field)
                ).like(f"%{search_query.lower()}%")
                for field in self.entity.Meta.search
            ]
            if len(clauses) > 0:
                query = query.filter(or_(*clauses))

        if hasattr(self.entity.Meta, "filters"):

            def operator_mapper(
                operator, attribute, value
            ):  # pragma: no cover
                if operator == Operator.IN.value:
                    return getattr(
                        self.entity, attribute
                    ).in_(value)
                elif operator == Operator.NOT_IN.value:
                    return getattr(
                        self.entity, attribute
                    ).notin_(value)
                elif operator == Operator.LTE.value:
                    return (
                        getattr(self.entity, attribute)
                        <= value
                    )
                elif operator == Operator.LT.value:
                    return (
                        getattr(self.entity, attribute)
                        < value
                    )
                elif operator == Operator.GTE.value:
                    return (
                        getattr(self.entity, attribute)
                        >= value
                    )
                elif operator == Operator.GT.value:
                    return (
                        getattr(self.entity, attribute)
                        > value
                    )
                elif operator == Operator.NOT.value:
                    return not_(
                        getattr(self.entity, attribute)
                        == value
                    )
                elif operator == Operator.EXACT.value:
                    return (
                        getattr(self.entity, attribute)
                        == value
                    )
                return True

            def filter_mapper(field):  # pragma: no cover
                is_valid_field = getattr(
                    self.entity, field
                ) and hasattr(params, field)
                if is_valid_field:
                    value = getattr(params, field)
                    value_type = type(value)
                    if hasattr(
                        self.entity.Meta, "filter_mapper"
                    ) and field in getattr(
                        self.entity.Meta, "filter_mapper"
                    ):
                        mapper_func = getattr(
                            self.entity.Meta,
                            "filter_mapper",
                        )
                        clause = mapper_func[field](value)
                        if type(clause) is tuple:
                            method = clause[0]
                            conditions = clause[1]
                            return (
                                or_(*conditions)
                                if method == "or"
                                else and_(*conditions)
                            )
                        elif type(clause) is list:
                            return and_(*clause)
                        else:
                            return clause
                    elif value_type == str:
                        return func.lower(
                            getattr(self.entity, field)
                        ).like(f"%{value.lower()}%")
                    elif value_type == tuple:
                        operator, v = value
                        return operator_mapper(
                            operator=operator,
                            value=v,
                            attribute=field,
                        )
                    elif value_type == dict:
                        operations = []
                        for operator, v in value.items():
                            operations.append(
                                operator_mapper(
                                    operator=operator,
                                    value=v,
                                    attribute=field,
                                )
                            )
                        return and_(*operations)

                    elif (
                        value_type == int
                        or value_type == bool
                        or value_type == float
                        or value_type == date
                        or value_type == datetime
                    ):
                        return (
                            getattr(self.entity, field)
                            == value
                        )
                return None

            clauses = [
                filter_mapper(field)
                for field in self.entity.Meta.filters
            ]
            clauses = [
                clause
                for clause in clauses
                if clause is not None
            ]

            query = query.filter(and_(True, *clauses))
        if (
            hasattr(params, "order")
            and params.order != ""
            and params.order is not None
        ):
            order = params.order
            field, direction = order.split(",")
            if hasattr(self.entity, field):
                field_attr = getattr(self.entity, field)

                if direction.lower() == "asc":
                    query = query.order_by(asc(field_attr))
                elif direction.lower() == "desc":
                    query = query.order_by(desc(field_attr))
        else:
            query = query.order_by(
                asc(getattr(self.entity, "id"))
            )
        results = query.count()
        if page is None:  # pragma: no cover
            return query.all(), results
        data = (
            query.offset((page - 1) * page_size)
            .limit(page_size)
            .all()
        )

        return data, results
