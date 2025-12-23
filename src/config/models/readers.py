from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Index, CheckConstraint
from ..database import Base
from .person import Person
from ..mixin.json_mixin import JsonMixinHelper
from .books import *

class Readers(Person, Base, JsonMixinHelper):
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
        attrs.update({'gender': self.gender, 'discount': self.discount,
                      'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat()})
        self._delete_private_attrs_helper(attrs)
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'books': self.books, 'distributions': self.distributions})
        self._delete_private_attrs_helper(attrs)
        return attrs