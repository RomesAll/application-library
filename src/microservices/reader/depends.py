from src.config import db_engine_helper
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

db_session = Annotated[AsyncSession, Depends(db_engine_helper.get_session_async)]