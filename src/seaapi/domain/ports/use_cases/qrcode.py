from abc import ABC, abstractmethod
from src.seaapi.domain.dtos.qrcode import (
    QRCodeCreateInputDto,
    QRCodeTokenDto,
    QRCodeInfoResponseDto,
)
from src.seaapi.domain.dtos.mics import SuccessResponse
from src.seaapi.domain.dtos.tokens import Tokens


class QRCodeServiceInterface(ABC):
    def create_qrcode_token(
        self, data: QRCodeCreateInputDto
    ) -> bytes:
        return self._create_qrcode_token(data)

    def regenerate_qrcode(
        self, token_id: int, frontend_url: str
    ) -> bytes:
        return self._regenerate_qrcode(
            token_id, frontend_url
        )

    def authenticate_with_qrcode(
        self, data: QRCodeTokenDto
    ) -> Tokens:
        return self._authenticate_with_qrcode(data)

    def get_qrcode_info(
        self, token_id: int
    ) -> QRCodeInfoResponseDto:
        return self._get_qrcode_info(token_id)

    def revoke_token(
        self, token_id: int
    ) -> SuccessResponse:
        return self._revoke_token(token_id)

    def get_plate_qrcode(self, serial: str) -> bytes:
        return self._get_plate_qrcode(serial)

    @abstractmethod
    def _create_qrcode_token(
        self, data: QRCodeCreateInputDto
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def _regenerate_qrcode(
        self, token_id: int, frontend_url: str
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def _authenticate_with_qrcode(
        self, data: QRCodeTokenDto
    ) -> Tokens:
        raise NotImplementedError

    @abstractmethod
    def _get_qrcode_info(
        self, token_id: int
    ) -> QRCodeInfoResponseDto:
        raise NotImplementedError

    @abstractmethod
    def _revoke_token(
        self, token_id: int
    ) -> SuccessResponse:
        raise NotImplementedError

    @abstractmethod
    def _get_plate_qrcode(self, serial: str) -> bytes:
        raise NotImplementedError
