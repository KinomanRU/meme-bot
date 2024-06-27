__all__ = ("router",)

from aiogram import Router
from routers.commands.base import router as base_router
from .user import router as user_router

router = Router(name=__name__)

router.include_routers(
    base_router,
    user_router,
)
