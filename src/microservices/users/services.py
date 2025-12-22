from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import *
from .repository import *
from datetime import datetime, timezone
from src.config.models import Users
from fastapi import Request
from .schemas import *

class UserService:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_user_async(self, pagination_params: PaginationParams):
        orm_model = await UserRepository(db_session=self.db_session, request=self.request).select_all_user_async(pagination_params)
        dto_model = [UserGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_user_by_id_async(self, user_id: int):
        orm_model = await UserRepository(db_session=self.db_session, request=self.request).select_user_by_id_async(user_id)
        dto_model = UserGetDTO.model_validate(orm_model)
        return dto_model

    async def create_user_async(self, user: UserCreateDTO):
        orm_model = Users(**user.model_dump(exclude_none=True))
        result = await UserRepository(db_session=self.db_session, request=self.request).create_user_async(orm_model)
        dto_model = UserGetDTO.model_validate(result)
        return dto_model

    async def update_user_async(self, user: UserUpdateDTO):
        orm_model = Users(**user.model_dump(exclude_none=True, exclude_defaults=True))
        result = await UserRepository(db_session=self.db_session, request=self.request).update_user_async(orm_model)
        dto_model = UserGetDTO.model_validate(result)
        return dto_model

    async def delete_user_async(self, user_id: int):
        orm_model = await UserRepository(db_session=self.db_session, request=self.request).delete_user_async(user_id)
        dto_model = UserDeleteDTO.model_validate(orm_model)
        return dto_model