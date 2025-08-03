import abc
from src.seaapi.domain.dtos.nutrition import (
    NutritionCalculateInputDto,
    NutritionCalculateOutputDto,
)


class NutritionServiceInterface(abc.ABC):
    @abc.abstractmethod
    def calculate_nutrition(
        self, food_data: NutritionCalculateInputDto
    ) -> NutritionCalculateOutputDto:
        raise NotImplementedError
