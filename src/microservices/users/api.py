from fastapi import APIRouter, Request
from .schemas import *
from .services import *
from .depends import db_session, pagination_params_dep

router = APIRouter(tags=['User'], prefix='/user')

@router.get('/', description='Вывод всех сотрудников')
async def get_all_users(request: Request, session: db_session, pagination_params: pagination_params_dep) -> list[UserGetDTO]:
    result = await UserService(db_session=session, request=request).select_all_user_async(pagination_params)
    return result


@router.get('/{user_id}', description='Вывод сотрудника по id')
async def get_user_by_id(user_id: int, request: Request, session: db_session):
    result = await UserService(db_session=session, request=request).select_user_by_id_async(user_id)
    return result


@router.post('/', description='Добавить сотрудника')
async def create_user(user: UserCreateDTO, request: Request, session: db_session):
    result = await UserService(db_session=session, request=request).create_user_async(user)
    return result


@router.put('/{user_id}', description='Обновить сотрудника')
async def update_user_by_id(user: UserUpdateDTO, request: Request, session: db_session):
    result = await UserService(db_session=session, request=request).update_user_async(user)
    return result


@router.delete('/{user_id}', description='Удалить сотрудника по id')
async def delete_user_by_id(user_id, request: Request, session: db_session) -> UserDeleteDTO:
    result = await UserService(db_session=session, request=request).delete_user_async(user_id)
    return result