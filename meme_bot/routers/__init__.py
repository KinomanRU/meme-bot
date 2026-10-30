__all__ = ("router",)

from aiogram import Router

from .base import router as base_router
from .other import router as other_router
from .user import router as user_router

router = Router(name=__name__)

router.include_routers(
    user_router,
    base_router,
    # This router should be the last one
    other_router,
)
