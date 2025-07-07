import qrcode
import io
from typing import Optional
from src.seaapi.domain.ports.services.qrcode import (
    QRCodeGeneratorInterface,
)


class QRCodeService(QRCodeGeneratorInterface):
    def __init__(self):
        self.box_size = 10
        self.border = 4

    def generate_qrcode(
        self, data: str, size: Optional[int] = None
    ) -> bytes:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=size or self.box_size,
            border=self.border,
        )

        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(
            fill_color="black", back_color="white"
        )

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")

        return buffer.getvalue()
