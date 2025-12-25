from src.config.models.models import Readers
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.exception_handler import RecordNotFoundError
from src.config import settings
from src.config.schemas.schemas import *
from fastapi import Request
import bcrypt

def hash_password(password) -> bytes:
    hashed_password = bcrypt.hashpw(password, bcrypt.gensalt(rounds=14))
    return hashed_password

def verify_password(plain_password, hashed_password) -> bool:
    return bcrypt.checkpw(plain_password, hashed_password)

class ReaderRepositoryAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def refresh_password(self, id_reader: int, old_password: str, new_password: str):
        reader = await self.db_session.get(Readers, {'id': int(id_reader)})
        if verify_password(old_password.encode(), reader.password):
            reader.password = hash_password(new_password.encode())
            await self.db_session.commit()
            settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил пароль у пользователя с id {id_reader}')
            return id_reader
        raise ValueError(f"Пароль для пользователя с id {id_reader} введен неверно")

    async def select_all_records_rel(self, pagination_params: PaginationParams):
        query = (select(Readers).limit(pagination_params.limit).offset(pagination_params.offset)
                 .options(selectinload(Readers.books)).options(selectinload(Readers.distributions))
                 )
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателях')
        return records.scalars().all()

    async def select_all_records(self, pagination_params: PaginationParams):
        query = select(Readers).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателях')
        return records.scalars().all()

    async def select_record_id_rel(self, reader_id: int):
        query = (
            select(Readers)
            .select_from(Readers).filter(Readers.id == int(reader_id))
            .options(selectinload(Readers.books))
            .options(selectinload(Readers.distributions))
        )
        record = await self.db_session.execute(query)
        reader = record.scalar()
        if reader is None:
            raise RecordNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателе с id: {reader_id}')
        return reader

    async def select_record_id(self, reader_id: int):
        record = await self.db_session.get(Readers, {'id': reader_id})
        if record is None:
            raise RecordNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о читателе с id: {reader_id}')
        return record

    async def create_record(self, orm_model: Readers):
        orm_model.password = hash_password(orm_model.password)
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - добавил нового читателя')
        return orm_model.id

    async def update_record(self, orm_model: Readers):
        updating_orm_model = await self.db_session.get(Readers, {'id': orm_model.id})
        if updating_orm_model is None:
            raise RecordNotFoundError(message=f'Читатель с номером: {orm_model.id} не найден')
        for k,v in orm_model.get_model_attr_without_relations().items():
            if v is not None and k != 'password':
                setattr(updating_orm_model, k, v)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил данные читателя с id: {orm_model.id}')
        return updating_orm_model.id

    async def delete_record(self, reader_id: int):
        deleting_orm_model = await self.db_session.get(Readers, {'id': int(reader_id)})
        if deleting_orm_model is None:
            raise RecordNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - удалил данные читателя с id: {reader_id}')
        return reader_id