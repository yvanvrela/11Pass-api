from fastapi import FastAPI


def create_app() -> FastAPI:
    """Create FastApi app

    Create a new FastApi instance, and apply the configurations.

    Returns:

        FastAPI:  FastAPI is the app.

    """
    app = FastAPI()

    return app
