from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.Table import Table
from app.schemas import schemas
from app.database import get_db

router_get_all_tables = APIRouter()

# для получения ВСЕХ СТОЛОВ В db
@router_get_all_tables.get('/',
            description="Получить список всех столиков в ресторане",
            response_model=list[schemas.TableRead])
async def get_all_tables(db: Session = Depends(get_db)):
    """
    Возвращает список всех столиков, зарегистрированных в ресторане.

    Параметры:
    - db (Session): Сессия подключения к базе данных.

    Возвращает:
    - Список объектов столиков (schemas.TableRead).
    """
    return db.query(Table).all()