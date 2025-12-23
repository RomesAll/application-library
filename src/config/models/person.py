from sqlalchemy.orm import Mapped, mapped_column

class Person:
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[bytes]

    def get_model_attr_without_relations(self):
        return {'id': self.id, 'fio': self.fio,
                'phone_number': self.phone_number, 'password': self.password, 'email': self.email}