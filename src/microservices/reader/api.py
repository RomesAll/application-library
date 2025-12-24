from fastapi import APIRouter, Request
from .schemas import ReaderCreateDTO, ReaderUpdateDTO
from .services import ReaderServiceAsync
from .depends import db_session, pagination_params_dep

router = APIRouter(tags=['Reader'], prefix='/reader')

@router.get('/', description='Вывод всех читателей')
async def get_all_readers(request: Request, session: db_session, pagination_params: pagination_params_dep):
    result = await ReaderServiceAsync(db_session=session, request=request).select_all_records(pagination_params)
    return result

@router.get('/relation-ship', description='Вывод всех читателей с отношениями между таблицами')
async def get_all_readers_rel(request: Request, session: db_session, pagination_params: pagination_params_dep):
    result = await ReaderServiceAsync(db_session=session, request=request).select_all_records_rel(pagination_params)
    return result

@router.get('/{reader_id}/relation-ship', description='Вывод читателя по id с отношениями между таблицами')
async def get_reader_by_id_rel(reader_id: int, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).select_record_id_rel(reader_id)
    return result

@router.get('/{reader_id}', description='Вывод читателя по id')
async def get_reader_by_id(reader_id: int, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).select_record_id(reader_id)
    return result

@router.put('/refresh-password', description='Обновить пароль читателя')
async def refresh_password(id_reader: int, old_password: str, new_password: str, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).refresh_password(id_reader, old_password, new_password)
    return {'message': f'Для читателя с id: {result} был обновлен пароль'}

@router.post('/', description='Добавить читателя')
async def create_reader(reader: ReaderCreateDTO, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).create_record(reader)
    return {'message': f'Читатель с id: {result} успешно добавлен в бд'}


@router.put('/{reader_id}', description='Обновить читателя')
async def update_reader_by_id(reader: ReaderUpdateDTO, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).update_record(reader)
    return {'message': f'Читатель с id: {result} успешно обновлен в бд'}


@router.delete('/{reader_id}', description='Удалить читателя по id')
async def delete_reader_by_id(reader_id, request: Request, session: db_session):
    result = await ReaderServiceAsync(db_session=session, request=request).delete_record(reader_id)
    return {'message': f'Читатель с id: {result} успешно удален в бд'}