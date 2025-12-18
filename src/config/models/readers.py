from sqlalchemy.orm import Mapped, mapped_column
from ..database import Base
from .person import Person

class Readers(Person, Base):
    __tablename__ = 'readers'
    gender: Mapped[str] = mapped_column(default='m')
    discount: Mapped[float] = mapped_column(default=0)