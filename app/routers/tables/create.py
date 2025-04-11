from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.Table import Table
from app.schemas import schemas
from app.database import get_db


router_create_table = APIRouter()

# Для создания нового столика 
@router_create_table.post("/", 
            description="Страница для создания нового столика",
            response_model=schemas.TableRead)
async def create_table(response:schemas.TableCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый столик в базе данных.

    Параметры:
    - table (schemas.TableCreate): Данные нового столика.
    - db (Session): Сессия подключения к БД.

    Возвращает:
    - Созданный столик (schemas.TableRead).
    """
    try:
        # Проверка, существует ли уже столик с таким именем
        existing_table_name = db.query(Table).filter(Table.name == response.name).first()
        print(existing_table_name)
        if existing_table_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Таблица с таким именем уже существует"
            )

        new_table = Table(**response.dict())

        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        
        return new_table
    
    except Exception as e:
        print(f'ERROR: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Произошла ошибка при создании столика"
        )