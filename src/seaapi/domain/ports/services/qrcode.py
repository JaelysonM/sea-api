from abc import ABC, abstractmethod
from typing import Optional


class QRCodeGeneratorInterface(ABC):
    @abstractmethod
    def generate_qrcode(
        self,
        data: str,
        text: Optional[str] = None,
        size: Optional[int] = None,
        color: Optional[str] = None,
    ) -> bytes:
        raise NotImplementedError
