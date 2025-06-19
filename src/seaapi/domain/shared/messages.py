from src.seaapi.config.settings import settings


class Message:
    subject = ""
    body = None
    template = None


class ForgotPasswordMessage(Message):
    subject = f"{settings.MARKETING_NAME} {settings.COMPANY_NAME} - Recuperação de senha"
    template = "forgot_password.html"

    def __init__(self, link):
        self.body = {"link": link}
