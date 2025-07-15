import logging

from src.seaapi.domain.dtos.meals import (
    FoodMeasurementCreateInputDto,
    MealFinishInputDto,
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
            logger.error(
                "Campo 'event_type' ausente na mensagem"
            )
            return

        if event_type == "meal.finished":
            await self._handle_finished(payload)
        elif event_type == "meal.add_food":
            await self._handle_add_food(payload)
        else:
            logger.warning(
                f"Tipo de evento desconhecido: {event_type}"
            )

    async def _handle_finished(self, payload: dict) -> None:
        plate_identifier = payload.get("plate_identifier")
        if not plate_identifier:
            logger.error(
                "Dados insuficientes para 'meal.finished'"
            )
            return

        logger.info(
            f"Processando finalização de refeição para o prato: {plate_identifier}"
        )
        self.container.meal_service().finish_meal(
            finish_meal=MealFinishInputDto(
                plate_identifier=plate_identifier
            )
        )

    async def _handle_add_food(self, payload: dict) -> None:
        serial = payload.get("serial")
        weight = payload.get("weight")
        meal_id = payload.get("meal_id")
        if not (serial and weight and meal_id):
            logger.error(
                "Dados insuficientes para 'meal.add_food'"
            )
            return

        logger.info(
            f"Adicionando alimento à refeição: {meal_id}"
        )
        self.container.meal_service().add_meal_food_measurement(
            id=meal_id,
            food_measurement=FoodMeasurementCreateInputDto(
                serial=serial,
                weight=weight,
            ),
        )
