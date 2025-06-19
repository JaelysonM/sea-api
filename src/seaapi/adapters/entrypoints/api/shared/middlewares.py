from fastapi import Request, UploadFile, File
from starlette.middleware.authentication import (
    AuthenticationBackend,
)
from jose import JWTError
from src.seaapi.domain.shared.security import decode_jwt
from src.seaapi.domain.ports.shared.exceptions import (
    ExpiredTokenException,
)
from src.seaapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)
from src.seaapi.domain.entities import UserEntity
from src.seaapi.domain.shared.validators import (
    VideoFile,
)


class BearerTokenAuthBackend(AuthenticationBackend):
    async def authenticate(self, request: Request):
        if "Authorization" not in request.headers:
            return

        auth = request.headers["Authorization"]
        try:
            scheme, token = auth.split()
            if scheme != "Bearer" or not self.verify_jwt(
                token
            ):  # pragma: no cover
                raise ExpiredTokenException()

        except Exception:  # pragma: no cover
            raise ExpiredTokenException()

        container = request.app.container

        user_service: UserServiceInterface = (
            container.user_service()
        )
        user_id = self.payload.get("user_id", 0)

        user = user_service.get_user(
            id_=user_id, entity=True
        )

        return auth, user

    def verify_jwt(
        self, token: str, token_type: str = "access"
    ) -> bool:
        try:
            self.payload = decode_jwt(token)
        except JWTError:
            self.payload = None
        if not self.payload:
            return False

        return self.payload.get("type", "") == token_type


def get_user(
    request: Request,
) -> UserEntity:
    return request.user


def validate_video(
    file: UploadFile,
) -> UserEntity:
    VideoFile(file=file.filename)
    return file


def validate_optional_video(
    file: UploadFile = File(None),
) -> UserEntity:
    if file is None:
        return None
    VideoFile(file=file.filename)
    return file
