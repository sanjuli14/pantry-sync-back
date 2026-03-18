# models.py (Añade o actualiza el campo)
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    zone = Column(String, index=True)
    category = Column(String)
    contact = Column(String)
    created_at = Column(DateTime, default=datetime.now(datetime.now().astimezone().tzinfo))  # Guarda con zona horaria local
    # Nueva columna:
    expires_at = Column(DateTime)