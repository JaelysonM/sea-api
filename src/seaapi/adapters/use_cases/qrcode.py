import secrets
from datetime import datetime, timedelta
from src.seaapi.domain.dtos.qrcode import (
    QRCodeCreateInputDto,
    QRCodeTokenDto,
    QRCodeInfoResponseDto,
)
from src.seaapi.domain.dtos.tokens import (
    TokenCreateInputDto,
    Tokens,
)
from src.seaapi.domain.dtos.mics import SuccessResponse
from src.seaapi.domain.ports.use_cases.qrcode import (
    QRCodeServiceInterface,
)
from src.seaapi.domain.ports.use_cases.tokens import (
    TokenServiceInterface,
)
from src.seaapi.domain.ports.use_cases.users import (
    UserServiceInterface,
)
from src.seaapi.domain.ports.unit_of_works.tokens import (
    TokenUnitOfWorkInterface,
)
from src.seaapi.domain.ports.shared.exceptions import (
    UserNotFoundException,
    ExpiredTokenException,
    InvalidCredentialsException,
    QRCodeGenerationException,
)
from src.seaapi.domain.ports.services.qrcode import (
    QRCodeGeneratorInterface,
)
from src.seaapi.config.settings import settings


class QRCodeService(QRCodeServiceInterface):
    def __init__(
        self,
        token_uow: TokenUnitOfWorkInterface,
        token_service: TokenServiceInterface,
        user_service: UserServiceInterface,
        qrcode_generator: QRCodeGeneratorInterface,
    ):
        self.token_uow = token_uow
        self.token_service = token_service
        self.user_service = user_service
        self.qrcode_generator = qrcode_generator

    def _generate_qrcode_token(self) -> str:
        return secrets.token_urlsafe(32)

    def _get_qrcode_expiration(self) -> datetime:
        return datetime.now() + timedelta(
            minutes=getattr(
                settings,
                "QRCODE_TOKEN_EXPIRE_MINUTES",
                20000000,
            )
        )

    def _create_qrcode_token(
        self, data: QRCodeCreateInputDto
    ) -> bytes:
        user = self.user_service.get_user(
            data.user_id, entity=True
        )

        if not user.can_generate_qrcode():
            raise InvalidCredentialsException(
                "Usuário não pode gerar QRCode"
            )

        token_value = self._generate_qrcode_token()
        expiration = self._get_qrcode_expiration()

        token_input = TokenCreateInputDto(
            type="fast_auth",
            token=token_value,
            expiration=expiration,
            reference=data.user_id,
        )

        self.token_service.create(token=token_input)

        qrcode_url = (
            f"{data.frontend_url}?token={token_value}"
        )
        try:
            qrcode_data = self.qrcode_generator.generate_qrcode(
                data=qrcode_url,
                text=f"{user.first_name} {user.last_name} (ID: {user.id})",
            )
        except Exception as e:
            raise QRCodeGenerationException(
                f"Erro ao gerar QRCode: {str(e)}"
            )

        return qrcode_data

    def _regenerate_qrcode(
        self, token_id: int, frontend_url: str
    ) -> bytes:
        with self.token_uow:
            token = self.token_uow.tokens.find_by_id(
                token_id
            )
            if not token or token.type != "fast_auth":
                raise InvalidCredentialsException(
                    "Token não encontrado"
                )
            if token.expiration < datetime.now():
                raise ExpiredTokenException(
                    "Token expirado"
                )

            qrcode_url = (
                f"{frontend_url}?token={token.token}"
            )

            user = self.user_service.get_user(
                token.reference, entity=True
            )

            try:
                qrcode_data = self.qrcode_generator.generate_qrcode(
                    qrcode_url,
                    text=f"{user.first_name} {user.last_name} (ID: {user.id})",
                )
            except Exception as e:
                raise QRCodeGenerationException(
                    f"Erro ao gerar QRCode: {str(e)}"
                )

            return qrcode_data

    def _authenticate_with_qrcode(
        self, data: QRCodeTokenDto
    ) -> Tokens:
        with self.token_uow:
            token = self.token_uow.tokens.find_by_token_and_type(
                token=data.token, type="fast_auth"
            )

            if not token:
                raise InvalidCredentialsException(
                    "Token QRCode inválido"
                )

            if token.expiration < datetime.now():
                self.token_service.delete(token)
                raise ExpiredTokenException(
                    "Token QRCode expirado"
                )

            try:
                user = self.user_service.get_user(
                    token.reference, entity=True
                )
            except Exception:
                raise UserNotFoundException()

            tokens, expiration = user.authenticate_qrcode()
            _, refresh_token_expiration = expiration

            refresh_token_input = TokenCreateInputDto(
                type="refresh",
                token=tokens.refresh_token,
                expiration=refresh_token_expiration,
                reference=user.id,
            )

            self.token_service.create(
                token=refresh_token_input
            )

            return tokens

    def _get_qrcode_info(
        self, token_id: int
    ) -> QRCodeInfoResponseDto:
        with self.token_uow:
            token = self.token_uow.tokens.find_by_id(
                token_id
            )
            if not token or token.type != "fast_auth":
                raise InvalidCredentialsException(
                    "Token QRCode não encontrado"
                )

            return QRCodeInfoResponseDto(
                token_id=token.id,
                user_id=token.reference,
                expires_at=token.expiration.isoformat(),
                qr_generated_at=token.created_at.isoformat(),
                is_expired=token.expiration
                < datetime.now(),
            )

    def _revoke_token(
        self, token_id: int
    ) -> SuccessResponse:
        with self.token_uow:
            token = self.token_uow.tokens.find_by_id(
                token_id
            )
            if not token or token.type != "fast_auth":
                raise InvalidCredentialsException(
                    "Token QRCode não encontrado"
                )

            self.token_service.delete(token)

            return SuccessResponse(
                message="Token QRCode revogado com sucesso",
                code="qrcode_revoked",
            )

    def _get_plate_qrcode(self, serial: str) -> bytes:
        if not all(c.isalnum() or c == "-" for c in serial):
            raise QRCodeGenerationException(
                "Serial inválido"
            )
        try:
            qrcode_data = (
                self.qrcode_generator.generate_qrcode(
                    data=serial,
                    text=f"{serial}",
                )
            )
        except Exception as e:
            raise QRCodeGenerationException(
                f"Erro ao gerar QRCode do prato: {str(e)}"
            )
        return qrcode_data
