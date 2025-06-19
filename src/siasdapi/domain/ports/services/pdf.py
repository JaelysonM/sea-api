from abc import ABC, abstractmethod
from src.siasdapi.domain.shared.documents import (
    Document,
)


class PDFGeneratorService(ABC):
    @abstractmethod
    async def generate(self, document: Document) -> bytes:
        pass
