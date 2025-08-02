from functools import wraps
from typing import Optional, Callable, Dict
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse


def rate_limit(
    max_requests: int,
    window_seconds: int,
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None,
    key_suffix: Optional[str] = None,
):
    """
    Decorador para aplicar rate limiting específico a endpoints

    Args:
        max_requests: Número máximo de requisições
        window_seconds: Janela de tempo em segundos
        identifier_func: Função para identificar o cliente
        key_suffix: Sufixo adicional para a chave de rate limiting
    """

    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Encontra o Request nos argumentos
            request = None
            for arg in args:
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                # Se não houver Request, executa normalmente
                return (
                    await func(*args, **kwargs)
                    if hasattr(func, "__await__")
                    else func(*args, **kwargs)
                )

            # Obtém o rate limiter do container da aplicação
            if hasattr(
                request.app, "container"
            ) and hasattr(
                request.app.container, "rate_limiter"
            ):
                rate_limiter = (
                    request.app.container.rate_limiter()
                )

                # Identifica o cliente
                if identifier_func:
                    identifier = identifier_func(request)
                else:
                    # Identificador padrão
                    if (
                        hasattr(request, "user")
                        and request.user
                        and hasattr(request.user, "id")
                    ):
                        identifier = (
                            f"user:{request.user.id}"
                        )
                    else:
                        client_ip = (
                            request.client.host
                            if request.client
                            else "unknown"
                        )
                        identifier = f"ip:{client_ip}"

                # Adiciona sufixo se especificado
                endpoint_key = f"{func.__name__}"
                if key_suffix:
                    endpoint_key += f":{key_suffix}"

                # Verifica rate limit
                (
                    allowed,
                    info,
                ) = await rate_limiter.is_allowed(
                    identifier=identifier,
                    max_requests=max_requests,
                    window_seconds=window_seconds,
                    endpoint=endpoint_key,
                )

                if not allowed:
                    # Retorna erro 429
                    error_response = {
                        "error": "rate_limit_exceeded",
                        "message": f"Limite de {max_requests} requisições "
                        f"por {window_seconds} segundos excedido para este endpoint",
                        "details": info,
                    }

                    return JSONResponse(
                        status_code=429,
                        content=error_response,
                        headers={
                            "Retry-After": str(
                                info.get(
                                    "retry_after",
                                    window_seconds,
                                )
                            )
                        },
                    )

            # Executa a função original
            if hasattr(func, "__await__"):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


# Decoradores pré-configurados para casos comuns
def strict_rate_limit(
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None
):
    """Rate limiting estrito: 10 requisições por minuto"""
    return rate_limit(
        max_requests=10,
        window_seconds=60,
        identifier_func=identifier_func,
        key_suffix="strict",
    )


def moderate_rate_limit(
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None
):
    """Rate limiting moderado: 100 requisições por hora"""
    return rate_limit(
        max_requests=100,
        window_seconds=3600,
        identifier_func=identifier_func,
        key_suffix="moderate",
    )


def loose_rate_limit(
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None
):
    """Rate limiting flexível: 1000 requisições por hora"""
    return rate_limit(
        max_requests=1000,
        window_seconds=3600,
        identifier_func=identifier_func,
        key_suffix="loose",
    )


def authenticated_user_rate_limit(
    max_requests: int, window_seconds: int
):
    """Rate limiting baseado apenas em usuários autenticados"""

    def user_identifier(request: Request) -> str:
        if (
            hasattr(request, "user")
            and request.user
            and hasattr(request.user, "id")
        ):
            return f"auth_user:{request.user.id}"
        raise HTTPException(
            status_code=401,
            detail="Authentication required for this endpoint",
        )

    return rate_limit(
        max_requests=max_requests,
        window_seconds=window_seconds,
        identifier_func=user_identifier,
        key_suffix="auth_only",
    )


def per_endpoint_rate_limit(
    limits_config: Dict[str, Dict[str, int]]
):
    """
    Rate limiting configurável por endpoint

    Args:
        limits_config: Dicionário com configurações por endpoint
        Exemplo: {
            "create_food": {"max_requests": 10, "window_seconds": 300},
            "upload_file": {"max_requests": 5, "window_seconds": 60}
        }
    """

    def decorator(func):
        endpoint_name = func.__name__
        if endpoint_name in limits_config:
            config = limits_config[endpoint_name]
            return rate_limit(
                max_requests=config["max_requests"],
                window_seconds=config["window_seconds"],
                key_suffix=f"endpoint_{endpoint_name}",
            )(func)
        return func

    return decorator
