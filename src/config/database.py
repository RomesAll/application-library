from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData
from .config_project import settings

__all__ = ['engine_sync', 'engine_def', 'engine_async', 'session_factory_sync', 'session_factory_async', 'Base']

try:
    engine_sync = create_engine(url=settings.database.POSTGRES_URL_sync, echo=False)
except Exception as exception:
    settings.logging.logger.exception(exception)
    engine_sync = None

try:
    engine_async = create_async_engine(url=settings.database.POSTGRES_URL_async, echo=False)
except Exception as exception:
    settings.logging.logger.exception(exception)
    engine_async = None

try:
    engine_def = create_engine(url=settings.database.POSTGRES_URL_default, echo=False)
except Exception as exception:
    settings.logging.logger.exception(exception)
    engine_async = None

session_factory_sync = sessionmaker(engine_sync, expire_on_commit=False)
session_factory_async = async_sessionmaker(engine_async, expire_on_commit=False)

class Base(DeclarativeBase):
    metadata = MetaData()