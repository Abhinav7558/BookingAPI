from datetime import datetime, timedelta, timezone
from unittest.mock import patch

from fastapi import status

from ..models import FitnessClass


def test_create_booking_success(test_class, client):
    booking_data = {
        "class_id": test_class.id,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = client.post("/bookings/book", json=booking_data)
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["class_id"] == test_class.id
    assert response.json()["client_name"] == "Test User"
    assert response.json()["client_email"] == "test@example.com"

def test_create_booking_invalid_class_id(client):
    booking_data = {
        "class_id": 999,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = client.post("/bookings/book", json=booking_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Class with id 999 not found'}

def test_create_booking_class_over(test_class, test_db, client):
    db_class = test_db.query(FitnessClass).filter(FitnessClass.id == test_class.id).first()
    db_class.scheduled_at = datetime.now(timezone.utc) - timedelta(days=1)
    test_db.commit()

    booking_data = {
        "class_id": test_class.id,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = client.post("/bookings/book", json=booking_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'Class is already over'}

def test_create_booking_duplicate(test_class, client):
    booking_data = {
        "class_id": test_class.id,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    client.post("/bookings/book", json=booking_data)
    response = client.post("/bookings/book", json=booking_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'You already have a booking for this class'}

def test_create_booking_no_slots(test_class, test_db, client):
    db_class = test_db.query(FitnessClass).filter(FitnessClass.id == test_class.id).first()
    db_class.available_slots = 0
    test_db.commit()

    booking_data = {
        "class_id": test_class.id,
        "client_name": "Test User",
        "client_email": "test@example.com"
    }
    response = client.post("/bookings/book", json=booking_data)
    assert response.status_code == status.HTTP_409_CONFLICT
    assert response.json() == {'detail': 'No available slots for this class'}

def test_get_bookings_success(mock_db_bookings, client):
    with patch("app.routers.bookings.get_bookings_with_class_details_by_email", return_value=mock_db_bookings), \
         patch("app.routers.bookings.is_valid_timezone", return_value=True), \
         patch("app.routers.bookings.convert_utc_to_timezone", side_effect=lambda dt, tz: dt):

        response = client.get("/bookings?email=testuser@example.com&time_zone=Asia/Kolkata")

        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["class_id"] == 10
        assert data[0]["class_name"] == "Yoga"
        assert data[0]["client_email"] == "testuser@example.com"
        assert data[0]["client_name"] == "test user"
        assert data[0]["instructor"] == "test instructor"
        assert data[0]["status"] == "confirmed"
        assert data[0]["booking_time"] == "2025-06-01T12:00:00"

def test_get_bookings_no_email(client):
    response = client.get("/bookings")
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY 

def test_get_bookings_invalid_timezone(client):
    response = client.get("/bookings?email=test@example.com&time_zone=Invalid/Zone")
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "Invalid timezone" in response.json()["detail"]
