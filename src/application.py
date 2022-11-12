from fastapi import FastAPI
from src.extensions.router_extensions import register_api_routers
from src.core.settings import Settings

settings = Settings()


def create_app() -> FastAPI:
    """Create FastApi app

    Create a new FastApi instance, and apply the configurations.

    Returns:

        FastAPI:  FastAPI is the app.

    """
    app = FastAPI(
        title=settings.project_name,
        openapi_url=f'{settings.api_v1_url}/openapi.json',
        description=settings.project_description,
    )

    register_api_routers(app, prefix_url=settings.api_v1_url)

    return app
