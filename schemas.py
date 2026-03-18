# schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ItemBase(BaseModel):
    title: str
    description: str
    zone: str
    category: str
    contact: str
    # El usuario puede mandar cuántas horas dura el producto

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int
    created_at: datetime
    expires_at: datetime # Para mostrarlo en Angular

    class Config:
        from_attributes = True