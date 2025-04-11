from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from app.models.Table import Table
from typing import List

from app.schemas import schemas
from app.database import get_db

router_get_all_tables = APIRouter()

# для получения ВСЕХ СТОЛОВ В db
@router_get_all_tables.get(
    "/",
    response_model=List[schemas.TableRead],
    status_code=status.HTTP_200_OK,
    summary="Получить все столики",
    description="""
    Возвращает полный список всех столиков в ресторане.
    
    ### Возвращает:
    - Список объектов с деталями каждого столика:
      - id: уникальный идентификатор
      - name: название столика
      - seats: количество мест
      - location: расположение в зале
      - status: текущий статус
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Успешный возврат списка столиков",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "name": "Столик у окна",
                        "seats": 4,
                        "location": "У фонтана",
                        "status": "available"
                    }]
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка при получении списка столиков"}
                }
            }
        }
    }
)
async def get_all_tables(db: Session = Depends(get_db)):
    """
    Получает список всех столиков из базы данных.

    Args:
        db: Сессия подключения к базе данных

    Returns:
        List[TableRead]: Список всех столиков в формате Pydantic модели

    Raises:
        HTTPException: 500 при ошибках базы данных
    """
    try:
        tables = db.query(Table).order_by(Table.name).all()
        return tables
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неожиданная ошибка: {str(e)}"
        )