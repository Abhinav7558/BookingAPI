from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker

from ..models import Booking, FitnessClass
from ..main import app
from ..database import Base, get_db
from app import main

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={'check_same_thread': False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

# Override get_db to use the testing database
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(main.app)

# Add a fixture to get the test database session
@pytest.fixture()
def test_db():
    """Fixture to get test database session - use this instead of direct TestingSessionLocal()"""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture for sample fitnessclass
@pytest.fixture
def test_class(test_db):
    fitness_class = FitnessClass(
        name="Yoga",
        scheduled_at=datetime.now(timezone.utc) + timedelta(days=1),
        instructor="Test Instructor",
        total_slots=10,
        available_slots=10
    )
    test_db.add(fitness_class)
    test_db.commit()
    test_db.refresh(fitness_class)

    yield fitness_class

    # Cleanup
    test_db.query(Booking).filter(Booking.class_id == fitness_class.id).delete()
    test_db.delete(fitness_class)
    test_db.commit()


@pytest.fixture
def mock_db_bookings():
    return [
        {
            "id": 1,
            "class_id": 10,
            "class_name": "Yoga",
            "scheduled_at": "2025-06-10T10:00:00+00:00",
            "instructor": "test instructor",
            "client_name": "test user",
            "client_email": "testuser@example.com",
            "booking_time": "2025-06-01T12:00:00+00:00",
            "status": "confirmed"
        }
    ]
