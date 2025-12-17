from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.exc import ArgumentError
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData, text
from .config_project import settings
import logging
from .logging_config import configure_logging

__all__ = ['engine_sync', 'engine_def', 'engine_async', 'session_factory_sync', 'session_factory_async', 'Base']

logger = logging.getLogger(__name__)
configure_logging(level=logging.INFO)

try:
    engine_sync = create_engine(url=settings.database.POSTGRES_URL_sync, echo=False)
except ArgumentError as exception:
    logger.error('Не удалось создать машину соединений (engine_sync) из-за неверных параметров, переданных в url')
    engine_sync = None
except Exception as exception:
    logger.error('Не удалось создать машину соединений (engine_sync) из-за неустановленной ошибки')
    engine_sync = None

try:
    engine_async = create_async_engine(url=settings.database.POSTGRES_URL_async, echo=False)
except ArgumentError as exception:
    logger.error('Ошибка создания машины соединений (engine_async) из-за неверных параметров, переданных в url')
    engine_async = None
except Exception as exception:
    logger.error('Не удалось создать машину соединений (engine_async) из-за неустановленной ошибки')
    engine_async = None

try:
    engine_def = create_engine(url=settings.database.POSTGRES_URL_default, echo=False)
except ArgumentError as exception:
    logger.error('Ошибка создания машины соединений (engine_def) из-за неверных параметров, переданных в url')
    engine_def = None
except Exception as exception:
    logger.error('Не удалось создать машину соединений (engine_def) из-за неустановленной ошибки')
    engine_def = None

session_factory_sync = sessionmaker(engine_sync, expire_on_commit=False)
session_factory_async = async_sessionmaker(engine_async, expire_on_commit=False)

class Base(DeclarativeBase):
    metadata = MetaData()