from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app.config import settings

# строка подключения 
DB_URL = settings.DATABASE_URL_psycopg

# создаем движок SqlAlchemy
engine = create_engine(
    url = DB_URL,
    echo=True, #логи
    # pool_size=5, #max_connect db 5 
    # pool_overflow=10,# доп connect к db
    )


Base = declarative_base()
Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)


async def create_db():
    try:
        async with engine.begin() as conn:
            # Попытка создания всех таблиц
            await conn.run_sync(Base.metadata.create_all)
        print("Таблицы успешно созданы.")
    except SQLAlchemyError as e:
        # Обработка ошибок SQLAlchemy
        print(f"Ошибка при создании таблиц: {e}")
    except Exception as e:
        # Обработка всех других исключений
        print(f"Произошла ошибка: {e}")


# # Функция для получения сессии
async def get_db():

    db = Session()  # Создаём сессию
    
    try:
        yield db  
    except SQLAlchemyError as e:
        print(f"Ошибка при получении сессии: {e}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")



