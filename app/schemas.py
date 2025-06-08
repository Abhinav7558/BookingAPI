"""
Pydantic schemas for request/response validation
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, validator


class ClassBase(BaseModel):
    """Base schema for fitness class"""
    name: str = Field(..., min_length=1, max_length=100)
    datetime: datetime
    instructor: str = Field(..., min_length=1, max_length=100)
    total_slots: int = Field(..., ge=1)
    available_slots: int = Field(..., ge=0)


class ClassCreate(ClassBase):
    """Schema for creating a new fitness class"""
    pass


class ClassResponse(ClassBase):
    """Schema for fitness class response"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class BookingBase(BaseModel):
    """Base schema for booking"""
    class_id: int = Field(..., ge=1)
    client_name: str = Field(..., min_length=1, max_length=100)
    client_email: EmailStr

    @validator('client_name')
    def validate_client_name(cls, v):
        """Validate client name format"""
        if not v.strip():
            raise ValueError('Client name cannot be empty')
        return v.strip()


class BookingCreate(BookingBase):
    """Schema for creating a new booking"""
    pass


class BookingResponse(BookingBase):
    """Schema for booking response"""
    id: int
    booking_time: datetime
    status: str = "confirmed"

    class Config:
        from_attributes = True


class BookingWithClassResponse(BookingResponse):
    """Schema for booking response with class details"""
    class_name: str
    class_datetime: datetime
    instructor: str

    class Config:
        from_attributes = True


class ErrorResponse(BaseModel):
    """Schema for error responses"""
    detail: str
    error_code: Optional[str] = None


class SuccessResponse(BaseModel):
    """Schema for success responses"""
    message: str
    data: Optional[dict] = None