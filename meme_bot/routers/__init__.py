__all__ = ("router",)

from aiogram import Router
from .commands import router as commands_router
from .common import router as common_router

router = Router(name=__name__)

router.include_routers(
    commands_router,
)

# This router should be the last one
router.include_router(common_router)
