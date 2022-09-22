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

Base = declarative_base()
