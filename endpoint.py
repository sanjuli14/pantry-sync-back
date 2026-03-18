# crud.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
import models, schemas

# Configuración de tiempos por categoría (en horas)
EXPIRY_TIMES = {
    "Frutas/Vegetales": 48,
    "Panadería": 24,
    "Lácteos": 72,
    "Enlatados": 720,  # 30 días
    "Higiene": 2160,   # 90 días
    "Otros": 48
}

def create_item(db: Session, item: schemas.ItemCreate):
    # 1. Buscamos cuánto dura según la categoría
    hours = EXPIRY_TIMES.get(item.category, 48)
    
    # 2. Calculamos la fecha exacta de muerte del post
    expiration = datetime.utcnow() + timedelta(hours=hours)
    
    db_item = models.Item(
        title=item.title,
        description=item.description,
        zone=item.zone,
        category=item.category,
        contact=item.contact,
        expires_at=expiration # <--- Esto debe estar en tu models.py
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_active_items(db: Session):
    # Solo devolvemos lo que NO ha expirado
    now = datetime.utcnow()
    return db.query(models.Item).filter(models.Item.expires_at > now).all()

def delete_expired_items(db: Session):
    now = datetime.utcnow()
    expired = db.query(models.Item).filter(models.Item.expires_at < now)
    count = expired.count()
    expired.delete(synchronize_session=False)
    db.commit()
    return count