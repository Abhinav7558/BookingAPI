from datetime import datetime
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import (
    BookingCreate, 
    BookingResponse, 
)
from app.crud.book_class import (
    get_class,
    check_existing_booking,
    create_booking
)


logger = logging.getLogger(__name__)
router = APIRouter()

router = APIRouter(
    prefix="/bookings",
    tags=['bookings']
)

@router.post(
    "/book",
    response_model=BookingResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_booking_for_class(
    booking: BookingCreate,
    db: Session = Depends(get_db)
):
    """
    Book a spot in a fitness class
    """
    try:
        # Check if class exists
        db_class = get_class(db, booking.class_id)
        if not db_class:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Class with id {booking.class_id} not found"
            )
        
        current_time = datetime.now().replace(tzinfo=None)

        if db_class.scheduled_at <= current_time:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Class is already over"
            )  
        
        # Check for existing booking
        existing_booking = check_existing_booking(
            db, booking.class_id, booking.client_email
        )
        if existing_booking:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="You already have a booking for this class"
            )
        
        # Check available slots
        if db_class.available_slots <= 0:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No available slots for this class"
            )
        
        # Create booking
        db_booking = create_booking(db, booking)
        if not db_booking:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create booking"
            )
        
        logger.info(f"Created booking {db_booking.id} for {booking.client_email}")
        return BookingResponse(
            id=db_booking.id,
            class_id=db_booking.class_id,
            client_name=db_booking.client_name,
            client_email=db_booking.client_email,
            scheduled_at = db_class.scheduled_at,
            booking_time=db_booking.booking_time,
            status=db_booking.status
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create booking"
        )