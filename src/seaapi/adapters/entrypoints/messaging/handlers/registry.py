from typing import Dict, Type, List, Tuple
from src.seaapi.adapters.entrypoints.messaging.handlers.base import (
    BaseMessageHandler,
)


class HandlerRegistry:

    _handlers: Dict[str, Type[BaseMessageHandler]] = {}

    @classmethod
    def register(cls, event_type: str):

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
        return list(cls._handlers.items())

    @classmethod
    def get_handler(
        cls, event_type: str
    ) -> Type[BaseMessageHandler]:
        return cls._handlers.get(event_type)

    @classmethod
    def clear(cls):
        cls._handlers.clear()


handler = HandlerRegistry.register
