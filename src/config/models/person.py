from sqlalchemy.orm import Mapped, mapped_column

class Person:
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    fio: Mapped[str]
    phone_number: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
    address: Mapped[str]