from abc import abstractmethod
import hashlib
import six
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from time import time
from jose import jwt
from src.seaapi.config import settings


class TokenGenerator:
    def __init__(self, secret_key):
        self.secret_key = secret_key

    @abstractmethod
    def _make_hash_value(self, payload, timestamp):
        pass

    def make_token(
        self,
        payload,
        timestamp=int(time()),
        expiration=3600,
    ):
        value = self._make_hash_value(payload, timestamp)
        return (
            "{0}:{1}".format(
                hashlib.sha256(
                    (value + self.secret_key).encode()
                ).hexdigest(),
                timestamp,
            ),
            timestamp + (expiration * 60 * 1000),
        )

    def check_token(self, payload, token, expiration=3600):
        try:
            timestamp = token.split(":")[1]
            timestamp = int(timestamp)
            if time() - timestamp <= (
                expiration * 60 * 1000
            ):
                expected_token, _ = self.make_token(
                    payload, timestamp=timestamp
                )
                return secrets.compare_digest(
                    token, expected_token
                )
        except (ValueError, TypeError):  # pragma: no cover
            pass
        return False  # pragma: no cover


class PasswordResetTokenGenerator(TokenGenerator):
    def _make_hash_value(self, payload, timestamp):
        return (
            six.text_type(payload.password)
            + six.text_type(payload.id)
            + six.text_type(timestamp)
        )

    def make_token(
        self,
        payload,
        timestamp=int(time()),
        expiration=settings.FORGOT_PASSWORD_TOKEN_DURATION,
    ):
        return super().make_token(
            payload, timestamp, expiration
        )

    def check_token(
        self,
        payload,
        token,
        expiration=settings.FORGOT_PASSWORD_TOKEN_DURATION,
    ):
        return super().check_token(
            payload, token, expiration
        )


def create_token(
    data: dict,
    type: str = "access",
    expires_delta: Optional[timedelta] = None,
):
    expirations = {
        "access": settings.ACCESS_TOKEN_EXPIRE_MINUTES,
        "refresh": settings.REFRESH_TOKEN_EXPIRE_MINUTES,
    }
    to_encode = data.copy()
    if expires_delta:  # pragma: no cover
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=expirations[type]
        )

    to_encode["exp"] = expire
    to_encode["type"] = type
    return encode_jwt(to_encode), expire


def encode_jwt(data: dict):
    return jwt.encode(
        data,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


def decode_jwt(token: str):
    decoded_token = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )
    return (
        decoded_token
        if decoded_token["exp"] >= time()
        else None
    )


password_reset_token_generator = (
    PasswordResetTokenGenerator(
        secret_key=settings.SECRET_KEY
    )
)
