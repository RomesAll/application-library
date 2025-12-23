from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, CheckConstraint
from ..database import Base
from .readers import *

class Publishers(Base):
    __tablename__ = 'publishers'
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
    publishers_id: Mapped[int] = mapped_column(ForeignKey('publishers.id', ondelete='CASCADE'))
    year_writing: Mapped[int]
    price: Mapped[float]
    discount: Mapped[float] = mapped_column(default=0)
    author: Mapped[str]
    count_page: Mapped[int]
    genres_id: Mapped[int] = mapped_column(ForeignKey('genres.id', ondelete='CASCADE'))

    readers: Mapped[list["Readers"]] = relationship(back_populates='books', secondary='distributions')
    distributions: Mapped[list["Distributions"]] = relationship(back_populates='book')

    __table_args__ = (
        Index('books_index', 'name', 'slug'),
        CheckConstraint('price >= 0', name='price_is_positive'),
        CheckConstraint('discount >= 0 and discount <= 100', name='discount_beetween_0_and_100'),
        CheckConstraint('count_page >= 0', name='count_page_is_positive')
    )

    def get_model_attr_without_relations(self):
        attrs = {'id': self.id, 'slug': self.slug,
                 'name': self.name, 'publishers': self.publishers_id,
                 'year_writing': self.year_writing, 'price': self.price,
                 'discount': self.discount, 'author': self.author,
                 'count_page': self.count_page, 'genres': self.genres_id,
                 'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat()}
        self._delete_private_attrs_helper(attrs)
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'readers': self.readers, 'distributions': self.distributions})
        self._delete_private_attrs_helper(attrs)
        return attrs