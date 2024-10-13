from .main_handler import router as main_router
from .commands import router as commands_router
from .profile import router as profile_router


__all__ = ['main_router', 'commands_router', 'profile_router']
