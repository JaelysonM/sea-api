from fastapi import APIRouter
from src.seaapi.adapters.entrypoints.api.v1 import (
    auth,
    user,
    group,
    permission,
    food,
    meal,
)

api_router = APIRouter(prefix="/v1")

api_router.include_router(
    auth.router, prefix="/auth", tags=["Authentication"]
)
api_router.include_router(
    user.router, prefix="/users", tags=["Users"]
)

api_router.include_router(
    group.router,
    prefix="/groups",
    tags=["Groups and Permissions"],
)


api_router.include_router(
    permission.router,
    prefix="/permissions",
    tags=["Groups and Permissions"],
)


api_router.include_router(
    food.router,
    prefix="/foods",
    tags=["Foods"],
)


api_router.include_router(
    meal.router,
    prefix="/meals",
    tags=["Meals"],
)
