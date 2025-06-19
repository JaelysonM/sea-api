import abc
from typing import Union

from src.seaapi.domain.entities import (
    UserEntity,
)
from src.seaapi.domain.dtos.users import (
    UserCreateInputDto,
    UserUpdateInputDto,
    UserLoginInputDto,
    UserOutputDto,
    UserForgotPasswordInputDto,
    UserRecoverPasswordInputDto,
)
from src.seaapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
)
from src.seaapi.domain.dtos.tokens import Tokens


class UserServiceInterface(abc.ABC):
    def create(
        self, user: UserCreateInputDto
    ) -> SuccessResponse:
        return self._create(user)

    def create_super_user(
        self,
    ) -> SuccessResponse:
        return self._create_super_user()

    def authenticate_user(
        self, user: UserLoginInputDto
    ) -> Union[Tokens, bool]:
        return self._authenticate_user(user)

    def refresh_access_token(self, token: str) -> Tokens:
        return self._refresh_access_token(token=token)

    def get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        return self._get_all(params=params)

    def get_user(
        self, id_: int, entity: bool = False
    ) -> Union[UserEntity, UserOutputDto]:
        return self._get_user(id_, entity)

    def get_authenticated_user(
        self, entity: UserEntity
    ) -> UserOutputDto:
        return self._get_authenticated_user(entity)

    def update_user(
        self, id_: int, user: UserUpdateInputDto
    ) -> SuccessResponse:
        return self._update_user(id_, user)

    def deactivate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._deactivate_user(id_)

    def activate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        return self._activate_user(id_)

    def forgot_password(
        self, dto: UserForgotPasswordInputDto, scheduler
    ):
        return self._forgot_password(dto, scheduler)

    def recover_password(
        self, dto: UserRecoverPasswordInputDto, token: str
    ) -> SuccessResponse:
        return self._recover_password(dto=dto, token=token)

    @abc.abstractmethod
    def _create(
        self, user: UserUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _authenticate_user(
        self, user: UserLoginInputDto
    ) -> Union[Tokens, bool]:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_authenticated_user(
        self, id_: int
    ) -> UserOutputDto:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_user(
        self, id_: int, entity: bool = True
    ) -> Union[UserEntity, UserOutputDto]:
        raise NotImplementedError

    @abc.abstractmethod
    def _update_user(
        self, id_: int, user: UserUpdateInputDto
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _get_all(
        self,
        params: PaginationParams,
    ) -> PaginationData:
        raise NotImplementedError

    @abc.abstractmethod
    def _deactivate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _activate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _create_super_user(
        self,
    ) -> SuccessResponse:
        raise NotImplementedError

    @abc.abstractmethod
    def _refresh_access_token(self, token: str) -> Tokens:
        raise NotImplementedError

    @abc.abstractmethod
    async def _forgot_password(
        self, dto: UserForgotPasswordInputDto, scheduler
    ):
        raise NotImplementedError

    @abc.abstractmethod
    def _recover_password(
        self,
        dto: UserRecoverPasswordInputDto,
        token=None,
    ) -> SuccessResponse:
        raise NotImplementedError
