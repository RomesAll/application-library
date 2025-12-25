from fastapi import APIRouter, Request
from src.config.schemas.schemas import *
from .services import DistributionServiceAsync
from .depends import db_session, pagination_params_dep
from src.config import settings

router = APIRouter(tags=['Distribution'], prefix='/distribution')

@router.get('/', description='Вывод всех продаж')
async def get_all_distribution(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[DistributionGetDTO]:
    result = await DistributionServiceAsync(db_session=session, request=request).select_all_distributions(pagination_params)
    return {'message': result}


@router.get('/{distribution_id}', description='Вывод продаж по id')
async def get_distribution_by_id(distribution_id: int, request: Request, session: db_session):
    result = await DistributionServiceAsync(db_session=session, request=request).select_distribution_by_id(distribution_id)
    return {'message': result}


@router.post('/', description='Добавить продажу')
async def create_distribution(distribution: DistributionCreateDTO, request: Request, session: db_session):
    result = await DistributionServiceAsync(db_session=session, request=request).create_distribution(distribution)
    return {'message': f'Информация о продаже с id: {result} успешно добавлен в бд'}


@router.put('/{distribution_id}', description='Обновить продажу')
async def update_distribution_by_id(distribution: DistributionUpdateDTO, request: Request, session: db_session):
    result = await DistributionServiceAsync(db_session=session, request=request).update_distribution(distribution)
    return {'message': f'Информация о продаже с id: {result} успешно обновлен в бд'}


@router.delete('/{distribution_id}', description='Удалить продажу по id')
async def delete_distribution_by_id(distribution_id, request: Request, session: db_session) -> DistributionDeleteDTO:
    result = await DistributionServiceAsync(db_session=session, request=request).delete_distribution(distribution_id)
    return {'message': f'Информация о продаже с id: {result} успешно удален в бд'}