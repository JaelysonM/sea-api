from functools import wraps
from typing import Optional, Callable, Dict
from fastapi import Request, HTTPException


def rate_limit(
    max_requests: int,
    window_seconds: int,
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None,
    key_suffix: Optional[str] = None,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = None
            for arg in list(args) + list(kwargs.values()):
                if isinstance(arg, Request):
                    request = arg
                    break

            if not request:
                return (
                    await func(*args, **kwargs)
                    if hasattr(func, "__await__")
                    else func(*args, **kwargs)
                )

            if hasattr(
                request.app, "container"
            ) and hasattr(
                request.app.container, "rate_limiter"
            ):
                rate_limiter = (
                    request.app.container.rate_limiter()
                )

                if identifier_func:
                    identifier = identifier_func(request)
                else:
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

                endpoint_key = f"{func.__name__}"
                if key_suffix:
                    endpoint_key += f":{key_suffix}"

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
                    raise HTTPException(
                        status_code=429,
                        detail={
                            "error": "rate_limit_exceeded",
                            "message": f"Limite de {max_requests} requisições "
                            f"por {window_seconds} segundos excedido para este endpoint",
                            "details": info,
                        },
                        headers={
                            "Retry-After": str(
                                info.get(
                                    "retry_after",
                                    window_seconds,
                                )
                            )
                        },
                    )

            if hasattr(func, "__await__"):
                return await func(*args, **kwargs)
            else:
                return func(*args, **kwargs)

        return wrapper

    return decorator


def strict_rate_limit(
    identifier_func: Optional[
        Callable[[Request], str]
    ] = None
):
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
    return rate_limit(
        max_requests=1000,
        window_seconds=3600,
        identifier_func=identifier_func,
        key_suffix="loose",
    )


def authenticated_user_rate_limit(
    max_requests: int, window_seconds: int
):
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
