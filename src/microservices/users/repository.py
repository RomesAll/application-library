from src.config.models import Users
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.exception_handler import RecordNotFoundError
from src.config import settings
from .schemas import PaginationParams
from fastapi import Request
import bcrypt

def hash_password(password) -> bytes:
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=14))
    return hashed_password

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)

class UserRepository:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_user_async(self, pagination_params: PaginationParams):
        query = select(Users).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о сотрудниках')
        return records.scalars().all()

    async def select_user_by_id_async(self, user_id: int):
        record = await self.db_session.get(Users, {'id': user_id})
        if record is None:
            raise RecordNotFoundError(message=f'Сотрудник с номером: {user_id} не найден')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о сотруднике с id: {user_id}')
        return record

    async def create_user_async(self, orm_model: Users):
        orm_model.password = hash_password(orm_model.password)
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - добавил нового сотрудника')
        return orm_model

    async def update_user_async(self, orm_model: Users):
        updating_orm_model = await self.db_session.get(Users, {'id': orm_model.id})
        if updating_orm_model is None:
            raise RecordNotFoundError(message=f'Сотрудник с номером: {orm_model.id} не найден')
        for k,v in orm_model.get_model_attributes().items():
            if v is not None and k != 'password':
                setattr(updating_orm_model, k, v)
        updating_orm_model.password = hash_password(orm_model.password)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил данные сотрудника с id: {orm_model.id}')
        return updating_orm_model

    async def delete_user_async(self, user_id: int):
        deleting_orm_model = await self.db_session.get(Users, {'id': int(user_id)})
        if deleting_orm_model is None:
            raise RecordNotFoundError(message=f'Сотрудник с номером: {user_id} не найден')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - удалил данные сотрудника с id: {user_id}')
        return deleting_orm_model