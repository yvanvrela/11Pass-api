from fastapi import FastAPI
# Routers
from src.apps.v1.routes.auth_route import router as auth
# Settings
from src.core.settings import Settings

settings = Settings()
api_url_prefix = settings.api_prefix_router


def register_routers(app: FastAPI) -> None:
    """Register the api routes

    This is function to register all router by the APIRouter.

    Args:

        app (FastAPI): FastAPI instance.
    """
    app.include_router(
        auth, prefix=f'{api_url_prefix}/auth', tags=['Auth', 'User'])
