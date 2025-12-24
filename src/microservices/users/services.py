from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import *
from .repository import UserRepositoryAsync
from datetime import datetime, timezone
from src.config.models import Users
from fastapi import Request

class UserServiceAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def refresh_password(self, id_user, old_password, new_password):
        result = await UserRepositoryAsync(db_session=self.db_session, request=self.request).refresh_password(id_user, old_password, new_password)
        return result

    #
    async def select_all_records_rel(self, pagination_params: PaginationParams):
        orm_model = await UserRepositoryAsync(db_session=self.db_session, request=self.request).select_all_records_rel(pagination_params)
        dto_model = [UserRelGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_all_records(self, pagination_params: PaginationParams):
        orm_model = await UserRepositoryAsync(db_session=self.db_session, request=self.request).select_all_records(pagination_params)
        dto_model = [UserGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_record_id_rel(self, user_id: int):
        orm_model = await UserRepositoryAsync(db_session=self.db_session, request=self.request).select_record_id_rel(user_id)
        dto_model = UserRelGetDTO.model_validate(orm_model)
        return dto_model

    async def select_record_id(self, user_id: int):
        orm_model = await UserRepositoryAsync(db_session=self.db_session, request=self.request).select_record_id(user_id)
        dto_model = UserGetDTO.model_validate(orm_model)
        return dto_model

    async def create_record(self, user: UserCreateDTO):
        orm_model = Users(**user.model_dump(exclude_none=True))
        result = await UserRepositoryAsync(db_session=self.db_session, request=self.request).create_record(orm_model)
        return result

    async def update_record(self, user: UserUpdateDTO):
        orm_model = Users(**user.model_dump(exclude_none=True, exclude_defaults=True))
        result = await UserRepositoryAsync(db_session=self.db_session, request=self.request).update_record(orm_model)
        return result

    async def delete_record(self, user_id: int):
        result = await UserRepositoryAsync(db_session=self.db_session, request=self.request).delete_record(user_id)
        return result