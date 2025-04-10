from sqlalchemy.orm import Session 
from app.models import Reservation 
from app.schemas import schemas

def create_reservation (db: Session, reservation_data: schemas.ReservationCreate)->Reservation: 
    """
    Создает новую бронь столика.

    :param db: Сессия базы данных
    :param reservation_data: Данные для создания брони
    :return: Объект Reservation
    """
    
    reservation = Reservation(**reservation_data.dict())
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return reservation