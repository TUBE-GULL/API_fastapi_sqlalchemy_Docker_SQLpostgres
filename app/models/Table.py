from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base  


# ресторана — столик
class Table(Base):
    """
    Модель ресторана — столик.
    
    Атрибуты:
    - id: Уникальный идентификатор столика.
    - name: Название столика (например, "Table 1").
    - seats: Количество посадочных мест.
    - location: Расположение в зале (например, "у окна").
    """
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    seats = Column(Integer, nullable=False)
    location = Column(String)

    reservations = relationship("Reservation", back_populates="table", cascade="all, delete")
