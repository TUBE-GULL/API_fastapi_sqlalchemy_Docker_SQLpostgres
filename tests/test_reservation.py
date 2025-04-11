import pytest
from fastapi import status
from tests.fixtures.test_data import test_table_data, test_reservation_data

# Тесты для создания бронирования
class TestCreateReservation:
    def test_create_reservation_success(self, client, db):
        # Сначала создаем тестовый столик
        table_response = client.post("/tables/", json=test_table_data())
        assert table_response.status_code == status.HTTP_201_CREATED
        
        # Создаем бронирование
        response = client.post("/reservations/", json=test_reservation_data())
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["customer_name"] == "Test Customer"
        assert data["table_id"] == 1

    def test_create_reservation_table_not_found(self, client):
        response = client.post("/reservations/", json=test_reservation_data())
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["detail"] == "Столик не найден"

    def test_create_reservation_time_conflict(self, client, db):
        # Создаем столик
        table_response = client.post("/tables/", json=test_table_data())
        
        # Первое бронирование
        client.post("/reservations/", json=test_reservation_data())
        
        # Второе бронирование на то же время
        response = client.post("/reservations/", json=test_reservation_data())
        assert response.status_code == status.HTTP_409_CONFLICT

# Тесты для получения всех бронирований
class TestGetAllReservations:
    def test_get_all_reservations_empty(self, client):
        response = client.get("/reservations/")
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == []

    def test_get_all_reservations_with_data(self, client, db):
        # Создаем тестовые данные
        client.post("/tables/", json=test_table_data())
        client.post("/reservations/", json=test_reservation_data())
        
        # Получаем все бронирования
        response = client.get("/reservations/")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert len(data) == 1
        assert data[0]["customer_name"] == "Test Customer"

# Тесты для удаления бронирования
class TestDeleteReservation:
    def test_delete_reservation_success(self, client, db):
        # Создаем тестовые данные
        client.post("/tables/", json=test_table_data())
        create_response = client.post("/reservations/", json=test_reservation_data())
        reservation_id = create_response.json()["id"]
        
        # Удаляем бронирование
        response = client.delete(f"/reservations/{reservation_id}")
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["message"] == "Бронь успешно удалена"

    def test_delete_reservation_not_found(self, client):
        response = client.delete("/reservations/999")
        assert response.status_code == status.HTTP_404_NOT_FOUND