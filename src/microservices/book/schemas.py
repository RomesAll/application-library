from pydantic import BaseModel, Field, ConfigDict, computed_field
from datetime import datetime, timezone

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

class BookGetDTO(BookCreateDTO):
    id: int = Field(..., ge=0, description='Id книги')
    created_at: datetime
    updated_at: datetime

class BookUpdateDTO(BookCreateDTO):
    id: int = Field(..., ge=0, description='Id книги')

class BookDeleteDTO(BookGetDTO):
    deleted_at: datetime = Field(default=datetime.now(tz=timezone.utc))

class PaginationParams(BaseModel):
    limit: int = Field(100, ge=0, le=100, description='Кол-во выводимых записей')
    offset: int = Field(0, ge=0, description='Смещение')

class BookRelGetDTO(BookGetDTO):
    readers: list['ReaderGetDTO']
    distributions: list['DistributionGetDTO']