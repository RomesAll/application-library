from pydantic import BaseModel, field_validator, Field, ConfigDict, computed_field
from datetime import datetime, timezone
from src.config.models.models import Workload, Role, Post
import re

compliance_table = {
            'а': 'a', 'б': 'b', 'в': 'w', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z',
            'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
            'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'ts', 'ч': 'ch','ш': 'sh', 'щ': 'sch',
            'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', ' ': '-'
        }

class BookCreateDTO(BaseModel):
    name: str = Field(default='default_name', min_length=5, max_length=200, examples=['Евгений Онегин'], description='Названия книги')
    publishers_id: int = Field(default='default_publisher', examples=['1'], description='Издатель книги')
    year_writing: int = Field(default='default_year_writing', ge=2, examples=['1833'], description='Год написания книги')
    price: float = Field(default='default_price', ge=0, examples=['890'], description='Цена книги')
    discount: float = Field(default='default_discount', ge=0, le=100, examples=['10'], description='Скидка на книги')
    author: str = Field(default='default_author', examples=['Александр Сергеевич Пушкин'], description='Автор книги')
    count_page: int = Field(default='default_count_page', ge=1, examples=['80'], description='Кол-во страниц книги')
    genres_id: int = Field(default='default_genres', ge=0, examples=['1'], description='Жанр книги')
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    def slug(self) -> str:
        slug = ''.join([compliance_table.get(ch, ch) for ch in self.name.lower()])
        return slug

class DistributionCreateDTO(BaseModel):
    books_id: int = Field(default='default_books_id', examples=['1'], description='Номер книги')
    readers_id: int = Field(default='default_readers_id', examples=['1'], description='Номер читателя')
    seller_id: int = Field(default='default_seller_id', examples=['1'], description='Номер сотрудника')
    total_amount: float = Field(default='default_total_amount', examples=['1000'], description='Конечная сумма за книгу')
    model_config = ConfigDict(from_attributes=True)

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

class BookGetDTO(BookCreateDTO):
    id: int = Field(..., ge=0, description='Id книги')
    created_at: datetime
    updated_at: datetime

class DistributionGetDTO(DistributionCreateDTO):
    id: int = Field(..., ge=0, description='Id продажи')
    created_at: datetime
    updated_at: datetime

class ReaderGetDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')
    password: bytes = Field(default=b'default_password', exclude=True)
    created_at: datetime
    updated_at: datetime

class UserGetDTO(UserCreateDTO):
    id: int = Field(..., ge=0, description='Id сотрудника')
    password: bytes = Field(default=b'default_password', exclude=True)
    created_at: datetime
    updated_at: datetime

class BookUpdateDTO(BookCreateDTO):
    id: int = Field(..., ge=0, description='Id книги')

class ReaderUpdateDTO(ReaderCreateDTO):
    id: int = Field(..., ge=0, description='Id читателя')

class UserUpdateDTO(UserCreateDTO):
    id: int = Field(..., ge=0, description='Id сотрудника')

class DistributionUpdateDTO(DistributionCreateDTO):
    id: int = Field(..., ge=0, description='Id продажи')

class UserDeleteDTO(UserGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class BookDeleteDTO(BookGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class DistributionDeleteDTO(DistributionGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class ReaderDeleteDTO(ReaderGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class BookRelGetDTO(BookGetDTO):
    readers: list[ReaderGetDTO]
    distributions: list[DistributionGetDTO]

class UserRelGetDTO(UserGetDTO):
    distributions: list[DistributionGetDTO]

class ReaderRelGetDTO(ReaderGetDTO):
    books: list[BookGetDTO]
    distributions: list[DistributionGetDTO]

class DistributionRelGetDTO(DistributionGetDTO):
    seller: UserGetDTO
    book: BookGetDTO
    reader: ReaderGetDTO

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')