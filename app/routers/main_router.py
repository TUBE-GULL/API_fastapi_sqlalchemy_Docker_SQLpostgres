from fastapi import APIRouter
from app.routers.tables.tables_router import tables
from app.routers.reservations.reservations_router import reservations

# root  
root = APIRouter()

# Главный router, чтобы файл main был чистым (здесь я объединяю все маршруты).
root.include_router(reservations) # Роутер для работы с бронями (просмотр, создание, удаление).
root.include_router(tables)  # Роутер для работы со столами (просмотр, бронирование, удаление).