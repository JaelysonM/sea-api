#!/usr/bin/env python3

import asyncio
import logging
import signal
import sys
from pathlib import Path


from src.seaapi.config.containers import Container
from src.seaapi.adapters.entrypoints.messaging.handlers.registry import (
    HandlerRegistry,
)
from src.seaapi.adapters.db.orm import (
    start_mappers,
)

sys.path.append(
    str(Path(__file__).parent.parent.parent.parent.parent)
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("MessagingWorker")


class MessagingWorker:
    def __init__(self):
        self.container = Container()
        self.event_bus = None
        self.running = False
        self.shutdown_event = None

    async def setup_handlers(self):
        logger.info("Configurando handlers de eventos...")

        handlers_config = HandlerRegistry.get_handlers()

        if not handlers_config:
            logger.warning(
                "Nenhum handler registrado encontrado!"
            )
            return

        for event_type, handler_class in handlers_config:
            handler = handler_class(self.container)
            await self.event_bus.subscribe(
                event_type, handler
            )

        logger.info("Handlers configurados:")
        for event_type, handler_class in handlers_config:
            logger.info(
                f"  - {event_type} -> {handler_class.__name__}"
            )

    async def start(self):
        logger.info("Iniciando Messaging Worker...")

        try:
            # Criar evento de shutdown no loop correto
            self.shutdown_event = asyncio.Event()

            self.event_bus = self.container.event_bus()

            await self.setup_handlers()

            await self.event_bus.start()

            self.running = True
            logger.info(
                "✅ Messaging Worker iniciado com sucesso!"
            )

            # Iniciar consumo em background
            consume_task = asyncio.create_task(
                self.event_bus.start_consuming()
            )

            await self.shutdown_event.wait()

            consume_task.cancel()
            try:
                await consume_task
            except asyncio.CancelledError:
                pass

        except Exception as e:
            logger.error(f"❌ Erro ao iniciar worker: {e}")
            raise

    async def stop(self):
        if self.running:
            logger.info("Parando Messaging Worker...")

            if self.event_bus:
                await self.event_bus.stop()

            self.running = False
            self.shutdown_event.set()
            logger.info("✅ Messaging Worker parado")

    def handle_signal(self, signum, frame):
        logger.info(
            f"Recebido sinal {signum}. Parando worker..."
        )
        if self.shutdown_event:
            # Usar call_soon_threadsafe para ser thread-safe
            loop = asyncio.get_event_loop()
            loop.call_soon_threadsafe(
                self.shutdown_event.set
            )


async def main():
    worker = MessagingWorker()

    # Configurar handlers de sinal
    signal.signal(signal.SIGINT, worker.handle_signal)
    signal.signal(signal.SIGTERM, worker.handle_signal)

    try:
        start_mappers()
        await worker.start()
    except KeyboardInterrupt:
        logger.info("Worker interrompido pelo usuário")
    except Exception as e:
        logger.error(f"Erro no worker: {e}")
        return 1
    finally:
        await worker.stop()

    return 0


if __name__ == "__main__":
    try:
        exit_code = asyncio.run(main())
        sys.exit(exit_code)
    except KeyboardInterrupt:
        logger.info("Worker finalizado")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro fatal: {e}")
        sys.exit(1)
