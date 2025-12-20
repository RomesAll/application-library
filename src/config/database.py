from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, MetaData, text
from .config_project import settings
from datetime import datetime, timezone

__all__ = ['Base', 'db_engine_helper']

class DatabaseEngineHelper:

    def __init__(self):
        try:
            self._engine_sync = create_engine(url=settings.database.POSTGRES_URL_sync, echo=False)
        except Exception as exception:
            settings.logging.logger.exception(exception)
            self._engine_sync = None

        try:
            self._engine_async = create_async_engine(url=settings.database.POSTGRES_URL_async, echo=False)
        except Exception as exception:
            settings.logging.logger.exception(exception)
            self._engine_async = None

        try:
            self._engine_def = create_engine(url=settings.database.POSTGRES_URL_default, echo=False)
        except Exception as exception:
            settings.logging.logger.exception(exception)
            self._engine_def = None

        try:
            self._session_factory_sync = sessionmaker(self._engine_sync, expire_on_commit=False)
        except Exception as exception:
            settings.logging.logger.exception(exception)
            self._session_factory_sync = None

        try:
            self._session_factory_async = async_sessionmaker(self._engine_async, expire_on_commit=False)
        except Exception as exception:
            settings.logging.logger.exception(exception)
            self._session_factory_async = None

    async def get_session_async(self):
        async with self._session_factory_async() as session:
            try:
                yield session
            finally:
                await session.close()

    async def get_engine_async(self):
        async with self._engine_async.connect() as connection:
            try:
                yield connection
            finally:
                await connection.close()

    def get_session_sync(self):
        with self._session_factory_sync() as session:
            try:
                yield session
            finally:
                session.close()

    def get_engine_sync(self):
        with self._engine_sync.connect() as connection:
            try:
                yield connection
            finally:
                connection.close()

db_engine_helper = DatabaseEngineHelper()

def get_current_time():
    dt = datetime.now(tz=timezone.utc)
    return dt

class Base(DeclarativeBase):
    metadata = MetaData()

    created_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"))
    updated_at: Mapped[datetime] = mapped_column(server_default=text("TIMEZONE('utc', now())"), onupdate=text("TIMEZONE('utc', now())"))