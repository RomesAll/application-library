from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy import create_engine, MetaData, text
from config import settings

engine_sync = create_engine(url=settings.database.POSTGRES_URL_sync, echo=False)
engine_def = create_engine(url=settings.database.POSTGRES_URL_default, echo=False)
engine_async = create_async_engine(url=settings.database.POSTGRES_URL_async, echo=False)

session_factory_sync = sessionmaker(engine_sync, expire_on_commit=False)
session_factory_async = sessionmaker(engine_sync, expire_on_commit=False)

class Base(DeclarativeBase):
    metadata = MetaData()

with engine_sync.connect() as conn:
    res = conn.execute(text("SELECT VERSION()"))
    print(res.all())