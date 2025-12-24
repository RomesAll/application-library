from fastapi import APIRouter, Request, middleware
from .schemas import ReaderCreateDTO, ReaderGetDTO, ReaderUpdateDTO, ReaderDeleteDTO
from .services import ReaderService
from .depends import db_session, pagination_params_dep
from src.config import settings

router = APIRouter(tags=['Reader'], prefix='/reader')

@router.get('/', description='Вывод всех читателей')
async def get_all_readers(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[ReaderGetDTO]:
    result = await ReaderService(db_session=session, request=request).select_all_reader_async(pagination_params)
    return result

@router.get('/rel', description='Вывод всех читателей rel')
async def get_all_rel_readers(request: Request, session: db_session, pagination_params: pagination_params_dep):
    result = await ReaderService(db_session=session, request=request).select_all_reader_rel_async(pagination_params)
    return result

@router.get('/{reader_id}', description='Вывод читателя по id')
async def get_reader_by_id(reader_id: int, request: Request, session: db_session):
    result = await ReaderService(db_session=session, request=request).select_reader_by_id_async(reader_id)
    return result


@router.post('/', description='Добавить читателя')
async def create_reader(reader: ReaderCreateDTO, request: Request, session: db_session):
    result = await ReaderService(db_session=session, request=request).create_reader_async(reader)
    return result


@router.put('/{reader_id}', description='Обновить читателя')
async def update_reader_by_id(reader: ReaderUpdateDTO, request: Request, session: db_session):
    result = await ReaderService(db_session=session, request=request).update_reader_async(reader)
    return result


@router.delete('/{reader_id}', description='Удалить читателя по id')
async def delete_reader_by_id(reader_id, request: Request, session: db_session) -> ReaderDeleteDTO:
    result = await ReaderService(db_session=session, request=request).delete_reader_async(reader_id)
    return result