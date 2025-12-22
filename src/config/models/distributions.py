from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Index, CheckConstraint
from ..database import Base
from .users import *

class Distributions(Base):
    __tablename__ = 'distributions'
    id: Mapped[int] = mapped_column(primary_key=True)
    books_id: Mapped[int] = mapped_column(ForeignKey('books.id', ondelete='CASCADE'))
    readers_id: Mapped[int] = mapped_column(ForeignKey('readers.id', ondelete='CASCADE'))
    seller_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    total_amount: Mapped[float]
    seller: Mapped["Users"] = relationship(back_populates='distribution')

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='total_amount_is_positive'),
    )

    def get_model_attributes(self):
        attrs = {'books_id': self.books_id, 'readers_id': self.readers_id, 'seller_id': self.seller_id, 'total_amount': self.total_amount}
        return attrs