from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from ..database import Base

class Distributions(Base):
    __tablename__ = 'distributions'
    id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True)
    books_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'))
    readers_id: Mapped[int] = mapped_column(ForeignKey('readers.id', ondelete='CASCADE'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_amount: Mapped[float]
