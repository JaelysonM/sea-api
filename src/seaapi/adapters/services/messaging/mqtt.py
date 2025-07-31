import asyncio
import json
import logging
from typing import Dict
import uuid

import paho.mqtt.client as mqtt

from src.seaapi.domain.ports.services.messaging import (
    MessagePublisherInterface,
    MessageConsumerInterface,
    Message,
    MessageHandlerInterface,
)
from src.seaapi.config.settings import settings

logger = logging.getLogger(__name__)


class MQTTPublisher(MessagePublisherInterface):
    def __init__(self):
        self.client_id = (
            f"sea-publisher-{uuid.uuid4().hex[:8]}"
        )
        self.client = None
        self.connected = False
        self._setup_client()

    def _setup_client(self):
        self.client = mqtt.Client(client_id=self.client_id)

        if (
            settings.MQTT_USERNAME
            and settings.MQTT_PASSWORD
        ):
            self.client.username_pw_set(
                settings.MQTT_USERNAME,
                settings.MQTT_PASSWORD,
            )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_publish = self._on_publish

    def _on_connect(
        self, client, userdata, flags, rc, properties=None
    ):
        if rc == 0:
            self.connected = True
            logger.info(
                "MQTT Publisher conectado: "
                f"{settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}"
            )
        else:
            self.connected = False
            logger.error(
                f"Falha na conexão MQTT Publisher. Código: {rc}"
            )

    def _on_disconnect(
        self, client, userdata, rc, properties=None
    ):
        self.connected = False
        logger.info("MQTT Publisher desconectado")

    def _on_publish(
        self, client, userdata, mid, properties=None
    ):
        logger.debug(f"Mensagem publicada com ID: {mid}")

    async def connect(self) -> None:
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                settings.MQTT_KEEPALIVE,
            )
            self.client.loop_start()

            attempts = 0
            while not self.connected and attempts < 10:
                await asyncio.sleep(0.5)
                attempts += 1

            if not self.connected:
                raise ConnectionError(
                    "Não foi possível conectar ao broker MQTT"
                )

        except Exception as e:
            logger.error(
                f"Erro ao conectar MQTT Publisher: {e}"
            )
            raise

    async def disconnect(self) -> None:
        if self.client and self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

    async def publish(self, message: Message) -> bool:
        if not self.connected:
            logger.warning(
                "MQTT Publisher desconectado. Tentando reconectar..."
            )
            try:
                await self.connect()
            except Exception as e:
                logger.error(f"Falha na reconexão: {e}")
                return False

        try:
            result = self.client.publish(
                topic=message.topic,
                payload=message.payload,
                qos=settings.MQTT_QOS,
                retain=message.retain
                or settings.MQTT_RETAIN,
            )

            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.info(
                    f"Mensagem publicada no tópico: {message.topic}"
                )
                return True
            else:
                logger.error(
                    f"Falha ao publicar mensagem. Código: {result.rc}"
                )
                return False

        except Exception as e:
            logger.error(f"Erro ao publicar mensagem: {e}")
            return False


class MQTTConsumer(MessageConsumerInterface):
    def __init__(self):
        self.client_id = (
            f"sea-consumer-{uuid.uuid4().hex[:8]}"
        )
        self.client = None
        self.connected = False
        self.handlers: Dict[
            str, MessageHandlerInterface
        ] = {}
        self._setup_client()

    def _setup_client(self):
        self.client = mqtt.Client(client_id=self.client_id)

        if (
            settings.MQTT_USERNAME
            and settings.MQTT_PASSWORD
        ):
            self.client.username_pw_set(
                settings.MQTT_USERNAME,
                settings.MQTT_PASSWORD,
            )

        self.client.on_connect = self._on_connect
        self.client.on_disconnect = self._on_disconnect
        self.client.on_message = self._on_message

    def _on_connect(
        self, client, userdata, flags, rc, properties=None
    ):
        if rc == 0:
            self.connected = True
            logger.info(
                "MQTT Consumer conectado: "
                f"{settings.MQTT_BROKER_HOST}:{settings.MQTT_BROKER_PORT}"
            )

            for topic in self.handlers.keys():
                self.client.subscribe(
                    topic, settings.MQTT_QOS
                )
                logger.info(
                    f"Re-subscrito ao tópico: {topic}"
                )
        else:
            self.connected = False
            logger.error(
                f"Falha na conexão MQTT Consumer. Código: {rc}"
            )

    def _on_disconnect(
        self, client, userdata, rc, properties=None
    ):
        self.connected = False
        logger.info("MQTT Consumer desconectado")

    def _on_message(self, client, userdata, msg):
        try:
            topic = msg.topic
            payload = json.loads(msg.payload.decode())
            message = Message(
                topic=topic,
                payload=payload.get("data", {}),
                message_id=payload.get("message_id"),
                correlation_id=payload.get(
                    "correlation_id"
                ),
                timestamp=payload.get("timestamp"),
                headers=payload.get("headers", {}),
            )

            handler = self.handlers.get(topic)
            if handler:
                try:
                    loop = asyncio.get_running_loop()
                except RuntimeError:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)

                future = asyncio.run_coroutine_threadsafe(
                    handler.handle(message), loop
                )
                future.add_done_callback(
                    lambda f: logger.error(
                        f"Erro no handler: {f.exception()}"
                    )
                    if f.exception()
                    else None
                )
            else:
                logger.warning(
                    f"Nenhum handler para tópico: {topic}"
                )

        except Exception as e:
            logger.error(
                f"Erro ao processar mensagem do tópico {msg.topic}: {e}"
            )

    async def connect(self) -> None:
        try:
            self.client.connect(
                settings.MQTT_BROKER_HOST,
                settings.MQTT_BROKER_PORT,
                settings.MQTT_KEEPALIVE,
            )
            self.client.loop_start()

            attempts = 0
            while not self.connected and attempts < 10:
                await asyncio.sleep(0.5)
                attempts += 1

            if not self.connected:
                raise ConnectionError(
                    "Não foi possível conectar ao broker MQTT"
                )

        except Exception as e:
            logger.error(
                f"Erro ao conectar MQTT Consumer: {e}"
            )
            raise

    async def disconnect(self) -> None:
        if self.client and self.connected:
            self.client.loop_stop()
            self.client.disconnect()
            self.connected = False

    async def subscribe(
        self, topic: str, handler: MessageHandlerInterface
    ) -> None:
        self.handlers[topic] = handler

        if self.connected:
            result = self.client.subscribe(
                topic, settings.MQTT_QOS
            )
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                logger.info(f"Subscrito ao tópico: {topic}")
            else:
                logger.error(
                    f"Falha ao subscrever tópico {topic}. Código: {result[0]}"
                )

    async def unsubscribe(self, topic: str) -> None:
        if topic in self.handlers:
            del self.handlers[topic]

        if self.connected:
            result = self.client.unsubscribe(topic)
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                logger.info(
                    f"Dessubscrito do tópico: {topic}"
                )
            else:
                logger.error(
                    f"Falha ao dessubscrever tópico {topic}. Código: {result[0]}"
                )

    async def start_consuming(self) -> None:
        if not self.connected:
            await self.connect()

        logger.info(
            "Iniciando consumo de mensagens MQTT..."
        )

        try:
            while self.connected:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            logger.info("Interrompido pelo usuário")
        finally:
            await self.stop_consuming()

    async def stop_consuming(self) -> None:
        logger.info("Parando consumo de mensagens MQTT...")
        await self.disconnect()
