from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.models.Table import Table
from app.schemas import schemas 
from app.database import get_db


router_create_table = APIRouter()

@router_create_table.post(
    "/",
    response_model=schemas.TableRead,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый столик",
    description="""
    Создает новый столик в системе ресторана.
    
    ### Проверки:
    - Уникальность имени столика
    - Корректность входных данных
    
    ### Возвращает:
    - Объект созданного столика со всеми полями
    """,
    responses={
        status.HTTP_201_CREATED: {
            "description": "Столик успешно создан",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "name": "Столик у окна",
                        "capacity": 4,
                        "status": "available"
                    }
                }
            }
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Некорректные данные",
            "content": {
                "application/json": {
                    "example": {"detail": "Таблица с таким именем уже существует"}
                }
            }
        },
        status.HTTP_500_INTERNAL_SERVER_ERROR: {
            "description": "Ошибка сервера",
            "content": {
                "application/json": {
                    "example": {"detail": "Произошла ошибка при создании столика"}
                }
            }
        }
    }
)
async def create_table(response:schemas.TableCreate, db: Session = Depends(get_db)):
    """
    Создание нового столика в базе данных.

    Args:
        table_data (schemas.TableCreate): Данные для создания столика
        db (Session): Сессия подключения к базе данных

    Returns:
        schemas.TableRead: Созданный столик

    Raises:
        HTTPException: 400 если столик с таким именем уже существует
        HTTPException: 500 при ошибках базы данных
    """
    try:
        # Проверка уникальности имени столика
        if db.query(Table).filter(Table.name == response.name).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Таблица с таким именем уже существует"
            )


        # Создание нового столика
        new_table = Table(**response.dict())
        
        db.add(new_table)
        db.commit()
        db.refresh(new_table)
        
        return new_table

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
