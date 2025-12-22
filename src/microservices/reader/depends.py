from src.config import db_engine_helper
from fastapi import Depends
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import PaginationParams

db_session = Annotated[AsyncSession, Depends(db_engine_helper.get_session_async)]
pagination_params_dep = Annotated[PaginationParams, Depends(PaginationParams)]