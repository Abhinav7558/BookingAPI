from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class FitnessClass(Base):
    """
    Model for fitness classes
    """
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, index=True)
    scheduled_at = Column(DateTime(timezone=True), nullable=False, index=True)
    instructor = Column(String(100), nullable=False)
    total_slots = Column(Integer, nullable=False)
    available_slots = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relationship with bookings
    bookings = relationship("Booking", back_populates="fitness_class")

    def __repr__(self):
        return f"<FitnessClass(id={self.id}, name='{self.name}', datetime='{self.datetime}')>"


class Booking(Base):
    """
    Model for class bookings
    """
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=False, index=True)
    client_name = Column(String(100), nullable=False)
    client_email = Column(String(255), nullable=False, index=True)
    booking_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    status = Column(String(20), default="confirmed", index=True)

    # Relationship with fitness class
    fitness_class = relationship("FitnessClass", back_populates="bookings")

    def __repr__(self):
        return f"<Booking(id={self.id}, class_id={self.class_id}, client_email='{self.client_email}')>"