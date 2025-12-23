from fastapi import APIRouter, Request, middleware
from .schemas import *
from .services import *
from .depends import db_session, pagination_params_dep
from src.config import settings

router = APIRouter(tags=['Book'], prefix='/book')

@router.get('/', description='Вывод всех книг')
async def get_all_book(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[BookGetDTO]:
    result = await BookService(db_session=session, request=request).select_all_book_async(pagination_params)
    return result


@router.get('/{book_id}', description='Вывод книги по id')
async def get_book_by_id(book_id: int, request: Request, session: db_session):
    result = await BookService(db_session=session, request=request).select_book_by_id_async(book_id)
    return result


@router.post('/', description='Добавить книгу')
async def create_reader(book: BookCreateDTO, request: Request, session: db_session):
    result = await BookService(db_session=session, request=request).create_book_async(book)
    return result


@router.put('/{book_id}', description='Обновить книгу')
async def update_reader_by_id(book: BookUpdateDTO, request: Request, session: db_session):
    result = await BookService(db_session=session, request=request).update_book_async(book)
    return result


@router.delete('/{book_id}', description='Удалить книгу по id')
async def delete_reader_by_id(book_id, request: Request, session: db_session) -> BookDeleteDTO:
    result = await BookService(db_session=session, request=request).delete_book_async(book_id)
    return result