import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, get_db
from sqlalchemy.orm import Session
from app.models.Table import Table

# Инициализируем клиент для тестов
client = TestClient(app)

# Настроим тестовую базу данных
@pytest.fixture(scope="module")
def db_session():
    # Создаем все таблицы в тестовой базе
    Base.metadata.create_all(bind=engine)
    db = Session(bind=engine)
    yield db
    db.close()
    # Очищаем таблицы после тестов
    Base.metadata.drop_all(bind=engine)


# Тестирование получения всех столиков
def test_get_all_tables(db_session):
    # Добавим несколько столиков для теста
    db_session.add(Table(name="Столик 1", seats=4, location="Терраса"))
    db_session.add(Table(name="Столик 2", seats=2, location="Зал"))
    db_session.commit()

    response = client.get("/tables/")
    
    assert response.status_code == 200
    assert len(response.json()) == 2  # Ожидаем 2 столика

# Тестирование создания нового столика
def test_create_table(db_session):
    new_table = {
        "name": "Столик 3",
        "seats": 4,
        "location": "Угол"
    }

    response = client.post("/tables/", json=new_table)
    
    assert response.status_code == 200
    assert response.json()["name"] == "Столик 3"
    assert response.json()["seats"] == 4

# Тестирование создания столика с уже существующим именем
def test_create_table_duplicate_name(db_session):
    # Создаем первый столик
    db_session.add(Table(name="Столик 4", seats=4, location="Угол"))
    db_session.commit()

    duplicate_table = {
        "name": "Столик 4",  # Уже существующее имя
        "seats": 2,
        "location": "Центр"
    }

    response = client.post("/tables/", json=duplicate_table)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Таблица с таким именем уже существует"

# Тестирование удаления столика
def test_delete_table(db_session):
    # Добавим столик, которого будем удалять
    table_to_delete = Table(name="Столик 5", seats=4, location="Терраса")
    db_session.add(table_to_delete)
    db_session.commit()

    response = client.delete(f"/tables/{table_to_delete.id}")
    
    assert response.status_code == 200
    assert response.json() == {"message": "Столик успешно удалён"}

# Тестирование попытки удалить несуществующий столик
def test_delete_table_not_found(db_session):
    response = client.delete("/tables/9999")  # Неверный ID
    assert response.status_code == 404
    assert response.json()["detail"] == "Столик не найден"