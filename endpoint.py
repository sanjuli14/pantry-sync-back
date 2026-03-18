# crud.py
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
import models, schemas

def create_item(db: Session, item: schemas.ItemCreate):
    # Calculamos el momento de expiración
    expiration = datetime.utcnow() + timedelta(hours=item.duration_hours)
    
    # Creamos el objeto para la DB, excluyendo duration_hours que no está en el modelo
    db_item = models.Item(
        title=item.title,
        description=item.description,
        zone=item.zone,
        category=item.category,
        contact=item.contact,
        expires_at=expiration
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def delete_expired_items(db: Session):
    now = datetime.utcnow()
    expired = db.query(models.Item).filter(models.Item.expires_at < now)
    count = expired.count()
    expired.delete(synchronize_session=False)
    db.commit()
    return count

def delete_item(db: Session, item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item:
        db.delete(db_item)
        db.commit()
        return True
    return False