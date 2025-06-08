from datetime import datetime, timezone
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.models import FitnessClass
from app.database import get_db


router = APIRouter(
    prefix="/classes",
    tags=['classes']
)

class FitnessClassResponse(BaseModel):
    id: int
    name: str
    scheduled_at: datetime
    instructor: str

@router.get("/", response_model=List[FitnessClassResponse])
async def get_classes(db: Session = Depends(get_db)):
    """Get all upcoming fitness classes"""
    current_time = datetime.now(timezone.utc)
    results = (
        db.query(FitnessClass)
        .filter(FitnessClass.scheduled_at > current_time)
        .order_by(FitnessClass.scheduled_at.asc())
        .all()
    )
    return results

