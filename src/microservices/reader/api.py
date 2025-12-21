from fastapi import APIRouter
from .schemas import ReaderCreateDTO, ReaderGetDTO, ReaderUpdateDTO, ReaderDeleteDTO
from .services import ReaderService
from .depends import db_session, pagination_params_dep
from src.config import settings

router = APIRouter(tags=['Reader'], prefix='/reader')

@router.get('/', description='Вывод всех читателей')
async def get_all_readers(session: db_session, pagination_params: pagination_params_dep):
    result = await ReaderService(db_session=session).select_all_reader_async(pagination_params)
    settings.logging.logger.debug('Вывод всех читателей')
    return result


@router.get('/{reader_id}', description='Вывод читателя по id')
async def get_reader_by_id(reader_id: int, session: db_session):
    result = await ReaderService(db_session=session).select_reader_by_id_async(reader_id)
    settings.logging.logger.debug('Вывод читателя по id')
    return result


@router.post('/', description='Добавить читателя')
async def create_reader(reader: ReaderCreateDTO, session: db_session):
    result = await ReaderService(db_session=session).create_reader_async(reader)
    settings.logging.logger.debug('Добавить читателя')
    return result


@router.put('/{reader_id}', description='Обновить читателя')
async def update_reader_by_id(reader: ReaderUpdateDTO, session: db_session):
    result = await ReaderService(db_session=session).update_reader_async(reader)
    settings.logging.logger.debug('Обновить читателя')
    return result


@router.delete('/{reader_id}', description='Удалить читателя по id')
async def delete_reader_by_id(reader_id, session: db_session):
    result = await ReaderService(db_session=session).delete_reader_async(reader_id)
    settings.logging.logger.debug('Удалить читателя по id')
    return result