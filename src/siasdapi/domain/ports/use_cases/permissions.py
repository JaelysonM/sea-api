import abc

from src.siasdapi.domain.dtos.permissions import (
    PermissionCreateInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationData,
    PaginationParams,
)


class PermissionServiceInterface(abc.ABC):
    def create(
        self, permission: PermissionCreateInputDto
    ) -> SuccessResponse:
        return self._create(permission)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    @abc.abstractmethod
    def _create(
        self, permission: PermissionCreateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError
