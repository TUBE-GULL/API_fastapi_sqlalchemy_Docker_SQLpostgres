from pydantic import BaseModel
from datetime import datetime

class TableBase(BaseModel):
    name: str
    seats: int
    location: str
    
class TableCreate(TableBase):
    pass

class TableRead(TableBase):
    id: int
    class Config:
        orm_mode = True
        
class ReservationBase(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_minutes: int
    
class ReservationCreate(ReservationBase):
    pass

class ReservationRead(ReservationBase):
    id: int
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    id: int
    username: str