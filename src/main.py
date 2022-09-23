from application import create_app
from utils.database import Base, engine
from database.models import *
import uvicorn

Base.metadata.create_all(bind=engine)

app = create_app()


def main() -> None:
    """Run FastApi
    """

    uvicorn.run(
        app='main:app',
        host='127.0.0.1',
        port=8000,
        reload=True,
    )


if __name__ == '__main__':
    main()
