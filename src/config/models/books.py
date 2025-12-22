from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..database import Base
from datetime import datetime

class Publishers(Base):
    __tablename__ = 'publisher'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    year_foundation: Mapped[int]
    description: Mapped[str] = mapped_column(default='', server_default='')

class Genres(Base):
    __tablename__ = 'genres'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]

class Books(Base):
    __tablename__ = "books"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str]
    name: Mapped[str]
    publisher: Mapped[int] = mapped_column(ForeignKey('publisher.id', ondelete='CASCADE'))
    year_writing: Mapped[int]
    price: Mapped[float]
    discount: Mapped[float] = mapped_column(default=0)
    author: Mapped[str]
    count_page: Mapped[int]
    genres: Mapped[int] = mapped_column(ForeignKey('genres.id', ondelete='CASCADE'))

    def get_model_attributes(self):
        attrs = {'slug': self.slug, 'name': self.name, 'publisher': self.publisher, 'year_writing': self.year_writing,
                 'price': self.price, 'discount': self.discount, 'author': self.author, 'count_page': self.count_page, 'genres': self.genres}
        return attrs