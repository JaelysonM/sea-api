import abc
from typing import Union

from src.siasdapi.domain.entities import (
    SectionEntity,
)
from src.siasdapi.domain.dtos.sections import (
    SectionCreateInputDto,
    SectionUpdateInputDto,
    SectionOutputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)


class SectionServiceInterface(abc.ABC):
    def create(
        self, section: SectionCreateInputDto
    ) -> SuccessResponse:
        return self._create(section)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_section(
        self, id_: int, entity: bool = False
    ) -> Union[SectionEntity, SectionOutputDto]:
        return self._get_section(id_, entity)

    def update_section(
        self, id_: int, section: SectionUpdateInputDto
    ) -> SuccessResponse:
        return self._update_section(id_, section)

    def delete_section(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._delete_section(id_)

    @abc.abstractmethod
    def _create(
        self, section: SectionUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_section(
        self, id_: int, entity: bool = True
    ) -> Union[SectionEntity, SectionOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_section(
        self, id_: int, section: SectionUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _delete_section(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError
