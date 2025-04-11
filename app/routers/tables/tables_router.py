from fastapi import APIRouter

from app.routers.tables.get_all import router_get_all_tables
from app.routers.tables.create import router_create_table 
from app.routers.tables.delete import router_delete_table

tables = APIRouter(
    prefix='/tables',
    tags=["Столики"]
)

tables.include_router(router_get_all_tables)
tables.include_router(router_create_table)
tables.include_router(router_delete_table)



# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
# from app.models.Table import Table
# from app.schemas import schemas
# from app.database import get_db

# # для получения ВСЕХ СТОЛОВ В db
# @tables.get('/',
#             description="Получить список всех столиков в ресторане",
#             response_model=list[schemas.TableRead])
# async def get_all_tables(db: Session = Depends(get_db)):
#     """
#     Возвращает список всех столиков, зарегистрированных в ресторане.

#     Параметры:
#     - db (Session): Сессия подключения к базе данных.

#     Возвращает:
#     - Список объектов столиков (schemas.TableRead).
#     """
#     return db.query(Table).all()


# # Для создания нового столика 
# @tables.post("/", 
#             description="Страница для создания нового столика",
#             response_model=schemas.TableRead)
# async def create_table(response:schemas.TableCreate, db: Session = Depends(get_db)):
#     """
#     Создаёт новый столик в базе данных.

#     Параметры:
#     - table (schemas.TableCreate): Данные нового столика.
#     - db (Session): Сессия подключения к БД.

#     Возвращает:
#     - Созданный столик (schemas.TableRead).
#     """
#     try:
#         # Проверка, существует ли уже столик с таким именем
#         existing_table_name = db.query(Table).filter(Table.name == response.name).first()
#         print(existing_table_name)
#         if existing_table_name:
#             raise HTTPException(
#                 status_code=status.HTTP_400_BAD_REQUEST, 
#                 detail="Таблица с таким именем уже существует"
#             )

#         new_table = Table(**response.dict())

#         db.add(new_table)
#         db.commit()
#         db.refresh(new_table)
        
#         return new_table
    
#     except Exception as e:
#         print(f'ERROR: {e}')
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
#             detail="Произошла ошибка при создании столика"
#         )
        
# удаления столика по id 
# @tables.delete('/{table_id}',
#                description="Удалить столик по его уникальному идентификатору")
# async def delete_table(table_id:int, db:Session = Depends(get_db)):
#     """
#     Удаляет столик по его ID.

#     Параметры:
#     - table_id (int): Идентификатор столика.
#     - db (Session): Сессия подключения к БД.

#     Исключения:
#     - 404: Столик не найден.

#     Возвращает:
#     - Подтверждение удаления.
#     """
#     try:
#         table = db.query(Table).filter(Table.id == table_id).first()
#         if not table:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Столик не найден"
#             )

#         db.delete(table)
#         db.commit()
#         return {"message": "Столик успешно удалён"}
    
#     except Exception as e:
#         print(f'ERROR: {e}')
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
#             detail="Произошла ошибка при создании столика"
        # )