from pydantic_settings import BaseSettings, SettingsConfigDict
import os, sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

class PostgresSettings(BaseSettings):
    POSTGRES_HOST: str | None = None
    POSTGRES_USER: str | None = None
    POSTGRES_PASSWORD: str | None = None
    POSTGRES_DB: str | None = None
    POSTGRES_PORT: int | None = None
    POSTGRES_MODE: str | None = None
    model_config = SettingsConfigDict(env_file=f'{BASE_DIR}/.env_test')

    @property
    def POSTGRES_URL_async(self):
        return f'postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def POSTGRES_URL_sync(self):
        return f'postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}'

    @property
    def POSTGRES_URL_default(self):
        return f'sqlite+pysqlite:///:default.db:'

class Settings(BaseSettings):
    database: PostgresSettings = PostgresSettings()

settings = Settings()
