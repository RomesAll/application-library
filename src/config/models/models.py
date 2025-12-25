from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, CheckConstraint
from ..database import Base
from ..mixin.person_mixin import PersonMixin
from enum import Enum

class Role(Enum):
    ADMIN = 'ADMIN'
    USER = 'USER'

class Post(Enum):
    ACCOUNTANT = 'ACCOUNTANT'
    MANAGER = 'MANAGER'
    DIRECTOR = 'DIRECTOR'

class Workload(Enum):
    PARTTIME = 'PARTTIME'
    FULLTIME = 'FULLTIME'

class Publishers(Base):
    __tablename__ = 'publishers_orm'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    year_foundation: Mapped[int]
    description: Mapped[str] = mapped_column(default='', server_default='')

class Genres(Base):
    __tablename__ = 'genres_orm'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)

class Books(Base):
    __tablename__ = "books_orm"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    slug: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(unique=True)
    publishers_id: Mapped[int] = mapped_column(ForeignKey('publishers_orm.id', ondelete='CASCADE'))
    year_writing: Mapped[int]
    price: Mapped[float]
    discount: Mapped[float] = mapped_column(default=0)
    author: Mapped[str]
    count_page: Mapped[int]
    genres_id: Mapped[int] = mapped_column(ForeignKey('genres_orm.id', ondelete='CASCADE'))

    readers: Mapped[list["Readers"]] = relationship(back_populates='books', secondary='distributions_orm')
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
                 'count_page': self.count_page, 'genres': self.genres_id}
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'readers': self.readers, 'distributions': self.distributions})
        return attrs

class Distributions(Base):
    __tablename__ = 'distributions_orm'
    id: Mapped[int] = mapped_column(primary_key=True)
    books_id: Mapped[int] = mapped_column(ForeignKey('books_orm.id', ondelete='CASCADE'))
    readers_id: Mapped[int] = mapped_column(ForeignKey('readers_orm.id', ondelete='CASCADE'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users_orm.id', ondelete='CASCADE'))
    total_amount: Mapped[float]

    seller: Mapped["Users"] = relationship(back_populates='distributions')
    book: Mapped["Books"] = relationship(back_populates='distributions')
    reader: Mapped["Readers"] = relationship(back_populates='distributions')

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='total_amount_is_positive'),
    )

    def get_model_attr_without_relations(self):
        attrs = {'id': self.id, 'books_id': self.books_id, 'readers_id': self.readers_id,
                 'seller_id': self.seller_id, 'total_amount': self.total_amount}
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'seller': self.seller, 'book': self.book, 'reader': self.reader})
        return attrs

class Readers(PersonMixin, Base):
    __tablename__ = 'readers_orm'
    gender: Mapped[str] = mapped_column(default='m')
    discount: Mapped[float] = mapped_column(default=0)

    books: Mapped[list["Books"]] = relationship(back_populates='readers', secondary='distributions_orm')
    distributions: Mapped[list["Distributions"]] = relationship(back_populates='reader')

    __table_args__ = (
        Index('readers_index', 'gender', 'fio', 'phone_number', 'email'),
        CheckConstraint('discount >= 0 and discount <= 100', 'discount_is_positive'),
    )

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'books': self.books, 'distributions': self.distributions})
        return attrs

    def get_model_attr_without_relations(self):
        attrs = super().get_model_attr_without_relations()
        attrs.update({'gender': self.gender, 'discount': self.discount})
        return attrs

class Users(PersonMixin, Base):
    __tablename__ = 'users_orm'
    workload: Mapped["Workload"] = mapped_column(default=Workload.PARTTIME)
    salary: Mapped[float] = mapped_column(default=0)
    role: Mapped["Role"] = mapped_column(default=Role.USER)
    post: Mapped["Post"] = mapped_column(default=Post.MANAGER)
    bonus: Mapped[float] = mapped_column(default=0)
    address: Mapped[str]

    distributions: Mapped[list["Distributions"]] = relationship(back_populates='seller')

    __table_args__ = (
        Index('users_index', 'workload', 'salary', 'address', 'fio', 'phone_number', 'email'),
        CheckConstraint('salary >= 0', 'salary_is_positive'),
        CheckConstraint('bonus >= 0', 'bonus_is_positive'),
    )

    def get_model_attr_without_relations(self):
        attrs = super().get_model_attr_without_relations()
        attrs.update({'workload': self.workload, 'salary': self.salary,
                      'role': self.role, 'post': self.post,
                      'bonus': self.bonus, 'address': self.address})
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'distributions': self.distributions})
        return attrs