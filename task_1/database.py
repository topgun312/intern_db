from datetime import datetime

from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER
from sqlalchemy import (
    Column,
    DateTime,
    Engine,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    create_engine,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker


def connect_db() -> Engine:
    """
    Функция для создания пула соединения
    """
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,
        echo=True,
    )
    return engine


Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=connect_db())
session = Session()


class Genre(Base):
    """
    Модель жанра книги
    """

    __tablename__ = "genre_table"
    id = Column(Integer(), primary_key=True)
    name_genre = Column(String(50), nullable=False)
    book = relationship("Book", backref="genre")


class Author(Base):
    """
    Модель автора
    """

    __tablename__ = "author_table"
    id = Column(Integer(), primary_key=True)
    name_author = Column(String(50), nullable=False)
    book = relationship("Book", backref="author")


class City(Base):
    """
    Модель города клиента
    """

    __tablename__ = "city_table"
    id = Column(Integer(), primary_key=True)
    name_city = Column(String(50), nullable=False)
    days_delivery = Column(Integer(), nullable=False)
    client = relationship("Client", backref="city")


class Book(Base):
    """
    Модель книги
    """

    __tablename__ = "book_table"
    id = Column(Integer(), primary_key=True)
    title = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    amount = Column(Integer(), nullable=False)
    author_id = Column(Integer(), ForeignKey("author_table.id"))
    genre_id = Column(Integer(), ForeignKey("genre_table.id"))
    buys = relationship("BuyBook", backref="book")


class Client(Base):
    """
    Модель клиента
    """

    __tablename__ = "client_table"
    id = Column(Integer(), primary_key=True)
    name_client = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    city_id = Column(Integer(), ForeignKey("city_table.id"))
    buy = relationship("Buy", backref="client")


class Buy(Base):
    """
    Модель заказа (покупки)
    """

    __tablename__ = "buy_table"
    id = Column(Integer(), primary_key=True)
    buy_description = Column(Text(), nullable=False)
    client_id = Column(Integer(), ForeignKey("client_table.id"))
    books = relationship("BuyBook", backref="buy")
    steps = relationship("BuyStep", backref="buy")


class Step(Base):
    """
    Модель этапов обработки заказов клиента
    """

    __tablename__ = "step_table"
    id = Column(Integer(), primary_key=True)
    name_step = Column(String(50), nullable=False)
    buys = relationship("BuyStep", backref="step")


class BuyBook(Base):
    """
    Модель связывающая заказ и книгу
    """

    __tablename__ = "buy_book_table"
    id = Column(Integer(), primary_key=True)
    amount = Column(Integer(), nullable=False)
    buy_id = Column(Integer(), ForeignKey("buy_table.id"))
    book_id = Column(Integer(), ForeignKey("book_table.id"))


class BuyStep(Base):
    """
    Модель связывающая заказ и этап обработки заказов клиента
    """

    __tablename__ = "buy_step_table"
    id = Column(Integer(), primary_key=True)
    date_step_beg = Column(DateTime(), default=datetime.now)
    date_step_end = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    buy_id = Column(Integer(), ForeignKey("buy_table.id"))
    step_id = Column(Integer(), ForeignKey("step_table.id"))


def create_db() -> None:
    """
    Функция для создания таблиц БД
    """
    try:
        engine = connect_db()
        Base.metadata.create_all(engine)
        print("Таблицы БД успешно созданы!")
    except Exception as ex:
        print("Ошибка создания БД: " + str(ex))


if __name__ == "__main__":
    create_db()
