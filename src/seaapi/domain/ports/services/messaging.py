from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Message:

    topic: str
    payload: Dict[str, Any]
    message_id: Optional[str] = None
    correlation_id: Optional[str] = None
    timestamp: Optional[str] = None
    headers: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()


class MessageHandlerInterface(ABC):
    @abstractmethod
    async def handle(self, message: Message) -> None:
        raise NotImplementedError


class MessagePublisherInterface(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def publish(self, message: Message) -> bool:
        raise NotImplementedError


class MessageConsumerInterface(ABC):
    @abstractmethod
    async def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def disconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def subscribe(
        self, topic: str, handler: MessageHandlerInterface
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def unsubscribe(self, topic: str) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start_consuming(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop_consuming(self) -> None:
        raise NotImplementedError


class EventBusInterface(ABC):
    @abstractmethod
    async def publish(
        self, event_type: str, data: Dict[str, Any]
    ) -> bool:
        raise NotImplementedError

    @abstractmethod
    async def subscribe(
        self,
        event_type: str,
        handler: MessageHandlerInterface,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    async def start(self) -> None:
        raise NotImplementedError

    @abstractmethod
    async def stop(self) -> None:
        raise NotImplementedError
