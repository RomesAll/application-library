from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, CheckConstraint
from ..database import Base
from .books import *
from ..mixin.person_mixin import PersonMixin

class Readers(PersonMixin, Base):
    __tablename__ = 'readers'
    gender: Mapped[str] = mapped_column(default='m')
    discount: Mapped[float] = mapped_column(default=0)

    books: Mapped[list["Books"]] = relationship(back_populates='readers', secondary='distributions')
    distributions: Mapped[list["Distributions"]] = relationship(back_populates='reader')

    __table_args__ = (
        Index('readers_index', 'gender', 'fio', 'phone_number', 'email'),
        CheckConstraint('discount >= 0 and discount <= 100', 'discount_is_positive'),
    )

    def get_model_attr_without_relations(self):
        attrs = super().get_model_attr_without_relations()
        attrs.update({'gender': self.gender, 'discount': self.discount})
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'books': self.books, 'distributions': self.distributions})
        return attrs