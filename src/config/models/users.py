from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..database import Base
from enum import Enum
from .person import Person
from .distributions import *

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

class Users(Person, Base):
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

    def get_model_attributes(self):
        attrs = super().get_model_attributes()
        attrs.update({'workload': self.workload, 'salary': self.salary,
                      'role': self.role, 'post': self.post,
                      'bonus': self.bonus, 'address': self.address})
        return attrs