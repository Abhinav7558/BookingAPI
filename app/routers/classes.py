from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.database import get_db
from app.crud.fitness_class import get_upcoming_classes
from app.schemas import FitnessClassResponse
from app.utils.timezone_utils import convert_utc_to_timezone, get_default_timezone, is_valid_timezone


router = APIRouter(
    prefix="/classes",
    tags=['classes']
)

@router.get("", 
            response_model=List[FitnessClassResponse], 
            status_code=status.HTTP_200_OK
            )
async def get_classes(db: Session = Depends(get_db),
                      time_zone: Optional[str] = Query(None, description="Target timezone for datetime conversion"
     ),
    ):
    """Get all upcoming fitness classes"""
    current_time = datetime.now(timezone.utc)
    target_timezone = time_zone or get_default_timezone()
    if not is_valid_timezone(target_timezone):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid timezone: {target_timezone}"
        )
    
    results = get_upcoming_classes(db, current_time)
    
    class_details = []
    for fitness_class in results:
        class_details.append(FitnessClassResponse(
            id=fitness_class.id,
            name=fitness_class.name,
            scheduled_at=convert_utc_to_timezone(fitness_class.scheduled_at, target_timezone),
            instructor=fitness_class.instructor,
            total_slots=fitness_class.total_slots,
            available_slots=fitness_class.available_slots
    ))
    
    return class_details

