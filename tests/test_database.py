import pytest
from src.config.models import *
from src.config import settings, Base, engine_sync
from sqlalchemy import text
from contextlib import nullcontext
from sqlalchemy.exc import DataError
from psycopg.errors import InvalidTextRepresentation

@pytest.fixture(scope="session", autouse=True)
def setup_db():
    Base.metadata.drop_all(engine_sync)
    Base.metadata.create_all(engine_sync)
    yield
    Base.metadata.drop_all(engine_sync)

@pytest.fixture(scope="module", autouse=True)
def default_records():
    with engine_sync.connect() as connection:
        pub = text("INSERT INTO publisher(name, year_foundation, description) VALUES ('Издатель2', '2011', 'sadas')")
        ganres = text("INSERT INTO genres(name) VALUES ('Жанр1'), ('Жанр2')")
        books = text("INSERT INTO books(slug, name, publisher, year_writing, price, discount, author, count_page, genres) "
                     "VALUES ('book1', 'Книга1', '1', '2018', '3245', '0', 'Автор1', '40', 1), "
                             "('book2', 'Книга2', '1', '2008', '3245', '0', 'Автор1', '40', 2), "
                             "('book3', 'Книга3', '1', '2001', '3245', '0', 'Автор2', '40', 2), "
                             "('book4', 'Книга4', '1', '2020', '3245', '0', 'Автор4', '40', 1)")
        users = text("INSERT INTO users(fio, phone_number, email, password, address, workload, salary, role, post, bonus) "
                     "VALUES ('user1', '+790213213', 'user1@gmail.com', '123', 'addres', 'PARTTIME', '10000', 'USER', 'MANAGER', '0'), "
                            "('user2', '+790213213', 'user2@gmail.com', 'qwerty', 'addres', 'PARTTIME', '10000', 'USER', 'MANAGER', '0')")
        readers = text("INSERT INTO readers(fio, phone_number, email, password, address, gender, discount) "
                     "VALUES ('readers1', '+790213234', 'readers1@gmail.com', 'sadfasd', 'address1', 'm', '0'), "
                            "('readers2', '+790213234', 'readers2@gmail.com', 'fdg345', 'address2', 'w', '0')")
        distributions = text("INSERT INTO distributions(books_id, readers_id, seller_id, total_amount) "
                             "VALUES ('1','1','1','10000'),"
                             "('1','1','1','2000'),"
                             "('2','2','2','500'),"
                             "('3','2','2','980')")
        connection.execute(pub)
        connection.execute(ganres)
        connection.execute(books)
        connection.execute(users)
        connection.execute(readers)
        connection.execute(distributions)
        connection.commit()

@pytest.mark.parametrize("name, year_foundation, description, exception",
                         [('test', '2020', '', nullcontext()),
                          ('test2', '2013', 'testsdfa', nullcontext()),
                          ('test3', 'sadfasdf', 'testsdfa', pytest.raises(Exception))])
def test_create_records_for_pub(name, year_foundation, description, exception):
    with exception:
        with engine_sync.connect() as connection:
            stmt = text("INSERT INTO publisher(name, year_foundation, description) VALUES (:name,:year_foundation,:description)")
            connection.execute(stmt, {"name": name, "year_foundation": year_foundation, "description": description})


@pytest.mark.parametrize("slug, name, publisher, year_writing, price, discount, author, count_page, genres, exception",
                         [('book1', 'name1', '1', '2001', '124', '0', 'author1', '132', '1', nullcontext()),
                          ('book1', 'name2', '1', '2004', '544', '0', 'author2', '32', '1', nullcontext()),
                          ('book1', 'name3', '1', 'dasf', '345', '0', 'author3', '43', '2', pytest.raises(Exception)),
                          ('book1', 'name4', 'sdafas', 'dsaf', '65', '0', 'author', '56', '2', pytest.raises(Exception))])
def test_create_records_for_books(slug, name, publisher, year_writing, price, discount, author, count_page, genres, exception):
    with exception:
        with engine_sync.connect() as connection:
            stmt = text("INSERT INTO books(slug, name, publisher, year_writing, price, discount, author, count_page, genres) "
                        "VALUES (:slug, :name, :publisher, :year_writing, :price, :discount, :author, :count_page, :genres)")
            connection.execute(stmt, {"slug": slug, "name": name, "publisher": publisher,
                                      "year_writing": year_writing, "price": price,
                                      "discount": discount, "author": author,
                                      "count_page": count_page,"genres": genres})

@pytest.mark.parametrize("fio, phone_number, email, password, address, gender, discount, exception",
                         [('fio1', '+7902324', 'test', '123', 'sadf', 'm', '0', nullcontext()),
                          ('fio2', '+7902324', 'test', '123', 'sadf', 'm', '0', nullcontext()),
                          ('fio4', '+7902324', 'test', '123', 'sadf', 'm', '0', nullcontext()),
                          ('fio6', '+7902324', 'test', '123', 'sadf', 'm', '0', nullcontext())])
def test_create_records_for_readers(fio, phone_number, email, password, address, gender, discount, exception):
    with exception:
        with engine_sync.connect() as connection:
            stmt = text("INSERT INTO readers(fio, phone_number, email, password, address, gender, discount) "
                        "VALUES (:fio, :phone_number, :email, :password, :address, :gender, :discount)")
            connection.execute(stmt, {'fio': fio, 'phone_number': phone_number, 'email': email,
                                      'password': password, 'address': address, 'gender': gender, 'discount': discount})

@pytest.mark.parametrize("fio, phone_number, email, password, address, workload, salary, role, post, bonus, exception",
                         [('fio1', '+7902324', 'test', '123', 'sadf', 'PARTTIME', '0', 'USER', 'MANAGER', '0', nullcontext()),
                          ('fio2', '+7902324', 'test', '123', 'sadf', 'PARTTIME', '0', 'USER', 'MANAGER', '0', nullcontext()),
                          ('fio4', '+7902324', 'test', '123', 'sadf', 'PARTTIME', 'FDGSDFG', 'USER', 'MANAGER', '0', pytest.raises(Exception)),
                          ('fio5', '+7902324', 'test', '123', 'sadf', 'PARTTIME', '0', 'USER', 'MANAGER', '0', nullcontext())])
def test_create_records_for_users(fio, phone_number, email, password, address, workload, salary, role, post, bonus, exception):
    with exception:
        with engine_sync.connect() as connection:
            stmt = text("INSERT INTO users(fio, phone_number, email, password, address, workload, salary, role, post, bonus) "
                        "VALUES (:fio, :phone_number, :email, :password, :address, :workload, :salary, :role, :post, :bonus)")
            connection.execute(stmt, {'fio': fio, 'phone_number': phone_number, 'email': email,
                                      'password': password, 'address': address, 'workload': workload, 'salary': salary,
                                      'role': role, 'post': post, 'bonus': bonus})

@pytest.mark.parametrize("books_id, readers_id, seller_id, total_amount, exception",
                         [('1', '1', '1', '32452', nullcontext()),
                          ('2', '1', '2', '43453', nullcontext()),
                          ('3', '2', '1', '4536', nullcontext()),
                          ('4', 'dsf', '2', '132423', pytest.raises(Exception))])
def test_create_records_for_distrib(books_id, readers_id, seller_id, total_amount, exception):
    with exception:
        with engine_sync.connect() as connection:
            stmt = text("INSERT INTO distributions(books_id, readers_id, seller_id, total_amount) "
                        "VALUES (:books_id, :readers_id, :seller_id, :total_amount)")
            connection.execute(stmt, {'books_id': books_id, 'readers_id': readers_id, 'seller_id': seller_id, 'total_amount': total_amount})