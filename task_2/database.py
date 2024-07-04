from sqlalchemy import Column, DateTime, Engine, Integer, String, create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker

from task_2.config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER, logger


def connect_db() -> Engine:
    """
    Функция для создания пула соединения
    """
    engine = create_engine(
        f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
        pool_pre_ping=True,
    )
    return engine


Base = declarative_base()
Session = sessionmaker(autoflush=False, bind=connect_db())
session = Session()


class SpimexTradingResult(Base):
    """
    Модель для хранения данных по итогов торгов
    """

    __tablename__ = "spimex_trading_results"
    id = Column(Integer(), primary_key=True)
    exchange_product_id = Column(String(255), nullable=False)
    exchange_product_name = Column(String(255), nullable=False)
    oil_id = Column(String(255), nullable=False)
    delivery_basis_id = Column(String(255), nullable=False)
    delivery_basis_name = Column(String(255), nullable=False)
    delivery_type_id = Column(String(255), nullable=False)
    volume = Column(String(255), nullable=False, default="-")
    total = Column(String(255), nullable=False, default="-")
    count = Column(String(255), nullable=False, default="-")
    date = Column(String(255), nullable=False)
    created_on = Column(
        DateTime(timezone=True), server_default=func.current_timestamp()
    )
    updated_on = Column(
        DateTime(timezone=True),
        server_default=func.current_timestamp(),
        server_onupdate=func.current_timestamp(),
    )


def create_db() -> None:
    """
    Функция для создания таблицы БД
    """
    try:
        engine = connect_db()
        Base.metadata.create_all(engine)
        logger.info("Таблица spimex_trading_results в БД создана!")
    except Exception as ex:
        logger.exception("Ошибка создания БД: " + str(ex), exc_info=True)
