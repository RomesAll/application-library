from fastapi import APIRouter
from .services import BookServiceAsync
from fastapi import Request
from .depends import db_session, pagination_params_dep
from src.config.schemas.schemas import *

router = APIRouter(tags=['Book'], prefix='/book')

@router.get('/', description='Вывод всех книг')
async def get_all_book(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[BookGetDTO]:
    result = await BookServiceAsync(db_session=session, request=request).select_all_books(pagination_params)
    return {'message': result}


@router.get('/{book_id}', description='Вывод книги по id')
async def get_book_by_id(book_id: int, request: Request, session: db_session):
    result = await BookServiceAsync(db_session=session, request=request).select_book_by_id(book_id)
    return {'message': result}


@router.post('/', description='Добавить книгу')
async def create_reader(book: BookCreateDTO, request: Request, session: db_session):
    result = await BookServiceAsync(db_session=session, request=request).create_book(book)
    return {'message': f'Книга с id: {result} успешно добавлен в бд'}


@router.put('/{book_id}', description='Обновить книгу')
async def update_reader_by_id(book: BookUpdateDTO, request: Request, session: db_session):
    result = await BookServiceAsync(db_session=session, request=request).update_book(book)
    return {'message': f'Книга с id: {result} успешно обновлен в бд'}


@router.delete('/{book_id}', description='Удалить книгу по id')
async def delete_reader_by_id(book_id, request: Request, session: db_session) -> BookDeleteDTO:
    result = await BookServiceAsync(db_session=session, request=request).delete_book(book_id)
    return {'message': f'Книга с id: {result} успешно удален в бд'}