from sqlalchemy import (
    Boolean,
    Column,
    Integer,
    String,
    Table,
    DateTime,
    ForeignKey,
    BigInteger,
    func,
)
from sqlalchemy.orm import relationship
from src.seaapi.adapters.db.models.base import (
    TablesRegistration,
)
from src.seaapi.domain.entities import (
    UserEntity,
    PermissionEntity,
    GroupEntity,
    TokenEntity,
)
from src.seaapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)


class UsersTables(TablesRegistration):
    def __init__(self, mapper_registry):
        self.mapper_registry = mapper_registry

    def create(self):
        self.permission = Table(
            "permissions",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "name",
                String(255),
                nullable=False,
            ),
            Column(
                "code",
                String(255),
                nullable=False,
                unique=True,
                index=True,
            ),
        )

        self.group = Table(
            "groups",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "name",
                String(255),
                nullable=False,
            ),
            Column(
                "default",
                Boolean,
                default=False,
            ),
        )

        self.user_group = Table(
            "user_groups",
            self.mapper_registry.metadata,
            Column(
                "user_id",
                BigInteger,
                ForeignKey("users.id"),
                primary_key=True,
            ),
            Column(
                "group_id",
                ForeignKey("groups.id"),
                primary_key=True,
            ),
        )

        self.group_permission = Table(
            "group_permissions",
            self.mapper_registry.metadata,
            Column(
                "group_id",
                ForeignKey("groups.id"),
                primary_key=True,
            ),
            Column(
                "permission_id",
                ForeignKey("permissions.id"),
                primary_key=True,
            ),
        )

        self.user = Table(
            "users",
            self.mapper_registry.metadata,
            Column(
                "id",
                BigInteger,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "first_name",
                String(255),
                nullable=False,
            ),
            Column(
                "last_name",
                String(255),
                nullable=False,
            ),
            Column(
                "email",
                String(255),
                nullable=False,
                unique=True,
                index=True,
            ),
            Column(
                "password",
                String(255),
                nullable=False,
            ),
            Column(
                "is_active",
                Boolean(),
                default=True,
            ),
            Column(
                "is_super_user",
                Boolean(),
                default=False,
            ),
            Column(
                "created_at",
                DateTime,
                server_default=func.now(),
                nullable=False,
            ),
            Column(
                "updated_at",
                DateTime,
                server_default=func.now(),
                onupdate=func.now(),
                nullable=False,
            ),
            Column("deleted_at", DateTime),
            Column("last_login", DateTime),
        )

        self.token = Table(
            "tokens",
            self.mapper_registry.metadata,
            Column(
                "id",
                Integer,
                primary_key=True,
                autoincrement=True,
            ),
            Column(
                "type",
                String(255),
                nullable=False,
            ),
            Column(
                "token",
                String(255),
                nullable=False,
            ),
            Column(
                "reference",
                BigInteger,
                ForeignKey("users.id"),
            ),
            Column(
                "created_at",
                DateTime,
                server_default=func.now(),
                nullable=False,
            ),
            Column(
                "expiration",
                DateTime,
                server_default=func.now(),
            ),
        )

    def register(self):

        self.mapper_registry.map_imperatively(
            PermissionEntity,
            self.permission,
        )
        self.mapper_registry.map_imperatively(
            GroupEntity,
            self.group,
            properties={
                "permissions": relationship(
                    PermissionEntity,
                    secondary=self.group_permission,
                    lazy="subquery",
                ),
            },
        )
        self.mapper_registry.map_imperatively(
            UserEntity,
            self.user,
            properties={
                "groups": relationship(
                    GroupEntity,
                    secondary=self.user_group,
                    lazy="subquery",
                ),
            },
        )
        self.mapper_registry.map_imperatively(
            TokenEntity,
            self.token,
        )
        super().register()
        user_service: UserServiceInterface = (
            self.container.user_service()
        )
        user_service.create_super_user()
