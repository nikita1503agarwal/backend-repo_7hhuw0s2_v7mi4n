"""
Database Schemas for Athly Global

Each Pydantic model represents a MongoDB collection. The collection name is the lowercase
version of the class name (e.g., Trainer -> "trainer").
"""
from typing import List, Optional
from pydantic import BaseModel, Field, EmailStr

# ------------ Core Domain Schemas ------------

class Client(BaseModel):
    full_name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password (store hashed in production)")
    goals: List[str] = Field(default_factory=list, description="Fitness goals multi-select")
    timezone: Optional[str] = Field(None, description="IANA timezone string")

class Trainer(BaseModel):
    full_name: str = Field(..., description="Full name")
    email: EmailStr = Field(..., description="Email address")
    password: str = Field(..., description="Password (store hashed in production)")
    specializations: List[str] = Field(default_factory=list, description="Areas of expertise")
    bio: Optional[str] = Field(None, description="Professional bio")
    certifications: List[str] = Field(default_factory=list, description="Certification names or IDs")
    verified: bool = Field(False, description="Verification flag")
    languages: List[str] = Field(default_factory=list, description="Languages spoken")
    timezone: Optional[str] = Field(None, description="IANA timezone string")
    price_30: Optional[float] = Field(None, ge=0, description="Price for 30 min session")
    price_60: Optional[float] = Field(None, ge=0, description="Price for 60 min session")
    rating: float = Field(4.9, ge=0, le=5, description="Average rating")
    reviews_count: int = Field(0, ge=0, description="Number of reviews")
    photo_url: Optional[str] = Field(None, description="Profile photo URL")
    availability: List[str] = Field(default_factory=list, description="Simple availability slots e.g., 'Mon 09:00-12:00'")

class Review(BaseModel):
    trainer_id: str = Field(..., description="Trainer document _id as string")
    client_name: str = Field(..., description="Name of reviewer")
    rating: float = Field(..., ge=0, le=5)
    comment: Optional[str] = None

class Waitlist(BaseModel):
    email: EmailStr

# Optional placeholder for bookings/payments for future extension
class Booking(BaseModel):
    trainer_id: str
    client_id: str
    length_minutes: int = Field(..., ge=15, le=180)
    price_paid: float = Field(..., ge=0)
    status: str = Field("pending", description="pending|confirmed|completed|canceled")
    video_link: Optional[str] = None
