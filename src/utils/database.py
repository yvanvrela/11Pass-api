from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.v1.config.settings import Settings

settings = Settings()

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.db_user}:{settings.db_pass}@postgresserver/{settings.db_name}'

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base return a class, later we will inherit from this class to create each of the database models
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
