from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas import schemas
from app.database import get_db
from app.models.Reservation import Reservation 

router_get_all_reservations = APIRouter()

@router_get_all_reservations.get(
    "/",
    response_model=list[schemas.ReservationRead],
    status_code=status.HTTP_200_OK,
    summary="Получить все бронирования",
    description="""
    Возвращает полный список всех бронирований в системе.
    
    ### Возвращает:
    - Список объектов бронирований с детальной информацией:
      - ID брони
      - Имя клиента
      - ID столика
      - Время бронирования
      - Продолжительность брони
    """,
    responses={
        status.HTTP_200_OK: {
            "description": "Успешный возврат списка бронирований",
            "content": {
                "application/json": {
                    "example": [{
                        "id": 1,
                        "customer_name": "Иван Иванов",
                        "table_id": 3,
                        "reservation_time": "2023-05-15T19:00:00",
                        "duration_minutes": 120
                    }]
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера при получении данных",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            }
        }
    }
)

async def get_all_reservations(db: Session = Depends(get_db)):
    """
    Получает список всех активных бронирований из системы.
    
    Args:
        db (Session): Сессия подключения к базе данных
        
    Returns:
        list[schemas.ReservationRead]: Список всех бронирований в формате Pydantic модели
        
    Raises:
        HTTPException: 500 при ошибках доступа к базе данных
    """
    try:
        # Получаем все бронирования из базы данных
        reservations = db.query(Reservation).order_by(Reservation.reservation_time).all()
        return reservations
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении списка бронирований: {str(e)}"
        )
