from pydantic import BaseModel, field_validator, model_validator, Field
from fastapi import HTTPException
from datetime import datetime
import re

class ReaderCreateDTO(BaseModel):
    fio: str = Field(default='default_fio', min_length=5, max_length=50, examples=['Петров П.В.', 'Петров Петр Владимирович'], description='ФИО читателя')
    phone_number: str = Field(default='default_phone_number', examples=['+79021348294', '89021348295'], description='Номер телефона читателя')
    email: str = Field(default='default_email', examples=['test@gmail.com'], description='Email читателя')
    password: bytes = Field(default=b'default_password')
    gender: str = Field(default='default_gender', examples=['м', 'ж'], description='Пол читателя')
    discount: float = Field(default='default_discount', ge=0, le=100, examples=['0', '100'], description='Персональная скидка для читателя')

    @field_validator('phone_number')
    def phone_number_validator(cls, v):
        result = re.fullmatch(r'(\+7|8)( ?[(-]?\d{3}[)-]? ?)(\d{3})([ -]?\d{2}){2}', v)
        if result is None:
            raise HTTPException(status_code=400, detail='Неверный формат телефона')
        return v

    @field_validator('email')
    def email_validator(cls, v):
        result = re.fullmatch(r'\S+@[a-z]{2,7}\.[a-z]{1,7}', v)
        if result is None:
            raise HTTPException(status_code=400, detail='Неверный формат почты')
        return v

    @field_validator('gender')
    def gender_validator(cls, v):
        result = re.fullmatch(r'([wmMWМЖмж])(oman|man|an|ужской|енский)?', v)
        if result is None:
            raise HTTPException(status_code=400, detail='Неверный формат пола')
        return v

class ReaderGetDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')
    created_at: datetime
    updated_at: datetime

class ReaderUpdateDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')
