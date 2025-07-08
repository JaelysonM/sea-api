from typing import Dict, Type, List, Tuple
from src.seaapi.adapters.entrypoints.messaging.handlers.base import (
    BaseMessageHandler,
)


class HandlerRegistry:
    """Registry para handlers de mensageria com auto-descoberta"""

    _handlers: Dict[str, Type[BaseMessageHandler]] = {}

    @classmethod
    def register(cls, event_type: str):
        """Decorator para registrar handlers automaticamente"""

        def decorator(
            handler_class: Type[BaseMessageHandler],
        ):
            cls._handlers[event_type] = handler_class
            return handler_class

        return decorator

    @classmethod
    def get_handlers(
        cls,
    ) -> List[Tuple[str, Type[BaseMessageHandler]]]:
        """Retorna lista de handlers registrados"""
        return list(cls._handlers.items())

    @classmethod
    def get_handler(
        cls, event_type: str
    ) -> Type[BaseMessageHandler]:
        """Retorna handler específico para um evento"""
        return cls._handlers.get(event_type)

    @classmethod
    def clear(cls):
        """Limpa registry (útil para testes)"""
        cls._handlers.clear()


# Alias para facilitar o uso
handler = HandlerRegistry.register
