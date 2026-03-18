# schemas.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    alias: str = Field(..., min_length=3, max_length=30)
    phone: str = Field(..., min_length=8, max_length=20)
    password: str = Field(..., min_length=4)

class UserLogin(BaseModel):
    alias: str
    password: str

class UserResponse(BaseModel):
    id: int
    alias: str
    phone: str
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(BaseModel):
    user_id: Optional[int] = None

class ItemBase(BaseModel):
    title: str
    description: str
    zone: str
    category: str
    contact: str
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    image_url: Optional[str] = None
    user_id: Optional[int] = None
    created_at: datetime
    expires_at: datetime

    class Config:
        from_attributes = True

class NearbyQuery(BaseModel):
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)
    radius_km: float = Field(default=0.5, gt=0, le=10)