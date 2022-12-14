from fastapi import FastAPI
# Routers
from src.apps.v1.routes import auth_route, users_route, vaults_route, accounts_route


def register_api_routers(app: FastAPI, prefix_url: str) -> None:
    """Register the api routes

    This is function to register all router by the APIRouter.

    Args:

        app (FastAPI): FastAPI instance.
    """

    app.include_router(
        auth_route.router, prefix=f'{prefix_url}/auth', tags=['Auth', 'Users'])

    app.include_router(
        users_route.router, prefix=f'{prefix_url}/users', tags=['Users'])

    app.include_router(
        vaults_route.router, prefix=f'{prefix_url}/vaults', tags=['Vaults'])

    app.include_router(
        accounts_route.router, prefix=f'{prefix_url}/accounts', tags=['Accounts'])
