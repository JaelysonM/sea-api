from pydantic import BaseModel


class NutritionCalculateInputDto(BaseModel):
    food_name: str


class NutritionCalculateOutputDto(BaseModel):
    protein_g: float
    carbohydrates_total_g: float
    fat_total_g: float
