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

    seller: Mapped["Users"] = relationship(back_populates='distributions')
    book: Mapped["Books"] = relationship(back_populates='distributions')
    reader: Mapped["Readers"] = relationship(back_populates='distributions')

    __table_args__ = (
        CheckConstraint('total_amount >= 0', name='total_amount_is_positive'),
    )

    def get_model_attr_without_relations(self):
        attrs = {'id': self.id, 'books_id': self.books_id, 'readers_id': self.readers_id,
                 'seller_id': self.seller_id, 'total_amount': self.total_amount,
                 'created_at': self.created_at.isoformat(), 'updated_at': self.updated_at.isoformat()}
        self._delete_private_attrs_helper(attrs)
        return attrs

    def get_model_attr_with_relations(self):
        attrs = self.get_model_attr_without_relations()
        attrs.update({'seller': self.seller, 'book': self.book, 'reader': self.reader})
        self._delete_private_attrs_helper(attrs)
        return attrs