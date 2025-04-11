from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.Table import Table
from app.database import get_db

router_delete_table = APIRouter()


# удаления столика по id 
@router_delete_table.delete('/{table_id}',
               description="Удалить столик по его уникальному идентификатору")
async def delete_table(table_id:int, db:Session = Depends(get_db)):
    """
    Удаляет столик по его ID.

    Параметры:
    - table_id (int): Идентификатор столика.
    - db (Session): Сессия подключения к БД.

    Исключения:
    - 404: Столик не найден.

    Возвращает:
    - Подтверждение удаления.
    """
    try:
        table = db.query(Table).filter(Table.id == table_id).first()
        if not table:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Столик не найден"
            )

        db.delete(table)
        db.commit()
        return {"message": "Столик успешно удалён"}
    
    except Exception as e:
        print(f'ERROR: {e}')
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Произошла ошибка при создании столика"
        )