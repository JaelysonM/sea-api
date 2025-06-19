from src.seaapi.domain.ports.services.notification import (
    NotificationServiceInterface,
)
from src.seaapi.domain.shared.messages import Message


class FakeNotificationService(NotificationServiceInterface):
    async def send_notification(
        self, target, message: Message
    ):
        print("Sending notification to %s" % target)
        print(f"{message.subject}")
        print(f"{message.body}")
        print(message.subject)
