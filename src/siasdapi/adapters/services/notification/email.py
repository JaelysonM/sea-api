from src.siasdapi.domain.ports.services.notification import (
    NotificationServiceInterface,
)
from src.siasdapi.config.settings import settings
from src.siasdapi.domain.shared.messages import Message

from fastapi_mail import (
    FastMail,
    MessageSchema,
    ConnectionConfig,
)


class EmailNotificationService(
    NotificationServiceInterface
):
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USER,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_FROM,
            MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
            MAIL_PORT=settings.MAIL_PORT,
            MAIL_SERVER=settings.MAIL_SERVER,
            MAIL_STARTTLS=False,
            MAIL_SSL_TLS=True,
            USE_CREDENTIALS=True,
            TEMPLATE_FOLDER="assets/templates",
        )

        self.instance = FastMail(self.conf)

    async def send_notification(
        self, target, message: Message
    ):
        mail_message = MessageSchema(
            subject=message.subject,
            recipients=[target],
            template_body=message.body,
            subtype="html",
        )
        await self.instance.send_message(
            mail_message, template_name=message.template
        )
