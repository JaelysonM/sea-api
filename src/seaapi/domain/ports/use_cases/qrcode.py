from abc import ABC, abstractmethod
from src.seaapi.domain.dtos.qrcode import (
    QRCodeCreateInputDto,
    QRCodeTokenDto,
    QRCodeInfoResponseDto,
)
from src.seaapi.domain.dtos.mics import SuccessResponse
from src.seaapi.domain.dtos.tokens import Tokens


class QRCodeServiceInterface(ABC):
    @abstractmethod
    def create_qrcode_token(
        self, data: QRCodeCreateInputDto
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def regenerate_qrcode(
        self, token_id: int, frontend_url: str
    ) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def authenticate_with_qrcode(
        self, data: QRCodeTokenDto
    ) -> Tokens:
        raise NotImplementedError

    @abstractmethod
    def get_qrcode_info(
        self, token_id: int
    ) -> QRCodeInfoResponseDto:
        raise NotImplementedError

    @abstractmethod
    def revoke_token(
        self, token_id: int
    ) -> SuccessResponse:
        raise NotImplementedError
