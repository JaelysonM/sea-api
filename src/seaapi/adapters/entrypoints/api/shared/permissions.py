from fastapi import (
    Request,
)
from src.seaapi.domain.ports.shared.exceptions import (
    NotAuthorizedException,
    NotAuthenticatedException,
)
from starlette.authentication import (
    UnauthenticatedUser,
)
from src.seaapi.domain.entities import (
    UserEntity,
)
from src.seaapi.domain import Role


class BasePermission:
    raise_error = NotAuthorizedException()

    def check_permission(self, request: Request):
        raise NotImplementedError


class And(BasePermission):
    def __init__(self, permissions):
        self.permissions = permissions

    def check_permission(self, request: Request):
        for permission in self.permissions:
            if not permission.check_permission(request):
                raise permission.raise_error
        return True


class Or(BasePermission):
    def __init__(self, permissions):
        self.permissions = permissions

    def check_permission(self, request: Request):
        permissions_denied = []
        for permission in self.permissions:
            if not permission.check_permission(request):
                permissions_denied.append(
                    permission.raise_error
                )
        if len(permissions_denied) != len(self.permissions):
            return True
        else:
            for error in permissions_denied:
                raise error


class PermissionsDependency:
    def __init__(self, permission: BasePermission):
        self.permission = permission

    async def __call__(self, request: Request):
        if not self.permission.check_permission(request):
            raise self.permission.raise_error


class IsAuthenticated(BasePermission):
    raise_error = NotAuthenticatedException()

    def check_permission(self, request: Request):
        if request.user is None or isinstance(
            request.user, UnauthenticatedUser
        ):
            return False
        return True


class HasObjectPermission(BasePermission):
    action = "all"

    def __init__(self, resource):
        self.resource = resource

    def check_permission(self, request: Request):
        user: UserEntity = request.user

        return user.has_permission(
            f"{self.action}_{self.resource}"
        )


class HasObjectDeletePermission(HasObjectPermission):
    action = "delete"


class HasObjectReadPermission(HasObjectPermission):
    action = "read"


class HasObjectEditPermission(HasObjectPermission):
    action = "edit"


class HasObjectCreatePermission(HasObjectPermission):
    action = "create"


class IsAdministrator(IsAuthenticated):

    raise_error = NotAuthorizedException(
        "Você precisa ser administrador para acessar/usar este recurso"
    )

    def check_permission(self, request: Request):
        is_authenticated = super().check_permission(request)
        user = request.user
        return is_authenticated and user.has_role(
            Role.ADMIN
        )


class IsCustomer(IsAuthenticated):
    raise_error = NotAuthorizedException(
        "Você precisa ser pelo menos um cliente para acessar/usar este recurso"
    )

    def check_permission(self, request: Request):
        is_authenticated = super().check_permission(request)
        user = request.user
        return is_authenticated and user.has_role(
            Role.CUSTOMER
        )


class IsSuperuser(IsAuthenticated):
    raise_error = NotAuthorizedException(
        "Você precisa  ser pelo menos um super-usário acessar/usar este recurso"
    )

    def check_permission(self, request: Request):
        is_authenticated = super().check_permission(request)
        user = request.user
        return is_authenticated and user.has_role(
            Role.SUPERUSER
        )
