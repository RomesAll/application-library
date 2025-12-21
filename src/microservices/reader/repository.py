from src.config.models.readers import Readers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .exception_handler import ReaderNotFoundError
from src.config import settings
from .schemas import PaginationParams
from fastapi import Request
import bcrypt

def hash_password(password) -> bytes:
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=14))
    return hashed_password

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)

class ReaderRepository:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_reader_async(self, pagination_params: PaginationParams):
        query = select(Readers).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателях')
        return records.scalars().all()

    async def select_reader_by_id_async(self, reader_id: int):
        record = await self.db_session.get(Readers, {'id': reader_id})
        if record is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателе с id: {reader_id}')
        return record

    async def create_reader_async(self, orm_model: Readers):
        orm_model.password = hash_password(orm_model.password)
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - добавил нового читателя')
        return orm_model

    async def update_reader_async(self, orm_model: Readers):
        updating_orm_model = await self.db_session.get(Readers, {'id': orm_model.id})
        if updating_orm_model is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {orm_model.id} не найден')
        for k,v in orm_model.get_model_attributes().items():
            if v is not None and k != 'password':
                setattr(updating_orm_model, k, v)
        updating_orm_model.password = hash_password(orm_model.password)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил данные читателя с id: {orm_model.id}')
        return updating_orm_model

    async def delete_reader_async(self, reader_id: int):
        deleting_orm_model = await self.db_session.get(Readers, {'id': int(reader_id)})
        if deleting_orm_model is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - удалил данные читателя с id: {reader_id}')
        return deleting_orm_model