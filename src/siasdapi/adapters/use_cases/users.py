import json
import base64
from typing import Union
from datetime import datetime
from src.siasdapi.domain.shared.hash import Hasher
from src.siasdapi.config.settings import settings
from src.siasdapi.domain.entities import (
    UserEntity,
    GroupEntity,
)
from src.siasdapi.domain.dtos.users import (
    UserCreateInputDto,
    UserLoginInputDto,
    UserOutputDto,
    UserUpdateInputDto,
    UserForgotPasswordInputDto,
    UserRecoverPasswordInputDto,
)
from src.siasdapi.domain.dtos.mics import (
    SuccessResponse,
    PaginationParams,
    PaginationData,
    PaginationOptions,
)
from src.siasdapi.domain.dtos.tokens import (
    TokenCreateInputDto,
    RefreshTokenDto,
)
from src.siasdapi.domain.dtos.tokens import Tokens
from src.siasdapi.domain.entities.user_entity import (
    user_model_factory,
)

from src.siasdapi.domain.ports.unit_of_works.users import (
    UserUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)
from src.siasdapi.domain.ports.unit_of_works.groups import (
    GroupUnitOfWorkInterface,
)
from src.siasdapi.domain.ports.shared.exceptions import (
    SystemException,
    InvalidCredentialsException,
    ExpiredTokenException,
    EmailExistsException,
    UserNotFoundException,
    ExpiredVerificationTokenException,
    NotAuthorizedException,
    EntityAlreadyActiveException,
    EmailExistsInInactiveUserException,
)


from src.siasdapi.domain.ports.use_cases.tokens import (
    TokenServiceInterface,
)
from src.siasdapi.domain.ports.services.notification import (
    NotificationServiceInterface,
)

from src.siasdapi.domain.shared.security import (
    password_reset_token_generator,
)

from src.siasdapi.domain.shared.messages import (
    ForgotPasswordMessage,
)
from src.siasdapi.domain.shared.utils import (
    update_entity_list,
)
from src.siasdapi.domain.shared.validators import (
    check_or_get_entity_if_exists,
)


class UserService(UserServiceInterface):
    def __init__(
        self,
        uow: UserUnitOfWorkInterface,
        group_uow: GroupUnitOfWorkInterface,
        token_service: TokenServiceInterface,
        notification_service: NotificationServiceInterface,
    ):
        self.uow = uow
        self.group_uow = group_uow

        self.token_service = token_service
        self.notification_service = notification_service

    def _create(
        self, user: UserCreateInputDto, raises=True
    ) -> SuccessResponse:

        with self.uow:
            user_ = self.uow.users.find_by_email(user.email)
            if user_ is not None:
                if not raises:
                    return
                if user_.is_active:
                    raise EmailExistsException()
                else:
                    raise EmailExistsInInactiveUserException()
            password = Hasher.get_password_hash(
                user.password
            )

            new_user = user_model_factory(
                first_name=user.first_name,
                last_name=user.last_name,
                password=password,
                email=user.email,
                is_active=user.is_active,
                is_super_user=user.is_super_user,
            )

            if user.groups is not None:
                update_entity_list(
                    ids=user.groups,
                    target_entity=new_user,
                    entity_class=GroupEntity,
                    target_field="groups",
                    repository="groups",
                    uow=self.group_uow,
                )

            self.uow.users.create(new_user)
            self.uow.commit()

            return SuccessResponse(
                message="Usuário cadastrado com sucesso!",
                code="user_registered",
                status_code=201,
            )

    def _create_super_user(self):
        if (
            settings.SUPERUSER_EMAIL is None
            or settings.SUPERUSER_PASSWORD is None
        ):  # pragma: no cover
            print(
                "[WARN] Please configure SUPERUSER_EMAIL and SUPERUSER_PASSWORD"
            )
            return

        super_user_ = UserCreateInputDto(
            id=0,
            first_name="Admin",
            last_name=settings.MARKETING_NAME,
            email=settings.SUPERUSER_EMAIL,
            password=settings.SUPERUSER_PASSWORD,
            is_active=True,
            is_super_user=True,
            groups=[],
        )

        return self._create(user=super_user_, raises=False)

    def _update_user(
        self, id_: int, user: UserUpdateInputDto
    ) -> SuccessResponse:
        with self.uow:
            existing_user = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.users,
                entity_class=UserEntity,
            )

            special_fields = [
                "password",
                "new_password",
                "email",
                "groups",
            ]

            for field, value in user.dict(
                exclude_unset=True
            ).items():
                if field not in special_fields:
                    setattr(existing_user, field, value)
            if (
                user.email is not None
                and user.email != existing_user.email
            ):
                user_ = self.uow.users.find_by_email(
                    email=user.email
                )
                is_available = user_ is None

                if not is_available:
                    if user_.is_active:
                        raise EmailExistsException()
                    else:
                        raise EmailExistsInInactiveUserException()
                existing_user.email = user.email

            if (
                user.new_password is not None
                and user.password is not None
            ):
                existing_user.change_password(
                    password=user.password,
                    new_password=user.new_password,
                )
            if (
                hasattr(user, "groups")
                and user.groups is not None
            ):  # pragma: no cover
                update_entity_list(
                    ids=user.groups,
                    target_entity=existing_user,
                    target_field="groups",
                    entity_class=GroupEntity,
                    repository="groups",
                    uow=self.group_uow,
                )

            existing_user.updated_at = datetime.now()
            self.uow.commit()

            return SuccessResponse(
                message="Dados do usuário atualizados com sucesso!",
                code="user_updated",
            )

    def _authenticate_user(
        self, user: UserLoginInputDto
    ) -> Union[Tokens, bool]:
        with self.uow:
            user_ = self.uow.users.find_by_email(user.email)
            if not user_:
                raise InvalidCredentialsException()

            user_.authenticate(user.password)
            tokens, expiration = user_.tokens
            _, refresh_token_expiration = expiration
            token_input = TokenCreateInputDto(
                type="refresh",
                token=tokens.refresh_token,
                expiration=refresh_token_expiration,
                reference=user_.id,
            )
            self.uow.commit()
            self.token_service.create(token=token_input)
            return tokens

    def _get_user(
        self, id_: int, entity: bool = False
    ) -> Union[UserEntity, UserOutputDto]:
        with self.uow:
            user_ = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.users,
                entity_class=UserEntity,
            )
            if entity:
                return user_
            return UserOutputDto(
                **user_.to_beautiful_dict(),
            )

    def _get_authenticated_user(
        self, entity: UserEntity
    ) -> UserOutputDto:
        return self._get_user(id_=entity.id)

    def _get_all(
        self, params: PaginationParams
    ) -> PaginationData:
        with self.uow:
            page = params.page
            page_size = params.page_size
            users, results = self.uow.users.find_all(
                params=params,
            )
            pages = (results + page_size - 1) // page_size

            return PaginationData(
                data=[
                    UserOutputDto(
                        **user.to_beautiful_dict()
                    )
                    for user in users
                ],
                options=PaginationOptions(
                    page=page,
                    pages=pages,
                    size=page_size,
                    results=results,
                ),
            )

    def _deactivate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        if id_ == 1:
            raise NotAuthorizedException()
        with self.uow:
            existing_user = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.users,
                entity_class=UserEntity,
            )

            existing_user.soft_delete()

            self.uow.commit()

            return SuccessResponse(
                message="Usuário removido com sucesso!",
                code="user_removed",
            )

    def _activate_user(
        self,
        id_: int,
    ) -> SuccessResponse:
        with self.uow:
            existing_user = check_or_get_entity_if_exists(
                id_=id_,
                repository=self.uow.users,
                entity_class=UserEntity,
                active_field=None,
            )
            if existing_user.is_active:
                raise EntityAlreadyActiveException()

            existing_user.recover()

            self.uow.commit()

            return SuccessResponse(
                message="Usuário recuperado com sucesso!",
                code="user_recovered",
            )

    def _refresh_access_token(
        self, token: RefreshTokenDto
    ) -> Tokens:

        with self.token_service.uow:
            token_ = self.token_service.uow.tokens.find_by_token_and_type(
                token=token.refresh_token, type="refresh"
            )
            if token_ is None:
                raise ExpiredTokenException()

            user_ = self._get_user(
                id_=token_.reference, entity=True
            )

            access_token, _ = user_.access_token

            return Tokens(
                access_token=access_token,
                refresh_token=token.refresh_token,
            )

    def _forgot_password(
        self, dto: UserForgotPasswordInputDto, scheduler
    ):
        with self.uow:
            user_ = self.uow.users.find_by_email(dto.email)
            if user_ is None:
                raise UserNotFoundException()
            (
                token,
                expiration,
            ) = password_reset_token_generator.make_token(
                user_
            )

            self.token_service.create(
                token=TokenCreateInputDto(
                    type="change_password",
                    token=token,
                    expiration=expiration,
                    reference=user_.id,
                )
            )

            info = {
                "name": user_.full_name,
                "email": user_.mask_email(),
                "id": user_.id,
            }
            json_info = json.dumps(info)

            encrypted_info = base64.b64encode(
                json_info.encode()
            ).decode()

            link = (
                f"{settings.WEB_APP_BASE_URL}/change-password"
                + f"?token={token}&info={encrypted_info}"
            )

            message = ForgotPasswordMessage(link)
            try:
                scheduler.add_task(
                    self.notification_service.send_notification,
                    target=user_.email,
                    message=message,
                )
            except Exception as e:  # pragma: no cover
                print(e)
                raise SystemException(
                    "Ocorreu um erro inesperado ao tentar enviar seu email"
                )

    def _recover_password(
        self, dto: UserRecoverPasswordInputDto, token: str
    ):
        with self.uow:
            with self.token_service.uow:
                token_ = self.token_service.uow.tokens.find_by_token_and_type(
                    token=token, type="change_password"
                )
                if token_ is None:
                    raise ExpiredVerificationTokenException()

                user_ = self.uow.users.find_by_id(
                    token_.reference
                )

                if user_ is None:
                    raise UserNotFoundException()

                if not password_reset_token_generator.check_token(
                    user_, token
                ):
                    raise ExpiredVerificationTokenException()

                user_.change_password(
                    password=None,
                    new_password=dto.new_password,
                )

                self.token_service.delete(token_)

                self.uow.commit()
                self.token_service.uow.commit()

                message = (
                    "Senha recuperada com sucesso! "
                    + f"Acesse usando o email {user_.mask_email()}"
                )

                return SuccessResponse(
                    message=message,
                    code="password_recovered",
                )
