import logging

from src.seaapi.domain.dtos.meals import (
    FoodMeasurementCreateInputDto,
    MealCreateInputDto,
)
from src.seaapi.domain.ports.services.messaging import (
    Message,
)
from src.seaapi.adapters.entrypoints.messaging.handlers.base import (
    BaseMessageHandler,
)
from src.seaapi.adapters.entrypoints.messaging.handlers.registry import (
    handler,
)

logger = logging.getLogger(__name__)


@handler("meal.events")
class MealEventHandler(BaseMessageHandler):
    async def process_message(
        self, message: Message
    ) -> None:
        payload = message.payload
        event_type = payload.get("event_type")

        if not event_type:
            logger.error("Campo 'event_type' ausente na mensagem")
            return

        if event_type == "meal.finished":
            await self._handle_finished(payload)
        elif event_type == "meal.initialize":
            await self._handle_initialize(payload)
        elif event_type == "meal.add_food":
            await self._handle_add_food(payload)
        else:
            logger.warning(f"Tipo de evento desconhecido: {event_type}")

    async def _handle_finished(self, payload: dict) -> None:
        meal_id = payload.get("meal_id")
        if not meal_id:
            logger.error("Dados insuficientes para 'meal.finished'")
            return

        logger.info(f"Processando finalização de refeição: {meal_id}")
        self.container.meal_service().finish_meal(id_=meal_id)

    async def _handle_initialize(self, payload: dict) -> None:
        user_id = payload.get("user_id")
        if not user_id:
            logger.error("Dados insuficientes para 'meal.initialize'")
            return

        logger.info(f"Abrindo refeição para o usuário: {user_id}")
        self.container.meal_service().initialize_meal(
            MealCreateInputDto(user_identifier=user_id)
        )

    async def _handle_add_food(self, payload: dict) -> None:
        serial = payload.get("serial")
        weight = payload.get("weight")
        meal_id = payload.get("meal_id")
        if not (serial and weight and meal_id):
            logger.error("Dados insuficientes para 'meal.add_food'")
            return

        logger.info(f"Adicionando alimento à refeição: {meal_id}")
        self.container.meal_service().add_meal_food_measurement(
            id=meal_id,
            food_measurement=FoodMeasurementCreateInputDto(
                serial=serial,
                weight=weight,
            ),
        )
