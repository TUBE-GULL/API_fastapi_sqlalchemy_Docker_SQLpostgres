from datetime import datetime, timedelta

def test_table_data():
    return {
        "name": "Test Table",
        "seats": 4,
        "location": "Test Location"
    }

def test_reservation_data():
    return {
        "customer_name": "Test Customer",
        "table_id": 1,
        "reservation_time": (datetime.now() + timedelta(days=1)).isoformat(),
        "duration_minutes": 60
    }