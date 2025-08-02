import time
from typing import Tuple, Optional
from datetime import datetime
from src.seaapi.domain.ports.services.rate_limiter import (
    RateLimiterInterface,
)

try:
    import redis

    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False


class RedisRateLimiter(RateLimiterInterface):
    """
    Implementação de rate limiter usando Redis com sliding window
    Adequado para produção e aplicações distribuídas
    """

    def __init__(
        self,
        redis_url: str = "redis://localhost:6379",
        **redis_kwargs,
    ):
        if not REDIS_AVAILABLE:
            raise ImportError(
                "Redis não está disponível. Instale com: pip install redis"
            )

        self.redis_client = redis.from_url(
            redis_url, **redis_kwargs
        )
        self.key_prefix = "rate_limit"

    def _get_key(
        self,
        identifier: str,
        endpoint: Optional[str] = None,
    ) -> str:
        """Gera chave única para o identificador e endpoint"""
        if endpoint:
            return (
                f"{self.key_prefix}:{identifier}:{endpoint}"
            )
        return f"{self.key_prefix}:{identifier}"

    async def is_allowed(
        self,
        identifier: str,
        max_requests: int,
        window_seconds: int,
        endpoint: Optional[str] = None,
    ) -> Tuple[bool, dict]:
        """
        Verifica se a requisição deve ser permitida usando sliding window no Redis
        """
        key = self._get_key(identifier, endpoint)
        current_time = time.time()
        cutoff_time = current_time - window_seconds

        # Pipeline para operações atômicas
        pipe = self.redis_client.pipeline()

        # Remove entradas antigas
        pipe.zremrangebyscore(key, 0, cutoff_time)

        # Conta requisições atuais
        pipe.zcard(key)

        # Executa pipeline
        results = pipe.execute()
        current_count = results[1]

        # Verifica se excedeu o limite
        if current_count >= max_requests:
            # Pega a requisição mais antiga para calcular reset_time
            oldest_requests = self.redis_client.zrange(
                key, 0, 0, withscores=True
            )
            if oldest_requests:
                oldest_time = oldest_requests[0][1]
                reset_time = oldest_time + window_seconds
            else:
                reset_time = current_time + window_seconds

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
        pipe = self.redis_client.pipeline()
        pipe.zadd(key, {str(current_time): current_time})
        pipe.expire(
            key, window_seconds + 1
        )  # TTL ligeiramente maior que a janela
        pipe.execute()

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
        result = self.redis_client.delete(key)
        return result > 0

    def get_stats(self) -> dict:
        """Retorna estatísticas do rate limiter"""
        pattern = f"{self.key_prefix}:*"
        keys = self.redis_client.keys(pattern)

        total_requests = 0
        for key in keys:
            total_requests += self.redis_client.zcard(key)

        return {
            "type": "redis",
            "total_tracked_keys": len(keys),
            "total_active_requests": total_requests,
            "redis_info": {
                "memory_usage": self.redis_client.info().get(
                    "used_memory_human", "N/A"
                ),
                "connected_clients": self.redis_client.info().get(
                    "connected_clients", 0
                ),
            },
        }
