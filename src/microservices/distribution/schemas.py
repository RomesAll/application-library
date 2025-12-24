from pydantic import BaseModel, field_validator, Field, ConfigDict, computed_field
from datetime import datetime, timezone
from ..users.schemas import *
from ..book.schemas import *
from ..reader.schemas import *
import re

class DistributionCreateDTO(BaseModel):
    books_id: int = Field(default='default_books_id', examples=['1'], description='Номер книги')
    readers_id: int = Field(default='default_readers_id', examples=['1'], description='Номер читателя')
    seller_id: int = Field(default='default_seller_id', examples=['1'], description='Номер сотрудника')
    total_amount: float = Field(default='default_total_amount', examples=['1000'], description='Конечная сумма за книгу')
    model_config = ConfigDict(from_attributes=True)

class DistributionGetDTO(DistributionCreateDTO):
    id: int = Field(..., ge=0, description='Id продажи')
    created_at: datetime
    updated_at: datetime

class DistributionUpdateDTO(DistributionCreateDTO):
    id: int = Field(..., ge=0, description='Id продажи')

class DistributionDeleteDTO(DistributionGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')

class DistributionRelGetDTO(DistributionGetDTO):
    seller: 'UserGetDTO'
    book: 'BookGetDTO'
    reader: 'ReaderGetDTO'