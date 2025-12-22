from .schemas import *
from .repository import *
from datetime import datetime, timezone
from fastapi import Request

class BookService:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_book_async(self, pagination_params: PaginationParams):
        orm_model = await BookRepository(db_session=self.db_session, request=self.request).select_all_book_async(pagination_params)
        dto_model = [BookGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_book_by_id_async(self, book_id: int):
        orm_model = await BookRepository(db_session=self.db_session, request=self.request).select_book_by_id_async(book_id)
        dto_model = BookGetDTO.model_validate(orm_model)
        return dto_model

    async def create_book_async(self, book: BookCreateDTO):
        orm_model = Books(**book.model_dump(exclude_none=True))
        result = await BookRepository(db_session=self.db_session, request=self.request).create_book_async(orm_model)
        dto_model = BookGetDTO.model_validate(result)
        return dto_model

    async def update_book_async(self, book: BookUpdateDTO):
        orm_model = Books(**book.model_dump(exclude_none=True, exclude_defaults=True))
        result = await BookRepository(db_session=self.db_session, request=self.request).update_book_async(orm_model)
        dto_model = BookGetDTO.model_validate(result)
        return dto_model

    async def delete_book_async(self, book_id: int):
        orm_model = await BookRepository(db_session=self.db_session, request=self.request).delete_book_async(book_id)
        dto_model = BookDeleteDTO.model_validate(orm_model)
        return dto_model