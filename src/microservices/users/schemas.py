from pydantic import BaseModel, field_validator, Field, ConfigDict
from datetime import datetime, timezone
from src.config.models import Workload, Role, Post
import re

class UserCreateDTO(BaseModel):
    fio: str = Field(default='default_fio', min_length=5, max_length=50, examples=['Петров П.В.', 'Петров Петр Владимирович'], description='ФИО сотрудника')
    phone_number: str = Field(default='default_phone_number', examples=['+79021348294', '89021348295'], description='Номер телефона сотрудника')
    email: str = Field(default='default_email', examples=['test@gmail.com'], description='Email сотрудника')
    password: bytes = Field(default=b'default_password')
    workload: Workload = Field(default='default_workload', examples=['PARTTIME', 'FULLTIME'],description='Рабочая нагрузка сотрудника')
    salary: float = Field(default='default_salary', examples=['0'], ge=0, description='Зарплата сотрудника')
    role: Role = Field(default='default_role', examples=['ADMIN','USER'], description='Зарплата сотрудника')
    post: Post = Field(default='default_post', examples=['ACCOUNTANT','MANAGER', 'DIRECTOR'], description='Должность сотрудника')
    bonus: float = Field(default='default_bonus', ge=0, examples=['0'], description='Премия сотрудника')
    address: str =Field(default='default_address', examples=['г. Москва ул. Пушкина д.3 кв.123'], description='Адрес сотрудника')
    model_config = ConfigDict(from_attributes=True)

    @field_validator('phone_number')
    def phone_number_validator(cls, v):
        result = re.fullmatch(r'(\+7|8)( ?[(-]?\d{3}[)-]? ?)(\d{3})([ -]?\d{2}){2}', v)
        if result is None:
            raise ValueError('Неверный формат телефона')
        return v

    @field_validator('email')
    def email_validator(cls, v):
        result = re.fullmatch(r'\S+@[a-z]{2,7}\.[a-z]{1,7}', v)
        if result is None:
            raise ValueError('Неверный формат почты')
        return v

class UserGetDTO(UserCreateDTO):
    id: int = Field(..., ge=0, description='Id сотрудника')
    password: bytes = Field(default=b'default_password', exclude=True)
    created_at: datetime
    updated_at: datetime

class UserUpdateDTO(UserCreateDTO):
    id: int = Field(..., ge=0, description='Id сотрудника')

class UserDeleteDTO(UserGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')

class UserRelGetDTO(UserGetDTO):
    distributions: list['DistributionGetDTO']