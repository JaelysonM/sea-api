from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.seaapi.adapters.unit_of_works import (
    UserSqlAlchemyUnitOfWork,
    GroupSqlAlchemyUnitOfWork,
    TokenSqlAlchemyUnitOfWork,
    PermissionSqlAlchemyUnitOfWork,
    StoreSqlAlchemyUnitOfWork,
    SectionSqlAlchemyUnitOfWork,
)
from src.seaapi.adapters.use_cases import (
    UserService,
    GroupService,
    PermissionService,
    TokenService,
    StoreService,
    SectionService,
)

from src.seaapi.adapters.services.notification.fake import (
    FakeNotificationService,
)
from src.seaapi.adapters.services.pdf.jinja import (
    JinjaPDFGenerator,
)
from src.seaapi.adapters.services.storage.fake import (
    FakeStorageService,
)


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.seaapi.adapters.entrypoints.api.v1",
            "tests",
        ]
    )

    def DEFAULT_SESSION_FACTORY():
        return scoped_session(
            sessionmaker(
                bind=create_engine(
                    "sqlite:///./test_db.db",
                    connect_args={
                        "check_same_thread": False
                    },
                )
            )
        )

    user_uow = providers.Factory(
        UserSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    group_uow = providers.Factory(
        GroupSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    permission_uow = providers.Factory(
        PermissionSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    token_uow = providers.Factory(
        TokenSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )
    store_uow = providers.Factory(
        StoreService,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    section_uow = providers.Factory(
        SectionSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    notification_service = providers.Factory(
        FakeNotificationService
    )

    pdf_service = providers.Factory(
        JinjaPDFGenerator,
    )

    storage_service = providers.Singleton(
        FakeStorageService
    )
    token_service = providers.Factory(
        TokenService,
        uow=token_uow,
    )

    user_service = providers.Factory(
        UserService,
        uow=user_uow,
        group_uow=group_uow,
        token_service=token_service,
        notification_service=notification_service,
    )

    group_service = providers.Factory(
        GroupService,
        uow=group_uow,
        permission_uow=permission_uow,
    )

    permission_service = providers.Factory(
        PermissionService, uow=permission_uow
    )

    store_service = providers.Factory(
        StoreService,
        uow=store_uow,
        storage_service=storage_service,
    )

    section_service = providers.Factory(
        StoreService,
        uow=section_uow,
        store_uow=store_uow,
        storage_service=storage_service,
    )
