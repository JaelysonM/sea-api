from abc import ABC, abstractmethod
from typing import Tuple, Optional


class RateLimiterInterface(ABC):
    """Interface para serviços de rate limiting"""

    @abstractmethod
    async def is_allowed(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int,
        endpoint: Optional[str] = None,
    ) -> Tuple[bool, dict]:
        """
        Verifica se uma requisição deve ser permitida

        Args:
            identifier: Identificador único (IP, user_id, etc.)
            max_requests: Número máximo de requisições permitidas
            window_seconds: Janela de tempo em segundos
            endpoint: Endpoint específico (opcional)

        Returns:
            Tuple[bool, dict]: (permitido, informações sobre o limite)
        """

    @abstractmethod
    async def reset_limit(
        self,
        identifier: str,
        endpoint: Optional[str] = None,
    ) -> bool:
        """
        Reseta o limite para um identificador específico

        Args:
            identifier: Identificador único
            endpoint: Endpoint específico (opcional)

        Returns:
            bool: True se resetado com sucesso
        """
