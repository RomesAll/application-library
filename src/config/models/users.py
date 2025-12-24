from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from sqlalchemy import Index, CheckConstraint
from enum import Enum
from .distributions import *
from ..mixin.person_mixin import PersonMixin

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

class Users(PersonMixin, Base):
    __tablename__ = 'users'
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
                      'bonus': self.bonus, 'address': self.address,
                      'created_at': self.created_at, 'updated_at': self.updated_at})
        self._delete_private_attrs_helper(attrs)
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'distributions': self.distributions})
        self._delete_private_attrs_helper(attrs)
        return attrs