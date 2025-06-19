import abc

from src.siasdapi.domain.dtos.groups import (
    GroupCreateInputDto,
    GroupUpdateInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationData,
    PaginationParams,
)


class GroupServiceInterface(abc.ABC):
    def create(
        self, group: GroupCreateInputDto
    ) -> SuccessResponse:
        return self._create(group)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def update_group(
        self, id_: int, group: GroupCreateInputDto
    ) -> PaginationData:
        return self._update_group(id_, group)

    @abc.abstractmethod
    def _create(
        self, group: GroupCreateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_group(
        self, id_: int, group: GroupUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError
