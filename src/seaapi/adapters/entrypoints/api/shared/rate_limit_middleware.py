from typing import Optional, Callable, Dict
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from src.seaapi.domain.ports.services.rate_limiter import (
    RateLimiterInterface,
)


class RateLimitMiddleware(BaseHTTPMiddleware):
    """
    Middleware de rate limiting para FastAPI
    Aplica limites de requisições baseados em diferentes estratégias
    """

    def __init__(
        self,
        app,
        rate_limiter: RateLimiterInterface,
        default_max_requests: int = 100,
        default_window_seconds: int = 3600,  # 1 hora
        identifier_func: Optional[
            Callable[[Request], str]
        ] = None,
        exempt_endpoints: Optional[list] = None,
        custom_limits: Optional[
            Dict[str, Dict[str, int]]
        ] = None,
    ):
        super().__init__(app)
        self.rate_limiter = rate_limiter
        self.default_max_requests = default_max_requests
        self.default_window_seconds = default_window_seconds
        self.identifier_func = (
            identifier_func or self._default_identifier
        )
        self.exempt_endpoints = exempt_endpoints or []
        self.custom_limits = custom_limits or {}

    def _default_identifier(self, request: Request) -> str:
        """
        Identificador padrão baseado em usuário autenticado ou IP
        """
        # Prioriza usuário autenticado
        if (
            hasattr(request, "user")
            and request.user
            and hasattr(request.user, "id")
        ):
            return f"user:{request.user.id}"

        # Fallback para IP
        client_ip = self._get_client_ip(request)
        return f"ip:{client_ip}"

    def _get_client_ip(self, request: Request) -> str:
        """Extrai o IP do cliente considerando proxies"""
        # Verifica headers de proxy
        forwarded_for = request.headers.get(
            "X-Forwarded-For"
        )
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()

        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip

        # IP direto
        if request.client:
            return request.client.host

        return "unknown"

    def _get_endpoint_key(self, request: Request) -> str:
        """Gera chave única para o endpoint"""
        method = request.method
        path = request.url.path
        return f"{method}:{path}"

    def _get_limits_for_endpoint(
        self, endpoint: str
    ) -> tuple:
        """Retorna os limites específicos para um endpoint"""
        if endpoint in self.custom_limits:
            limits = self.custom_limits[endpoint]
            return limits.get(
                "max_requests", self.default_max_requests
            ), limits.get(
                "window_seconds",
                self.default_window_seconds,
            )

        return (
            self.default_max_requests,
            self.default_window_seconds,
        )

    def _should_exempt(self, request: Request) -> bool:
        """Verifica se o endpoint deve ser isento do rate limiting"""
        endpoint = self._get_endpoint_key(request)
        return any(
            exempt in endpoint
            for exempt in self.exempt_endpoints
        )

    async def dispatch(self, request: Request, call_next):
        """Processa a requisição aplicando rate limiting"""

        # Verifica se deve aplicar rate limiting
        if self._should_exempt(request):
            return await call_next(request)

        # Identifica o cliente
        identifier = self.identifier_func(request)
        endpoint = self._get_endpoint_key(request)

        # Obtém limites para o endpoint
        (
            max_requests,
            window_seconds,
        ) = self._get_limits_for_endpoint(endpoint)

        try:
            # Verifica rate limit
            (
                allowed,
                info,
            ) = await self.rate_limiter.is_allowed(
                identifier=identifier,
                max_requests=max_requests,
                window_seconds=window_seconds,
                endpoint=endpoint,
            )

            if not allowed:
                # Retorna erro 429 (Too Many Requests)
                headers = {
                    "X-RateLimit-Limit": str(max_requests),
                    "X-RateLimit-Window": str(
                        window_seconds
                    ),
                    "X-RateLimit-Remaining": "0",
                    "Retry-After": str(
                        info.get(
                            "retry_after", window_seconds
                        )
                    ),
                }

                error_response = {
                    "error": "rate_limit_exceeded",
                    "message": f"Limite de {max_requests} requisições por "
                    f"{window_seconds} segundos excedido",
                    "details": {
                        "current_requests": info.get(
                            "current_requests", 0
                        ),
                        "max_requests": max_requests,
                        "window_seconds": window_seconds,
                        "reset_time": info.get(
                            "reset_time"
                        ),
                        "retry_after": info.get(
                            "retry_after"
                        ),
                    },
                }

                return JSONResponse(
                    status_code=429,
                    content=error_response,
                    headers=headers,
                )

            # Processa a requisição
            response = await call_next(request)

            # Adiciona headers informativos
            response.headers["X-RateLimit-Limit"] = str(
                max_requests
            )
            response.headers["X-RateLimit-Window"] = str(
                window_seconds
            )
            response.headers["X-RateLimit-Remaining"] = str(
                info.get("remaining_requests", 0)
            )

            return response

        except Exception as e:

            print(f"Rate limiter error: {e}")
            response = await call_next(request)
            response.headers[
                "X-RateLimit-Error"
            ] = "rate_limiter_unavailable"
            return response
