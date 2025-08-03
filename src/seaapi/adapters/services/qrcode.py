import qrcode
import io
import os
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import (
    GappedSquareModuleDrawer,
)
from qrcode.image.styles.colormasks import (
    SolidFillColorMask,
)
from src.seaapi.domain.ports.services.qrcode import (
    QRCodeGeneratorInterface,
)
from src.seaapi.config.settings import root_path


class QRCodeGeneratorService(QRCodeGeneratorInterface):
    def __init__(self):
        self.box_size = 20
        self.border = 1
        self.fill_color = "#3D444A"
        self.back_color = "#FFFFFF"
        self.text_color = "#3A4A5C"
        self.font_size = 14
        self.logo_path = os.path.join(
            root_path, "assets", "images", "logo.png"
        )
        self.font_path = os.path.join(
            root_path, "assets", "fonts", "Lato-Bold.ttf"
        )

    def _load_logo_image(self) -> Optional[Image.Image]:
        try:
            if os.path.exists(self.logo_path):
                return Image.open(self.logo_path).convert(
                    "RGBA"
                )
        except Exception:
            pass
        return None

    def _load_font(self) -> ImageFont.FreeTypeFont:
        try:
            if os.path.exists(self.font_path):
                return ImageFont.truetype(
                    self.font_path, self.font_size
                )
        except Exception:
            pass
        return ImageFont.load_default()

    def hex_to_rgb(self, h):
        h = h.lstrip("#")
        return tuple(
            int(h[i : i + 2], 16)  # noqa: E203
            for i in (0, 2, 4)
        )

    def generate_qrcode(
        self,
        data: str,
        text: Optional[str] = None,
        size: Optional[int] = None,
        color: Optional[str] = None,
        target_size: Optional[int] = 1024,
        output_format: str = "PNG",
    ) -> bytes:
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=size or self.box_size,
            border=self.border,
        )
        qr.add_data(data)
        qr.make(fit=True)

        final_color = color or self.fill_color

        img_qr: Image.Image = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=GappedSquareModuleDrawer(),
            color_mask=SolidFillColorMask(
                front_color=self.hex_to_rgb(final_color),
                back_color=self.hex_to_rgb(self.back_color),
            ),
        ).convert("RGBA")

        qr_width, qr_height = img_qr.size
        logo = self._load_logo_image()

        if not logo:
            buf = io.BytesIO()
            img_qr.save(
                buf,
                format=output_format.upper(),
                optimize=True,
            )
            return buf.getvalue()

        logo_size = int(qr_width / 4)
        logo = logo.resize(
            (logo_size, logo_size), Image.Resampling.LANCZOS
        )

        padding = 20
        text_height = 0
        gap = 5
        font = self._load_font()
        if text:
            bbox = font.getbbox(text)
            text_height = bbox[3] - bbox[1]

        c_width = logo_size + padding * 2
        c_height = (
            logo_size
            + padding * 2
            + (text_height + gap if text else 0)
        )

        canvas = Image.new(
            "RGBA", (c_width, c_height), (0, 0, 0, 0)
        )
        draw = ImageDraw.Draw(canvas)
        draw.rounded_rectangle(
            (0, 0, c_width, c_height),
            radius=15,
            fill="white",
        )

        x_logo = (c_width - logo_size) // 2
        canvas.paste(logo, (x_logo, padding), logo)

        if text:
            draw_point = (
                c_width / 2,
                padding + logo_size + gap,
            )
            draw.text(
                draw_point,
                text,
                font=font,
                fill=self.text_color,
                anchor="mt",
            )

        pos = (
            (qr_width - c_width) // 2,
            (qr_height - c_height) // 2,
        )
        img_qr.paste(canvas, pos, canvas)

        if target_size and isinstance(target_size, int):
            img_qr = img_qr.resize(
                (target_size, target_size),
                Image.Resampling.LANCZOS,
            )

        buf = io.BytesIO()
        img_qr.save(
            buf, format=output_format.upper(), optimize=True
        )
        return buf.getvalue()
