from src.config.models.readers import Readers
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from .exception_handler import ReaderNotFoundError
from src.config import settings
from .schemas import PaginationParams

class ReaderRepository:

    def __init__(self, db_session):
        self.db_session: AsyncSession = db_session

    async def select_all_reader_async(self, pagination_params: PaginationParams):
        query = select(Readers).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'Получение данных о читателях')
        return records.scalars().all()

    async def select_reader_by_id_async(self, reader_id: int):
        record = await self.db_session.get(Readers, {'id': reader_id})
        if record is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        settings.logging.logger.info(f'Получение данных о читателе с id: {reader_id}')
        return record

    async def create_reader_async(self, orm_model: Readers):
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'Добавление данных о читателе с id: {orm_model.id}')
        return orm_model

    async def update_reader_async(self, orm_model: Readers):
        updating_orm_model = await self.db_session.get(Readers, {'id': orm_model.id})
        if updating_orm_model is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {orm_model.id} не найден')
        for k,v in orm_model.get_model_attributes().items():
            if v is not None:
                setattr(updating_orm_model, k, v)
        await self.db_session.commit()
        settings.logging.logger.info(f'Обновление данных о читателе с id: {orm_model.id}')
        return updating_orm_model

    async def delete_reader_async(self, reader_id: int):
        deleting_orm_model = await self.db_session.get(Readers, {'id': int(reader_id)})
        if deleting_orm_model is None:
            raise ReaderNotFoundError(message=f'Читатель с номером: {reader_id} не найден')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'Удаление данных о читателе с id: {reader_id}')
        return deleting_orm_model