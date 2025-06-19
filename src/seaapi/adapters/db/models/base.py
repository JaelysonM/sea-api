import sys
from abc import ABC, abstractclassmethod
from src.seaapi.domain.ports.use_cases.permissions import (
    PermissionServiceInterface,
)
from src.seaapi.domain.dtos.permissions import (
    PermissionCreateInputDto,
)
from src.seaapi.config.containers import Container
from tests.fake_container import Container as FakeContainer


class TablesRegistration(ABC):
    mapper_registry = None
    container = None

    @abstractclassmethod
    def create(self):
        pass

    @staticmethod
    def inject_container(instances, container):
        for instance in instances:
            instance.set_container(container)

    def set_container(self, container):
        self.container = container

    def register(self):
        registered_models = [
            model.class_
            for model in self.mapper_registry.mappers
        ]
        for model in registered_models:
            default_name = model.__name__.lower().replace(
                "entity", ""
            )
            if not hasattr(model, "Meta"):
                return
            permissions = (
                model.Meta.permissions
                if hasattr(model.Meta, "permissions")
                else ()
            )
            display_name = (
                model.Meta.display_name
                if hasattr(model.Meta, "display_name")
                else default_name.upper()
            )
            name = (
                model.Meta.name
                if hasattr(model.Meta, "name")
                else default_name
            )

            default_permissions = (
                (
                    f"Create {display_name}",
                    f"create_{name}",
                ),
                (f"Read {display_name}", f"read_{name}"),
                (f"Edit {display_name}", f"edit_{name}"),
                (
                    f"Delete {display_name}",
                    f"delete_{name}",
                ),
            )
            all_permissions = permissions

            if (
                display_name is not None
                and name is not None
            ):
                all_permissions = (
                    all_permissions + default_permissions
                )

            container = Container

            from_test = "pytest" in sys.argv[0]
            if from_test is True:
                container = FakeContainer
            permission_service: PermissionServiceInterface = (
                container.permission_service()
            )
            try:
                for permission in all_permissions:
                    name = permission[0]
                    code = permission[1]

                    permission_service.create(
                        permission=PermissionCreateInputDto(
                            name=name, code=code
                        )
                    )
            except Exception:
                pass
