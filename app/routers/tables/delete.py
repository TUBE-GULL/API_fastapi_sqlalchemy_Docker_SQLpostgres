from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict

from app.models.Table import Table
from app.database import get_db

router_delete_table = APIRouter()

@router_delete_table.delete(
    "/{table_id}",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    summary="Удалить столик",
    description="""
    Удаляет столик из системы по его уникальному идентификатору.
    
    ### Параметры:
    - `table_id`: ID столика для удаления (целое число > 0)
    
    ### Возвращает:
    - Сообщение об успешном удалении
    
    ### Ошибки:
    - 404: Если столик с указанным ID не найден
    - 500: При внутренних ошибках сервера
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Столик успешно удален",
            "content": {
                "application/json": {
                    "example": {"message": "Столик успешно удалён"}
                }
            }
        },
        status.HTTP_404_NOT_FOUND: {
            "description": "Столик не найден",
            "content": {
                "application/json": {
                    "example": {"detail": "Столик не найден"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Ошибка при удалении столика"}
                }
            }
        }
    }
)
async def delete_table(table_id:int, db:Session = Depends(get_db)):
    """
    Удаляет столик из базы данных по его ID.

    Args:
        table_id: Уникальный идентификатор столика (должен быть > 0)
        db: Сессия подключения к базе данных

    Returns:
        dict: Сообщение об успешном удалении

    Raises:
        HTTPException: 404 если столик не найден
        HTTPException: 500 при ошибках базы данных
    """
    try:
        # Поиск столика в базе данных
        table = db.query(Table).filter(Table.id == table_id).first()
        
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Столик не найден"
            )

        # Удаление столика
        db.delete(table)
        db.commit()
        
        return {"message": "Столик успешно удалён"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка базы данных: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неожиданная ошибка: {str(e)}"
        )
