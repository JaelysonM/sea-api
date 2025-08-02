import logging
import json
from typing import Dict, Any

from src.seaapi.domain.ports.services.messaging import (
    EventBusInterface,
    MessagePublisherInterface,
    MessageConsumerInterface,
    MessageHandlerInterface,
    Message,
)
from src.seaapi.config.settings import settings

logger = logging.getLogger(__name__)


class EventBus(EventBusInterface):
    def __init__(
        self,
        publisher: MessagePublisherInterface,
        consumer: MessageConsumerInterface,
    ):
        self.publisher = publisher
        self.consumer = consumer
        self.handlers: Dict[
            str, MessageHandlerInterface
        ] = {}
        self.running = False

    def _get_topic_for_event(self, event_type: str) -> str:
        topic_parts = event_type.split(".")
        return f"{settings.MQTT_TOPIC_PREFIX}/{'/'.join(topic_parts)}"

    async def publish(
        self, event_type: str, data: Dict[str, Any]
    ) -> bool:
        if not settings.MESSAGING_ENABLED:
            logger.debug(
                "Mensageria desabilitada - evento não publicado"
            )
            return True

        if not self.publisher.connected:
            try:
                await self.publisher.connect()
            except Exception as e:
                logger.error(
                    f"Erro ao conectar publisher: {e}"
                )
                return False

        try:
            topic = self._get_topic_for_event(event_type)

            retain = data.pop(
                "retain", settings.MQTT_RETAIN
            )
            if len(data) == 0:
                data = ""
            else:
                data = json.dumps(data)
            message = Message(
                topic=topic,
                payload=data,
                retain=retain,
            )

            return await self.publisher.publish(message)

        except Exception as e:
            logger.error(
                f"Erro ao publicar evento {event_type}: {e}"
            )
            return False

    async def subscribe(
        self,
        event_type: str,
        handler: MessageHandlerInterface,
    ) -> None:
        topic = self._get_topic_for_event(event_type)
        self.handlers[event_type] = handler

        if self.running:
            await self.consumer.subscribe(topic, handler)

    async def start(self) -> None:
        if not settings.MESSAGING_ENABLED:
            logger.info(
                "Mensageria desabilitada - Event Bus não iniciado"
            )
            return

        try:
            await self.publisher.connect()
            if settings.IS_MESSAGE_WORKER:
                await self.consumer.connect()

                for (
                    event_type,
                    handler,
                ) in self.handlers.items():
                    topic = self._get_topic_for_event(
                        event_type
                    )
                    await self.consumer.subscribe(
                        topic, handler
                    )

            self.running = True
            logger.info("Event Bus iniciado com sucesso")

        except Exception as e:
            logger.error(f"Erro ao iniciar Event Bus: {e}")
            raise

    async def stop(self) -> None:
        if self.running:
            try:
                await self.consumer.stop_consuming()
                await self.publisher.disconnect()
                self.running = False
                logger.info("Event Bus parado")
            except Exception as e:
                logger.error(
                    f"Erro ao parar Event Bus: {e}"
                )

    async def start_consuming(self) -> None:
        if not self.running:
            await self.start()

        logger.info("Iniciando consumo de eventos...")
        await self.consumer.start_consuming()
