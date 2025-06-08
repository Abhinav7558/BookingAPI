import logging
from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.models import FitnessClass, Booking
from app.schemas import BookingCreate

logger = logging.getLogger(__name__)


def get_class(db: Session, class_id: int) -> Optional[FitnessClass]:
    """Get a fitness class by ID"""
    return db.query(FitnessClass).filter(FitnessClass.id == class_id).first()

def check_existing_booking(db: Session, class_id: int, email: str) -> Optional[Booking]:
    """Check if a client already has a booking for a specific class"""
    return (
        db.query(Booking)
        .filter(
            and_(
                Booking.class_id == class_id,
                Booking.client_email == email,
                Booking.status == "confirmed"
            )
        )
        .first()
    )


def create_booking(db: Session, booking_data: BookingCreate) -> Optional[Booking]:
    """
    Create a new booking with slot validation
    
    """
    # Check if class exists and has available slots
    db_class = get_class(db, booking_data.class_id)
    
    # Create the booking
    db_booking = Booking(
        class_id=booking_data.class_id,
        client_name=booking_data.client_name,
        client_email=booking_data.client_email,
        booking_time=datetime.now(timezone.utc),
        status="confirmed"
    )
    
    # Decrease available slots
    db_class.available_slots -= 1
    db_class.updated_at = datetime.now(timezone.utc)
    
    # Add both to session and commit
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    
    logger.info(f"Created booking: {db_booking.id} for class {booking_data.class_id}")
    return db_booking