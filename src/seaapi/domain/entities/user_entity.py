from datetime import datetime
from dataclasses import asdict
from copy import deepcopy
from typing import List, Optional, Set, Tuple, Dict
from dataclasses import dataclass, field
from src.seaapi.domain.shared.hash import Hasher
from src.seaapi.domain.shared.security import create_token
from src.seaapi.domain.dtos.tokens import Tokens
from src.seaapi.domain.ports.shared.exceptions import (
    UserNotActiveException,
    InvalidCredentialsException,
    SamePasswordBeforeException,
)
from src.seaapi.domain.entities.group_entity import (
    GroupEntity,
)
from src.seaapi.domain.entities.permission_entity import (
    PermissionEntity,
)
from src.seaapi.domain.entities.base import BaseEntity
from src.seaapi.domain import Role


@dataclass
class UserEntity(BaseEntity):

    id: int

    first_name: str
    last_name: str
    email: str
    password: str
    is_active: bool
    is_super_user: bool

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]
    last_login: datetime

    groups: Optional[List[GroupEntity]] = field(
        default_factory=list
    )

    class Meta:
        def groups_filter(value):  # pragma: no cover
            if value is None:
                return True
            if value.lower() == "admin":
                return UserEntity.is_super_user
            return UserEntity.groups.any(
                GroupEntity.name.ilike(f"%{value.lower()}%")
            )

        masculine = True
        verbose = "Usuário"
        display_name = "User"
        name = "user"
        search = ["first_name", "last_name", "email"]
        filters = [
            "id",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_super_user",
            "created_at",
            "updated_at",
            "groups",
        ]
        composite_field = None
        active_field = "is_active"

        filter_mapper = {
            "groups": groups_filter,
        }
        joins = []

    @property
    def full_name(self) -> str:
        return f"{self.first_name} {self.last_name}"

    @property
    def permissions(self) -> Set[PermissionEntity]:
        permissions = set()
        for group in self.groups:
            for permission in group.permissions:
                permissions.add(permission)
        return permissions

    @property
    def permissions_codes(self) -> List[str]:
        permissions_code = []
        for permission in self.permissions:
            permissions_code.append(permission.code)
        return permissions_code

    @property
    def groups_ids(self) -> List[int]:
        ids = [group.id for group in self.groups]
        if self.is_super_user:
            ids = ids + [0]
        return ids

    def has_role(self, role: Role, exact=False) -> bool:
        return role.check_privileges(self.groups_ids, exact)

    @property
    def city_composed(self) -> Dict:
        if self.cidade is not None:
            return self.cidade.flat()

    def has_permission(self, permission: str) -> bool:
        if self.is_super_user:
            return True
        return permission in self.permissions_codes

    def check_password(self, password) -> bool:
        return Hasher.verify_password(
            password, self.password
        )

    def set_password(self, password: str):
        hashed_new_password = Hasher.get_password_hash(
            password
        )
        self.password = hashed_new_password

    def change_password(
        self, password: str, new_password: str
    ) -> bool:

        if (
            password is not None
            and not self.check_password(password)
        ):
            raise InvalidCredentialsException()

        if self.check_password(new_password):
            raise SamePasswordBeforeException()

        self.set_password(new_password)

    def authenticate(self, password) -> bool:
        if not self.is_active:
            raise UserNotActiveException()

        if not self.check_password(password):
            raise InvalidCredentialsException()

        self.last_login = datetime.now()
        return True

    @property
    def access_token(self) -> Tuple[str, datetime]:
        return create_token({"user_id": self.id}, "access")

    @property
    def refresh_token(self) -> Tuple[str, datetime]:
        return create_token({"user_id": self.id}, "refresh")

    @property
    def tokens(
        self,
    ) -> Tuple[Tokens, Tuple[datetime, datetime]]:
        (
            access_token,
            access_token_expiration,
        ) = self.access_token
        (
            refresh_token,
            refresh_token_expiration,
        ) = self.refresh_token
        return Tokens(
            access_token=access_token,
            refresh_token=refresh_token,
        ), [
            access_token_expiration,
            refresh_token_expiration,
        ]

    def can_generate_qrcode(self) -> bool:
        return self.is_active

    def authenticate_qrcode(
        self,
    ) -> Tuple[Tokens, Tuple[datetime, datetime]]:
        if not self.is_active:
            raise UserNotActiveException()

        self.last_login = datetime.now()
        return self.tokens

    def mask_email(self) -> str:
        username, domain = self.email.split("@")
        if len(username) > 2:
            masked_username = (
                username[0]
                + "*" * (len(username) - 2)
                + username[-1]
            )
            masked_email = f"{masked_username}@{domain}"
            return masked_email

    def __eq__(self, other):
        if not isinstance(other, UserEntity):
            return False
        return self.email == other.email

    def __hash__(self):
        return hash(
            (
                self.id,
                self.first_name,
                self.last_name,
                self.email,
                self.password,
                self.is_active,
                self.is_super_user,
                self.created_at,
                self.updated_at,
                self.deleted_at,
                self.last_login,
            )
        )

    def to_dict(self):
        copy_self = deepcopy(self)
        copy_self.cliente = None
        safe_dict = asdict(copy_self)
        return safe_dict

    def to_beautiful_dict(self):
        user_dict = self.to_dict()
        user_dict["permissions"] = self.permissions_codes

        return user_dict


def user_model_factory(
    first_name: str,
    last_name: str,
    email: str,
    password: str,
    is_active: bool,
    is_super_user: bool,
    created_at: datetime = datetime.now(),
    updated_at: datetime = datetime.now(),
    deleted_at: datetime = None,
    last_login: datetime = datetime.now(),
    id: int = None,
) -> UserEntity:
    return UserEntity(
        id=id,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=password,
        is_active=is_active,
        is_super_user=is_super_user,
        created_at=created_at,
        updated_at=updated_at,
        deleted_at=deleted_at,
        last_login=last_login,
    )
