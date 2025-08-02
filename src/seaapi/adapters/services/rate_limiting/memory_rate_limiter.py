import time
from typing import Tuple, Optional, Dict, List
from datetime import datetime
from src.seaapi.domain.ports.services.rate_limiter import (
    RateLimiterInterface,
)


class MemoryRateLimiter(RateLimiterInterface):
    """
    Implementação de rate limiter em memória usando sliding window
    Adequado para desenvolvimento e aplicações de pequeno porte
    """

    def __init__(self):
        self._requests: Dict[str, List[float]] = {}

    def _get_key(
        self,
        identifier: str,
        endpoint: Optional[str] = None,
    ) -> str:
        """Gera chave única para o identificador e endpoint"""
        if endpoint:
            return f"{identifier}:{endpoint}"
        return identifier

    def _cleanup_old_requests(
        self, requests: List[float], window_seconds: int
    ) -> List[float]:
        """Remove requisições antigas fora da janela de tempo"""
        current_time = time.time()
        cutoff_time = current_time - window_seconds
        return [
            req_time
            for req_time in requests
            if req_time > cutoff_time
        ]

    async def is_allowed(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int,
        endpoint: Optional[str] = None,
    ) -> Tuple[bool, dict]:
        """
        Verifica se a requisição deve ser permitida usando sliding window
        """
        key = self._get_key(identifier, endpoint)
        current_time = time.time()

        # Inicializa se não existir
        if key not in self._requests:
            self._requests[key] = []

        # Remove requisições antigas
        self._requests[key] = self._cleanup_old_requests(
            self._requests[key], window_seconds
        )

        current_count = len(self._requests[key])

        # Verifica se excedeu o limite
        if current_count >= max_requests:
            # Calcula quando a próxima requisição será permitida
            oldest_request = (
                min(self._requests[key])
                if self._requests[key]
                else current_time
            )
            reset_time = oldest_request + window_seconds

            return False, {
                "allowed": False,
                "current_requests": current_count,
                "max_requests": max_requests,
                "window_seconds": window_seconds,
                "reset_time": datetime.fromtimestamp(
                    reset_time
                ).isoformat(),
                "retry_after": max(
                    0, int(reset_time - current_time)
                ),
            }

        # Adiciona a requisição atual
        self._requests[key].append(current_time)

        return True, {
            "allowed": True,
            "current_requests": current_count + 1,
            "max_requests": max_requests,
            "window_seconds": window_seconds,
            "remaining_requests": max_requests
            - current_count
            - 1,
        }

    async def reset_limit(
        self,
        identifier: str,
        endpoint: Optional[str] = None,
    ) -> bool:
        """Reseta o limite para um identificador específico"""
        key = self._get_key(identifier, endpoint)
        if key in self._requests:
            del self._requests[key]
            return True
        return False

    def get_stats(self) -> dict:
        """Retorna estatísticas do rate limiter"""
        total_keys = len(self._requests)
        total_requests = sum(
            len(requests)
            for requests in self._requests.values()
        )

        return {
            "type": "memory",
            "total_tracked_keys": total_keys,
            "total_active_requests": total_requests,
            "memory_usage_estimate": f"{total_requests * 8} bytes",  # Aproximação
        }
