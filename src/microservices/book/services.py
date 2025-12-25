from sqlalchemy.ext.asyncio import AsyncSession
from src.config.schemas.schemas import *
from src.config.models.models import Books
from .repository import BookRepositoryAsync
from fastapi import Request

class BookServiceAsync:

    def __init__(self, db_session, request):
        self.db_session: AsyncSession = db_session
        self.request: Request = request

    async def select_all_books(self, pagination_params: PaginationParams):
        orm_model = await BookRepositoryAsync(db_session=self.db_session, request=self.request).select_all_books(pagination_params)
        dto_model = [BookGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_all_books_rel(self, pagination_params: PaginationParams):
        orm_model = await BookRepositoryAsync(db_session=self.db_session, request=self.request).select_all_books_rel(pagination_params)
        dto_model = [BookRelGetDTO.model_validate(row) for row in orm_model]
        return dto_model

    async def select_book_by_id(self, book_id: int):
        orm_model = await BookRepositoryAsync(db_session=self.db_session, request=self.request).select_book_by_id(book_id)
        dto_model = BookGetDTO.model_validate(orm_model)
        return dto_model

    async def select_book_by_id_rel(self, book_id: int):
        orm_model = await BookRepositoryAsync(db_session=self.db_session, request=self.request).select_book_by_id_rel(book_id)
        dto_model = BookRelGetDTO.model_validate(orm_model)
        return dto_model

    async def create_book(self, book: BookCreateDTO):
        orm_model = Books(**book.model_dump(exclude_none=True))
        result = await BookRepositoryAsync(db_session=self.db_session, request=self.request).create_book(orm_model)
        return result

    async def update_book(self, book: BookUpdateDTO):
        orm_model = Books(**book.model_dump(exclude_none=True, exclude_defaults=True))
        result = await BookRepositoryAsync(db_session=self.db_session, request=self.request).update_book(orm_model)
        return result

    async def delete_book(self, book_id: int):
        result = await BookRepositoryAsync(db_session=self.db_session, request=self.request).delete_book(book_id)
        return result