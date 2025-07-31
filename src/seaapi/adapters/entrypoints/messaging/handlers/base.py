import logging
import uuid
from abc import abstractmethod

from src.seaapi.domain.ports.services.messaging import (
    MessageHandlerInterface,
    Message,
)
from src.seaapi.config.containers import Container


logger = logging.getLogger(__name__)


class BaseMessageHandler(MessageHandlerInterface):
    def __init__(self, container: Container):
        self.container = container

    async def handle(self, message: Message) -> None:
        try:
            if not message.message_id:
                message.message_id = str(uuid.uuid4())

            logger.info(
                f"Processando mensagem do tópico: {message.topic}"
            )
            await self.process_message(message)
            logger.info(
                f"Mensagem processada com sucesso: {message.message_id}"
            )
        except Exception as e:
            logger.error(f"Erro ao processar mensagem: {e}")
            await self.handle_error(message, e)

    @abstractmethod
    async def process_message(
        self, message: Message
    ) -> None:
        """Processa a mensagem (deve ser implementado pelas subclasses)"""
        raise NotImplementedError

    async def handle_error(
        self, message: Message, error: Exception
    ) -> None:
        """Trata erros durante o processamento"""
        logger.error(
            f"Erro no handler {self.__class__.__name__}: {error}"
        )
        logger.error(
            f"Erro não tratado para mensagem {message.message_id}: {error}"
        )
