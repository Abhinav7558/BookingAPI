from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_serializer, field_validator


class ORMConfig:
    class Config:
        from_attributes = True 


class FitnessClassResponse(BaseModel, ORMConfig):
    id: int
    name: str
    instructor: str
    scheduled_at: datetime
    total_slots: int
    available_slots: int

    @field_serializer("scheduled_at", when_used="json")
    def serialize_dt(self, dt: datetime, _info):
        return dt.replace(tzinfo=None, microsecond=0).isoformat()


class BookingBase(BaseModel):
    """Base schema for booking"""
    class_id: int = Field(..., ge=1)
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

    @field_validator('client_name')
    def validate_client_name(cls, v):
        """Validate client name format"""
        if not v.strip():
            raise ValueError('Client name cannot be empty')
        return v.strip()


class BookingCreate(BookingBase):
    """Schema for creating a new booking"""
    pass


class BookingResponse(BookingBase, ORMConfig):
    """Schema for booking response"""
    id: int
    booking_time: datetime
    scheduled_at: datetime
    status: str = "confirmed"

    @field_serializer("booking_time", "scheduled_at", when_used="json")
    def serialize_dt(self, dt: datetime, _info):
        return dt.replace(tzinfo=None, microsecond=0).isoformat()


class BookingWithClassResponse(BookingResponse, ORMConfig):
    """Schema for booking response with class details"""
    class_name: str
    instructor: str


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[dict] = None