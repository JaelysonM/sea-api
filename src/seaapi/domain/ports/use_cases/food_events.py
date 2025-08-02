import abc
from src.seaapi.domain.entities import FoodEntity


class FoodEventPublisherInterface(abc.ABC):
    async def publish_food_scale_event(
        self, event_type: str, food: FoodEntity
    ):
        return await self._publish_food_scale_event(
            event_type, food
        )

    async def publish_food_scale_event_with_serial(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        return await self._publish_food_scale_event_with_serial(
            event_type, food, scale_serial
        )

    async def publish_to_scale_topic(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        return await self._publish_to_scale_topic(
            event_type, food, scale_serial
        )

    @abc.abstractmethod
    async def _publish_food_scale_event(
        self, event_type: str, food: FoodEntity
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _publish_food_scale_event_with_serial(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        raise NotImplementedError

    @abc.abstractmethod
    async def _publish_to_scale_topic(
        self,
        event_type: str,
        food: FoodEntity,
        scale_serial: str,
    ):
        raise NotImplementedError
