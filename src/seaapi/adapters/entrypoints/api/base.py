from fastapi import APIRouter
from src.seaapi.adapters.entrypoints.api.v1 import (
    auth,
    user,
    group,
    permission,
    food,
    meal,
    scale,
    user_meal,
    qrcode,
    user_food,
    rate_limit,
)

api_router = APIRouter(prefix="/v1")

api_router.include_router(
    auth.router, prefix="/auth", tags=["Authentication"]
)

api_router.include_router(
    user_meal.router,
    prefix="/auth/meals",
    tags=["Authentication/Meals"],
)

api_router.include_router(
    user_food.router,
    prefix="/auth/foods",
    tags=["Authentication/Foods"],
)


api_router.include_router(
    user.router,
    prefix="/users",
    tags=["Administrator/Users"],
)

api_router.include_router(
    group.router,
    prefix="/groups",
    tags=["Administrator/Groups and Permissions"],
)


api_router.include_router(
    permission.router,
    prefix="/permissions",
    tags=["Administrator/Groups and Permissions"],
)


api_router.include_router(
    food.router,
    prefix="/foods",
    tags=["Administrator/Foods"],
)

api_router.include_router(
    meal.router,
    prefix="/meals",
    tags=["Administrator/Meals"],
)


api_router.include_router(
    scale.router,
    prefix="/scales",
    tags=["Administrator/Scales"],
)

api_router.include_router(
    qrcode.router,
    prefix="/qrcode",
    tags=["QRCode Authentication"],
)

api_router.include_router(
    rate_limit.router,
    prefix="/rate-limit",
    tags=["System/Rate Limiting"],
)
