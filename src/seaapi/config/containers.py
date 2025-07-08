from dependency_injector import containers, providers
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from src.seaapi import config
from src.seaapi.adapters.unit_of_works import (
    UserSqlAlchemyUnitOfWork,
    GroupSqlAlchemyUnitOfWork,
    TokenSqlAlchemyUnitOfWork,
    PermissionSqlAlchemyUnitOfWork,
    FoodSqlAlchemyUnitOfWork,
    ScaleSqlAlchemyUnitOfWork,
    MealSqlAlchemyUnitOfWork,
)
from src.seaapi.adapters.use_cases import (
    UserService,
    GroupService,
    PermissionService,
    TokenService,
    FoodService,
    MealService,
    ScaleService,
)
from src.seaapi.adapters.use_cases.qrcode import (
    QRCodeAuthService,
)
from src.seaapi.config.settings import settings

from src.seaapi.adapters.services.notification.email import (
    EmailNotificationService,
)

# Messaging imports
from src.seaapi.adapters.services.messaging import (
    MQTTPublisher,
    MQTTConsumer,
    EventBus,
)

from src.seaapi.adapters.services.pdf.jinja import (
    JinjaPDFGenerator,
)

from src.seaapi.adapters.services.qrcode import (
    QRCodeService,
)


from src.seaapi.adapters.services.storage import (
    S3StorageService,
    MinIOStorageService,
)

ENGINE = create_engine(config.get_database_uri())


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "..adapters.entrypoints.api.v1",
        ]
    )

    def DEFAULT_SESSION_FACTORY():
        return scoped_session(
            sessionmaker(
                bind=ENGINE, expire_on_commit=False
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

    food_uow = providers.Factory(
        FoodSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    scale_uow = providers.Factory(
        ScaleSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    meal_uow = providers.Factory(
        MealSqlAlchemyUnitOfWork,
        session_factory=DEFAULT_SESSION_FACTORY,
    )

    notification_service = providers.Factory(
        EmailNotificationService,
    )

    pdf_service = providers.Factory(
        JinjaPDFGenerator,
    )

    qrcode_generator = providers.Factory(
        QRCodeService,
    )

    storage_service = providers.Singleton(
        S3StorageService
        if settings.STORAGE_PROVIDER == "s3"
        else MinIOStorageService,
    )

    token_service = providers.Factory(
        TokenService,
        uow=token_uow,
    )

    group_service = providers.Factory(
        GroupService,
        uow=group_uow,
        permission_uow=permission_uow,
    )

    permission_service = providers.Factory(
        PermissionService, uow=permission_uow
    )

    food_service = providers.Factory(
        FoodService,
        uow=food_uow,
        scale_uow=scale_uow,
        storage_service=storage_service,
    )

    # Messaging providers (definir antes dos serviços que dependem deles)
    # Messaging providers
    mqtt_publisher = providers.Factory(MQTTPublisher)

    mqtt_consumer = providers.Factory(
        MQTTConsumer,
    )

    event_bus = providers.Factory(
        EventBus,
        publisher=mqtt_publisher,
        consumer=mqtt_consumer,
    )

    user_service = providers.Factory(
        UserService,
        uow=user_uow,
        group_uow=group_uow,
        token_service=token_service,
        notification_service=notification_service,
    )

    meal_service = providers.Factory(
        MealService,
        uow=meal_uow,
        food_uow=food_uow,
        user_uow=user_uow,
        storage_service=storage_service,
    )

    scale_service = providers.Factory(
        ScaleService,
        uow=scale_uow,
    )

    qrcode_service = providers.Factory(
        QRCodeAuthService,
        token_uow=token_uow,
        token_service=token_service,
        user_service=user_service,
        qrcode_generator=qrcode_generator,
    )
