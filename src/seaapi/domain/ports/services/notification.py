from abc import ABC, abstractmethod
from src.seaapi.domain.shared.messages import (
    Message,
)


class NotificationServiceInterface(ABC):
    @abstractmethod
    async def send_notification(
        self, target, message: Message
    ):
        raise NotImplementedError
