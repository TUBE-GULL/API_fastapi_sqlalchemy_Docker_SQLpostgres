from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from datetime import datetime, timedelta, timezone

from app.models.Reservation import Reservation 
from app.models.Table import Table
from app.schemas import schemas
from app.database import get_db 

router_create_reservation = APIRouter()


@router_create_reservation.post(
    "/",
    response_model=schemas.ReservationRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новое бронирование",
    description="""
    Создает новое бронирование столика с проверкой доступности.
    
    ### Параметры запроса:
    - `customer_name`: Имя клиента (обязательно)
    - `table_id`: ID столика (обязательно)
    - `reservation_time`: Дата и время брони (формат ISO 8601)
    - `duration_minutes`: Продолжительность брони в минутах
    
    ### Проверки:
    - Существование столика
    - Корректность формата времени
    - Отсутствие пересечений с другими бронированиями
    
    ### Возвращает:
    - Созданный объект бронирования со всеми деталями
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Бронирование успешно создано",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "customer_name": "Иван Иванов",
                        "table_id": 5,
                        "reservation_time": "2023-06-15T19:00:00",
                        "duration_minutes": 120
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Неверные данные запроса",
            "content": {
                "application/json": {
                    "examples": {
                        "invalid_table": {"detail": "Столик не найден"},
                        "invalid_time": {"detail": "Неверный формат времени бронирования"}
                    }
                }
            }
        },
        status.HTTP_409_CONFLICT: {
            "description": "Конфликт бронирований",
            "content": {
                "application/json": {
                    "example": {"detail": "Столик уже забронирован с 2023-06-15T18:00:00 до 2023-06-15T20:00:00"}
                }
            }
        }
    }
)
async def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    """
    Создает новое бронирование столика с полной валидацией.
    
    Args:
        reservation: Данные для создания брони (Pydantic модель)
        db: Сессия подключения к базе данных
        
    Returns:
        schemas.ReservationRead: Созданное бронирование
        
    Raises:
        HTTPException: 400 если столик не существует или неверный формат времени
        HTTPException: 409 если время уже занято другим бронированием
        HTTPException: 500 при внутренних ошибках сервера
    """
    try:
        # Проверка существования столика
        if not db.query(Table).filter(Table.id == reservation.table_id).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Столик не найден"
            )
        
        # Обработка и валидация времени бронирования
        try:
            if isinstance(reservation.reservation_time, datetime):
                start_new = (
                    reservation.reservation_time
                    if reservation.reservation_time.tzinfo
                    else reservation.reservation_time.replace(tzinfo=timezone.utc)
                )
            else:
                start_new = datetime.fromisoformat(
                    reservation.reservation_time.replace("Z", "+00:00")
                ).replace(tzinfo=timezone.utc)
        except (AttributeError, ValueError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Неверный формат времени бронирования: {str(e)}"
            )
            
        end_new = start_new + timedelta(minutes=reservation.duration_minutes)
        
        # ПРОВЕРКА ДОСТУПНОСТИ
        
        # Получаем все бронирования для выбранного столика
        existing_reservations = db.query(Reservation).filter(
            Reservation.table_id == reservation.table_id
        ).all()
        
        # Проверяем пересечения временных интервалов
        for existing in existing_reservations:
            start_existing = (
                existing.reservation_time.replace(tzinfo=timezone.utc)
                if not existing.reservation_time.tzinfo
                else existing.reservation_time.astimezone(timezone.utc)
            )
            end_existing = start_existing + timedelta(minutes=existing.duration_minutes)
            
            if start_new < end_existing and end_new > start_existing:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=(
                        f"Столик уже забронирован с "
                        f"{start_existing.strftime('%Y-%m-%dT%H:%M:%S')} "
                        f"до {end_existing.strftime('%Y-%m-%dT%H:%M:%S')}"
                    )
                )
        
        # СОЗДАНИЕ БРОНИРОВАНИЯ
        
        new_reservation = Reservation(
            customer_name=reservation.customer_name,
            table_id=reservation.table_id,
            reservation_time=start_new.replace(tzinfo=None),
            duration_minutes=reservation.duration_minutes
        )
        
        db.add(new_reservation)
        db.commit()
        db.refresh(new_reservation)
        
        return new_reservation
        
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
