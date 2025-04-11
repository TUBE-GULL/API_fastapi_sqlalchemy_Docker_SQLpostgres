from fastapi import APIRouter
from app.routers.reservations.create import router_create_reservation
from app.routers.reservations.delete import router_delete_reservation
from app.routers.reservations.get_all import router_get_all_reservations

reservations = APIRouter(
    prefix="/reservations",
    tags=["Брони"]
)

reservations.include_router(router_create_reservation)
reservations.include_router(router_delete_reservation)
reservations.include_router(router_get_all_reservations)



# from fastapi import APIRouter, Depends, HTTPException, status, Path
# from sqlalchemy.orm import Session
# from sqlalchemy.exc import SQLAlchemyError
# from app.models.Reservation import Reservation 
# from app.models.Table import Table
# from app.schemas import schemas
# from app.database import get_db 
# from datetime import datetime, timedelta
# from fastapi import HTTPException, status
# from datetime import datetime, timedelta, timezone


# @reservations.get('/',
#                   description="Получить список всех броней",
#                   response_model=list[schemas.ReservationRead])
# async def get_all_reservations(db:Session = Depends(get_db)):
#     """
#     Возвращает список всех броней в ресторане.

#     Параметры:
#     - db (Session): Сессия подключения к базе данных.
    
#     Возвращает:
#     - Список объектов броней (schemas.ReservationRead).
#     """
    
#     return db.query(Reservation).all()


# @reservations.post('/',
#                    description="Создать новую бронь столика",
#                    response_model=schemas.ReservationRead)
# async def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
#     """
#     Создаёт новую бронь столика на основе входных данных.
#     """
#     # Проверка существования столика
#     table = db.query(Table).filter(Table.id == reservation.table_id).first()
#     if not table:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, 
#             detail="Столик не найден"
#         )
    
#     # Обработка времени бронирования
#     try:
#         # Приводим время к UTC и делаем timezone-aware
#         if isinstance(reservation.reservation_time, datetime):
#             if reservation.reservation_time.tzinfo is None:
#                 start_new = reservation.reservation_time.replace(tzinfo=timezone.utc)
#             else:
#                 start_new = reservation.reservation_time.astimezone(timezone.utc)
#         else:
#             start_new = datetime.fromisoformat(reservation.reservation_time.replace("Z", "+00:00"))
#             if start_new.tzinfo is None:
#                 start_new = start_new.replace(tzinfo=timezone.utc)
#     except (AttributeError, ValueError) as e:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail=f"Неверный формат времени бронирования: {str(e)}"
#         )
    
#     end_new = start_new + timedelta(minutes=reservation.duration_minutes)
    
#     # Получаем все бронирования для этого столика
#     existing_reservations = db.query(Reservation).filter(
#         Reservation.table_id == reservation.table_id
#     ).all()
    
#     # Проверяем пересечения с существующими бронями
#     for existing in existing_reservations:
#         # Приводим время существующей брони к UTC
#         start_existing = existing.reservation_time
#         if start_existing.tzinfo is None:
#             start_existing = start_existing.replace(tzinfo=timezone.utc)
#         else:
#             start_existing = start_existing.astimezone(timezone.utc)
        
#         end_existing = start_existing + timedelta(minutes=existing.duration_minutes)
        
#         # Проверяем пересечение временных интервалов
#         if (start_new < end_existing) and (end_new > start_existing):
#             raise HTTPException(
#                 status_code=status.HTTP_409_CONFLICT,
#                 detail=f"Столик уже забронирован с {start_existing} до {end_existing}"
#             )
    
#     # Создаем новую бронь (сохраняем как timezone-naive в БД)
#     new_reservation = Reservation(
#         customer_name=reservation.customer_name,
#         table_id=reservation.table_id,
#         reservation_time=start_new.replace(tzinfo=None),  # Убираем временную зону для хранения
#         duration_minutes=reservation.duration_minutes
#     )
    
#     db.add(new_reservation)
#     db.commit()
#     db.refresh(new_reservation)
#     return new_reservation


# @reservations.delete(
#     '/{reservation_id}',
#     response_model=dict,
#     status_code=status.HTTP_200_OK,
#     summary="Удаление бронирования",
#     description="""
#     Удаляет существующее бронирование столика по указанному идентификатору.
    
#     ### Параметры:
#     - `reservation_id`: ID бронирования, которое нужно удалить
    
#     ### Возвращает:
#     - Сообщение об успешном удалении
    
#     ### Ошибки:
#     - 404: Если бронирование с указанным ID не найдено
#     - 500: При внутренних ошибках сервера
#     """,
#     responses={
#         200: {
#             "description": "Бронирование успешно удалено",
#             "content": {
#                 "application/json": {
#                     "example": {"message": "Бронь успешно удалена"}
#                 }
#             }
#         },
#         404: {
#             "description": "Бронирование не найдено",
#             "content": {
#                 "application/json": {
#                     "example": {"detail": "Бронь не найдена"}
#                 }
#             }
#         }
#     }
# )
# async def delete_reservation(
#     reservation_id: int = Path(..., description="ID бронирования для удаления", gt=0),
#     db: Session = Depends(get_db)
# ) -> dict:
#     """
#     Удаляет бронирование столика по его уникальному идентификатору.
    
#     Args:
#         reservation_id: Уникальный идентификатор брони (должен быть > 0)
#         db: Сессия подключения к базе данных
        
#     Returns:
#         dict: Сообщение об успешном удалении
        
#     Raises:
#         HTTPException: 404 если бронь не найдена
#     """
#     try:
#         # Ищем бронирование в базе
#         reservation = db.query(Reservation).get(reservation_id)
        
#         if not reservation:
#             raise HTTPException(
#                 status_code=status.HTTP_404_NOT_FOUND,
#                 detail="Бронь не найдена"
#             )
        
#         # Удаляем бронирование
#         db.delete(reservation)
#         db.commit()
        
#         return {"message": "Бронь успешно удалена"}
        
#     except SQLAlchemyError as e:
#         db.rollback()
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Ошибка при удалении брони: {str(e)}"
#         )
#     except Exception as e:
#         raise HTTPException(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             detail=f"Неожиданная ошибка: {str(e)}"
#         )