from datetime import datetime

from sqlalchemy.orm import Session

from ..models import FitnessClass

def get_upcoming_classes(db: Session, current_time: datetime):
    return (
        db.query(FitnessClass)
        .filter(FitnessClass.scheduled_at > current_time)
        .order_by(FitnessClass.scheduled_at.asc())
        .all()
    )
