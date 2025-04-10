from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.database import Base

#бронирования столика
class Reservation(Base):
    """
    Модель бронирования столика.

    Атрибуты:
    - id: Уникальный идентификатор брони.
    - customer_name: Имя клиента.
    - table_id: Внешний ключ на столик.
    - reservation_time: Время начала бронирования.
    - duration_minutes: Продолжительность в минутах.
    """   
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, nullable=False)
    table_id = Column(Integer, ForeignKey('tables.id', ondelete='CASCADE'))
    reservation_time = Column(DateTime, nullable=False)
    duration_minutes = Column(Integer, nullable=False)
    
    table = relationship('Table', back_populates='reservations')