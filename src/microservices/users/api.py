from fastapi import APIRouter, Request
from .schemas import *
from .services import UserServiceAsync
from .depends import db_session, pagination_params_dep

router = APIRouter(tags=['User'], prefix='/user')

@router.get('/', description='Вывод всех сотрудников')
async def get_all_users(request: Request, session: db_session, pagination_params: pagination_params_dep):
    result = await UserServiceAsync(db_session=session, request=request).select_all_records(pagination_params)
    return {'message': result}

@router.get('/relation-ship', description='Вывод всех сотрудников с отношениями между таблицами')
async def get_all_users_rel(request: Request, session: db_session, pagination_params: pagination_params_dep):
    result = await UserServiceAsync(db_session=session, request=request).select_all_records_rel(pagination_params)
    return {'message': result}

@router.get('/{user_id}/relation-ship', description='Вывод сотрудника по id с отношениями между таблицами')
async def get_user_id_rel(user_id: int, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).select_record_id_rel(user_id)
    return {'message': result}

@router.get('/{user_id}', description='Вывод сотрудника по id')
async def get_user_id(user_id: int, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).select_record_id(user_id)
    return {'message': result}

@router.put('/refresh-password', description='Обновить пароль сотрудника')
async def refresh_password(id_user: int, old_password: str, new_password: str, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).refresh_password(id_user, old_password, new_password)
    return {'message': f'Для сотрудника с id: {result} был обновлен пароль'}

@router.post('/', description='Добавить сотрудника')
async def create_user(user: UserCreateDTO, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).create_record(user)
    return {'message': f'Сотрудник с id: {result} успешно добавлен в бд'}

@router.put('/', description='Обновить сотрудника')
async def update_user_by_id(user: UserUpdateDTO, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).update_record(user)
    return {'message': f'Сотрудник с id: {result} успешно обновлен в бд'}

@router.delete('/{user_id}', description='Удалить сотрудника по id')
async def delete_user_by_id(user_id, request: Request, session: db_session):
    result = await UserServiceAsync(db_session=session, request=request).delete_record(user_id)
    return {'message': f'Сотрудник с id: {result} успешно удален в бд'}