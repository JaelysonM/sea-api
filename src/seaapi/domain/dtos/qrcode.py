from pydantic import BaseModel


class QRCodeCreateInputDto(BaseModel):
    user_id: int
    frontend_url: str


class QRCodeRegenerateInputDto(BaseModel):
    frontend_url: str


class QRCodeTokenDto(BaseModel):
    token: str


class QRCodeInfoResponseDto(BaseModel):
    token_id: int
    user_id: int
    expires_at: str
    qr_generated_at: str
    is_expired: bool


class QRCodePlateInputDto(BaseModel):
    plate_id: int
