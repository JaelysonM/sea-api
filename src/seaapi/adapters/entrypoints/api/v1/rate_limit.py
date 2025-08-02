from dependency_injector.wiring import (
    Provide,
    inject,
)
from fastapi import (
    APIRouter,
    Depends,
    Request,
)
from fastapi.security import HTTPBearer
from src.seaapi.config.containers import Container
from src.seaapi.domain.ports.services.rate_limiter import (
    RateLimiterInterface,
)
from src.seaapi.adapters.entrypoints.api.shared.permissions import (
    PermissionsDependency,
    And,
    IsAuthenticated,
    IsAdministrator,
)

router = APIRouter()
auth_scheme = HTTPBearer()


@router.get(
    "/stats",
    dependencies=[
        Depends(
            PermissionsDependency(
                And([IsAuthenticated(), IsAdministrator()])
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
def get_rate_limit_stats(
    rate_limiter: RateLimiterInterface = Depends(
        Provide[Container.rate_limiter]
    ),
):
    """
    Retorna estatísticas do rate limiter
    Apenas administradores podem acessar
    """
    if hasattr(rate_limiter, "get_stats"):
        return {
            "rate_limiting_enabled": True,
            "stats": rate_limiter.get_stats(),
        }

    return {
        "rate_limiting_enabled": True,
        "stats": {
            "message": "Estatísticas não disponíveis para este backend"
        },
    }


@router.post(
    "/reset/{identifier}",
    dependencies=[
        Depends(
            PermissionsDependency(
                And([IsAuthenticated(), IsAdministrator()])
            )
        ),
        Depends(auth_scheme),
    ],
)
@inject
async def reset_rate_limit(
    identifier: str,
    endpoint: str = None,
    rate_limiter: RateLimiterInterface = Depends(
        Provide[Container.rate_limiter]
    ),
):
    """
    Reseta o rate limit para um identificador específico
    Apenas administradores podem fazer isso
    """
    success = await rate_limiter.reset_limit(
        identifier, endpoint
    )

    return {
        "success": success,
        "message": f"Rate limit {'resetado' if success else 'não encontrado'} "
        f"para {identifier}"
        + (f" no endpoint {endpoint}" if endpoint else ""),
    }


@router.get(
    "/my-status",
    dependencies=[
        Depends(PermissionsDependency(IsAuthenticated())),
        Depends(auth_scheme),
    ],
)
@inject
async def get_my_rate_limit_status(
    request: Request,
    rate_limiter: RateLimiterInterface = Depends(
        Provide[Container.rate_limiter]
    ),
):
    """
    Retorna o status de rate limiting do usuário atual
    """
    # Identifica o usuário
    if (
        hasattr(request, "user")
        and request.user
        and hasattr(request.user, "id")
    ):
        identifier = f"user:{request.user.id}"
    else:
        client_ip = (
            request.client.host
            if request.client
            else "unknown"
        )
        identifier = f"ip:{client_ip}"

    # Testa diferentes endpoints comuns para mostrar status
    endpoints_to_check = [
        ("POST:/v1/foods", 20, 3600),
        ("GET:/v1/foods", 200, 3600),
        ("POST:/v1/auth/refresh", 10, 300),
    ]

    status = {"identifier": identifier, "endpoints": {}}

    for endpoint, max_req, window in endpoints_to_check:
        allowed, info = await rate_limiter.is_allowed(
            identifier=identifier,
            max_requests=max_req,
            window_seconds=window,
            endpoint=endpoint,
        )

        # "Desfaz" a verificação se foi permitida (para não contar como uso real)
        if allowed and hasattr(rate_limiter, "_requests"):
            # Para MemoryRateLimiter, remove a última entrada
            key = f"{identifier}:{endpoint}"
            if (
                key in rate_limiter._requests
                and rate_limiter._requests[key]
            ):
                rate_limiter._requests[key].pop()

        status["endpoints"][endpoint] = {
            "currently_allowed": allowed,
            "current_requests": info.get(
                "current_requests", 0
            ),
            "max_requests": max_req,
            "window_seconds": window,
            "remaining_requests": info.get(
                "remaining_requests", 0
            ),
            "reset_time": info.get("reset_time")
            if not allowed
            else None,
        }

    return status
