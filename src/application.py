from fastapi import FastAPI
from src.extensions.router_extensions import register_routers


def create_app() -> FastAPI:
    """Create FastApi app

    Create a new FastApi instance, and apply the configurations.

    Returns:

        FastAPI:  FastAPI is the app.

    """
    app = FastAPI()

    register_routers(app)

    return app
