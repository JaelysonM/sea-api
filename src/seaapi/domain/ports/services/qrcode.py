from abc import ABC, abstractmethod
from typing import Optional


class QRCodeGeneratorInterface(ABC):
    @abstractmethod
    def generate_qrcode(
        self, data: str, size: Optional[int] = None
    ) -> bytes:
        raise NotImplementedError
