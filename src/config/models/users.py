from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
from enum import Enum
from .person import Person

class Role(Enum):
    ADMIN = 'admin'
    USER = 'users'

class Post(Enum):
    ACCOUNTANT = 'accountant'
    MANAGER = 'manager'
    DIRECTOR = 'director'

class Workload(Enum):
    PARTTIME = 'parttime'
    FULLTIME = 'fulltime'

class Users(Person, Base):
    __tablename__ = 'users'
    workload: Mapped["Workload"] = mapped_column(default=Workload.PARTTIME)
    salary: Mapped[float] = mapped_column(default=0)
    role: Mapped["Role"] = mapped_column(default=Role.USER)
    post: Mapped["Post"] = mapped_column(default=Post.MANAGER)
    bonus: Mapped[float] = mapped_column(default=0)
    address: Mapped[str]

    def get_model_attributes(self):
        attrs = super().get_model_attributes()
        attrs.update({'workload': self.workload, 'salary': self.salary,
                      'role': self.role, 'post': self.post,
                      'bonus': self.bonus, 'address': self.address})
        return attrs