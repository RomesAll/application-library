from pydantic import BaseModel, field_validator, Field, ConfigDict, model_validator, EmailStr
from datetime import datetime, timezone
import re

class ReaderCreateDTO(BaseModel):
    fio: str = Field(default='default_fio', min_length=5, max_length=50, examples=['Петров П.В.', 'Петров Петр Владимирович'], description='ФИО читателя')
    phone_number: str = Field(default='default_phone_number', examples=['+79021348294', '89021348295'], description='Номер телефона читателя')
    email: str = Field(default='default_email', examples=['test@gmail.com'], description='Email читателя')
    password: bytes = Field(default=b'default_password')
    gender: str = Field(default='default_gender', examples=['м', 'ж'], description='Пол читателя')
    discount: float = Field(default='default_discount', ge=0, le=100, examples=['0', '100'], description='Персональная скидка для читателя')
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

    @field_validator('gender')
    def gender_validator(cls, v):
        result = re.fullmatch(r'([wmMWМЖмж])(oman|man|an|ужской|енский)?', v)
        if result is None:
            raise ValueError('Неверный формат пола')
        return v

class ReaderGetDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')
    password: bytes = Field(default=b'default_password', exclude=True)
    created_at: datetime
    updated_at: datetime

class ReaderUpdateDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')

class ReaderDeleteDTO(ReaderGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')

class ReaderRelGetDTO(ReaderGetDTO):
    books: list['BookGetDTO']
    distributions: list['DistributionGetDTO']