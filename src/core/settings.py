import os
from pydantic import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # Project Name
    project_name: str = os.getenv('PROJECT_NAME')

    # Private var
    _db_name: str = os.getenv('DB_NAME')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_host: str = os.getenv('DB_HOST')
    db_port: str = os.getenv('DB_PORT')

    # Security 
    secret_key: str = os.getenv('SECRET_KEY')
    token_expire: int = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
    algorithm_type: str = os.getenv('ALGORITHM')

    # Prefix route
    api_v1_url: str = os.getenv('API_PREFIX_ROUTER')

    @property
    def db_name(self):
        """Change the db name

        This function change the database name, if running of test.

        Returns:

            str: str database name.
        """
        if os.getenv('RUN_ENV') == 'test':
            return f'test_{self._db_name}'

        return self._db_name
