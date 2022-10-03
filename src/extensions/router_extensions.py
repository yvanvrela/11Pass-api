from fastapi import FastAPI

from src.apps.v1.routes.auth_route import router as auth

api_router = '/api/v1'


def register_routers(app: FastAPI) -> None:
    """Register the api routes

    This is function to register all router by the APIRouter.

    Args:

        app (FastAPI): FastAPI instance.
    """
    app.include_router(
        auth, prefix=f'{api_router}/auth', tags=['Auth', 'User'])
