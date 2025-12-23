from src.config.models.books import Books
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.config.exception_handler import RecordNotFoundError
from src.config import settings
from .schemas import PaginationParams
from fastapi import Request

class BookRepository:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_book_async(self, pagination_params: PaginationParams):
        query = select(Books).limit(pagination_params.limit).offset(pagination_params.offset)
        records = await self.db_session.execute(query)
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о книгах')
        return records.scalars().all()

    async def select_book_by_id_async(self, book_id: int):
        record = await self.db_session.get(Books, {'id': book_id})
        if record is None:
            raise RecordNotFoundError(message=f'Книга с номером: {book_id} не найдена')
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - вывел данные о книге с id: {book_id}')
        return record

    async def create_book_async(self, orm_model: Books):
        self.db_session.add(orm_model)
        await self.db_session.flush()
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - добавил новую книгу')
        return orm_model

    async def update_book_async(self, orm_model: Books):
        updating_orm_model = await self.db_session.get(Books, {'id': orm_model.id})
        if updating_orm_model is None:
            raise RecordNotFoundError(message=f'Книга с номером: {orm_model.id} не найдена')
        for k,v in orm_model.get_model_attributes().items():
            if v is not None:
                setattr(updating_orm_model, k, v)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - обновил данные о книге с id: {orm_model.id}')
        return updating_orm_model

    async def delete_book_async(self, book_id: int):
        deleting_orm_model = await self.db_session.get(Books, {'id': int(book_id)})
        if deleting_orm_model is None:
            raise RecordNotFoundError(message=f'Книга с номером: {book_id} не найдена')
        await self.db_session.delete(deleting_orm_model)
        await self.db_session.commit()
        settings.logging.logger.info(f'{self.request.client.host} - {self.request.method} - удалил данные о книге с id: {book_id}')
        return deleting_orm_model