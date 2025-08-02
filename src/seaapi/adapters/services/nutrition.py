import json
import logging
import aiohttp
from src.seaapi.domain.ports.services.nutrition import (
    NutritionServiceInterface,
)
from src.seaapi.domain.dtos.nutrition import (
    NutritionCalculateInputDto,
    NutritionCalculateOutputDto,
)

logger = logging.getLogger(__name__)


class OpenAINutritionService(NutritionServiceInterface):
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = (
            "https://api.openai.com/v1/chat/completions"
        )
        self.system_prompt = """
Você é um assistente de nutrição especializado.
Sua única função é retornar os macronutrientes aproximados de um alimento "
"ou prato, considerando uma porção padrão de 100g.

Regras obrigatórias:
1. Responda SOMENTE com o JSON (sem explicação, sem markdown).
2. O formato exato deve ser:
{
  "protein_g": <float>,
  "carbohydrates_g": <float>,
  "fat_g": <float>
}
3. Use apenas números com 1 casa decimal, com ponto como separador decimal (ex: 12.3).

Regras para interpretação:
- Se o alimento for uma receita ou prato regional (como "pizza de rapadura""
" ou "bolo de rolo"), estime os ingredientes típicos e calcule os
 macros aproximados com base neles.
- Use dados nutricionais confiáveis (USDA, TACO, fontes científicas).
- Não invente ou varie a estrutura do JSON. Não adicione unidades nem explicações.
- Se o nome for genérico ou impossível de estimar, retorne:
  {
    "protein_g": 0.0,
    "carbohydrates_g": 0.0,
    "fat_g": 0.0
  }

Exemplos:
- "bolo de cenoura com cobertura de chocolate" → usar estimativa com cenoura,
 farinha, óleo, ovo, açúcar, chocolate
- "pizza de rapadura" → estimar como massa de pizza tradicional + cobertura de
 rapadura derretida + (opcional) queijo coalho

Seu foco é praticidade e aproximação realista, não perfeição.
"""

    async def calculate_nutrition(
        self, food_data: NutritionCalculateInputDto
    ) -> NutritionCalculateOutputDto:
        name = (food_data.food_name or "").strip()
        if not name:
            return self._default_response()

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        payload = {
            "model": "gpt-4-turbo",
            "messages": [
                {
                    "role": "system",
                    "content": self.system_prompt,
                },
                {"role": "user", "content": name},
            ],
            "temperature": 0,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.api_url,
                    headers=headers,
                    json=payload,
                ) as response:
                    if not response.ok:
                        logger.error(
                            f"OpenAI API error: {response.status}"
                        )
                        return self._default_response()

                    result = await response.json()
                    content = (
                        result.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )

                    try:
                        data = json.loads(content)
                        if not self._is_valid_result(data):
                            raise ValueError(
                                "Resultado mal formatado"
                            )

                        return NutritionCalculateOutputDto(
                            protein_g=float(
                                data["protein_g"]
                            ),
                            carbohydrates_total_g=float(
                                data["carbohydrates_g"]
                            ),
                            fat_total_g=float(
                                data["fat_g"]
                            ),
                        )
                    except Exception as parse_err:
                        logger.warning(
                            f"Erro ao interpretar resposta do modelo: {parse_err}"
                        )
                        return self._default_response()

        except Exception as e:
            logger.error(
                f"Erro geral ao consultar OpenAI: {e}"
            )
            return self._default_response()

    def _is_valid_result(self, data: dict) -> bool:
        keys = ["protein_g", "carbohydrates_g", "fat_g"]
        return all(
            key in data
            and isinstance(data[key], (int, float))
            for key in keys
        )

    def _default_response(
        self,
    ) -> NutritionCalculateOutputDto:
        return NutritionCalculateOutputDto(
            protein_g=0.0,
            carbohydrates_total_g=0.0,
            fat_total_g=0.0,
        )
