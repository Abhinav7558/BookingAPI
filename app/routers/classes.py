from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.database import get_db
from app.crud.fitness_class import get_upcoming_classes


router = APIRouter(
    prefix="/classes",
    tags=['classes']
)

class FitnessClassResponse(BaseModel):
    id: int
    name: str
    scheduled_at: datetime
    instructor: str
    available_slots: int

@router.get("/", response_model=List[FitnessClassResponse])
async def get_classes(db: Session = Depends(get_db)):
    """Get all upcoming fitness classes"""
    current_time = datetime.now(timezone.utc)
    return get_upcoming_classes(db, current_time)

