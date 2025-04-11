from fastapi import APIRouter, Depends, Path, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database import get_db
from app.models.Reservation import Reservation 

router_delete_reservation = APIRouter()

@router_delete_reservation.delete(
    '/{reservation_id}',
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Удаление бронирования",
    description="""
    Удаляет существующее бронирование столика по указанному идентификатору.
    
    ### Параметры:
    - `reservation_id`: ID бронирования, которое нужно удалить
    
    ### Возвращает:
    - Сообщение об успешном удалении
    
    ### Ошибки:
    - 404: Если бронирование с указанным ID не найдено
    - 500: При внутренних ошибках сервера
    """,
    responses={
        200: {
            "description": "Бронирование успешно удалено",
            "content": {
                "application/json": {
                    "example": {"message": "Бронь успешно удалена"}
                }
            }
        },
        404: {
            "description": "Бронирование не найдено",
            "content": {
                "application/json": {
                    "example": {"detail": "Бронь не найдена"}
                }
            }
        }
    }
)
async def delete_reservation(
    reservation_id: int = Path(..., description="ID бронирования для удаления", gt=0),
    db: Session = Depends(get_db)
) -> dict:
    """
    Удаляет бронирование столика по его уникальному идентификатору.
    
    Args:
        reservation_id: Уникальный идентификатор брони (должен быть > 0)
        db: Сессия подключения к базе данных
        
    Returns:
        dict: Сообщение об успешном удалении
        
    Raises:
        HTTPException: 404 если бронь не найдена
    """
    try:
        # Ищем бронирование в базе
        reservation = db.query(Reservation).get(reservation_id)
        
        if not reservation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Бронь не найдена"
            )
        
        # Удаляем бронирование
        db.delete(reservation)
        db.commit()
        
        return {"message": "Бронь успешно удалена"}
        
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при удалении брони: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Неожиданная ошибка: {str(e)}"
        )