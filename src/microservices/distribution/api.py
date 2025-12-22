from fastapi import APIRouter, Request, middleware
from .schemas import *
from .services import *
from .depends import db_session, pagination_params_dep
from src.config import settings

router = APIRouter(tags=['Distribution'], prefix='/distribution')

@router.get('/', description='Вывод всех продаж')
async def get_all_distribution(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[DistributionGetDTO]:
    result = await DistributionService(db_session=session, request=request).select_all_distribution_async(pagination_params)
    return result


@router.get('/{distribution_id}', description='Вывод продаж по id')
async def get_distribution_by_id(distribution_id: int, request: Request, session: db_session):
    result = await DistributionService(db_session=session, request=request).select_distribution_by_id_async(distribution_id)
    return result


@router.post('/', description='Добавить продажу')
async def create_distribution(distribution: DistributionCreateDTO, request: Request, session: db_session):
    result = await DistributionService(db_session=session, request=request).create_distribution_async(distribution)
    return result


@router.put('/{distribution_id}', description='Обновить продажу')
async def update_distribution_by_id(distribution: DistributionUpdateDTO, request: Request, session: db_session):
    result = await DistributionService(db_session=session, request=request).update_distribution_async(distribution)
    return result


@router.delete('/{distribution_id}', description='Удалить продажу по id')
async def delete_distribution_by_id(distribution_id, request: Request, session: db_session) -> DistributionDeleteDTO:
    result = await DistributionService(db_session=session, request=request).delete_distribution_async(distribution_id)
    return result