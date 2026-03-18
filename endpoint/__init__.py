# endpoint/__init__.py
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
import models, schemas
import math

EXPIRY_TIMES = {
    "Frutas/Vegetales": 48,
    "Panadería": 24,
    "Lácteos": 72,
    "Enlatados": 720,
    "Higiene": 2160,
    "Otros": 48
}

def create_item(db: Session, item: schemas.ItemCreate, user_id: int = None):
    hours = EXPIRY_TIMES.get(item.category, 48)
    expiration = datetime.utcnow() + timedelta(hours=hours)
    
    db_item = models.Item(
        title=item.title,
        description=item.description,
        zone=item.zone,
        category=item.category,
        contact=item.contact,
        latitude=item.latitude,
        longitude=item.longitude,
        user_id=user_id,
        expires_at=expiration
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_active_items(db: Session):
    now = datetime.utcnow()
    return db.query(models.Item).filter(models.Item.expires_at > now).all()

def get_user_items(db: Session, user_id: int):
    now = datetime.utcnow()
    return db.query(models.Item).filter(
        and_(models.Item.user_id == user_id, models.Item.expires_at > now)
    ).all()

def get_items_by_zone(db: Session, zone: str):
    now = datetime.utcnow()
    return db.query(models.Item).filter(
        and_(models.Item.zone == zone, models.Item.expires_at > now)
    ).all()

def get_nearby_items(db: Session, lat: float, lng: float, radius_km: float):
    now = datetime.utcnow()
    all_items = db.query(models.Item).filter(models.Item.expires_at > now).all()
    
    nearby = []
    for item in all_items:
        if item.latitude is not None and item.longitude is not None:
            distance = haversine_distance(lat, lng, item.latitude, item.longitude)
            if distance <= radius_km:
                nearby.append({
                    "item": item,
                    "distance_km": round(distance, 2)
                })
    
    nearby.sort(key=lambda x: x["distance_km"])
    return nearby

def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    
    lat1_rad = math.radians(lat1)
    lat2_rad = math.radians(lat2)
    delta_lat = math.radians(lat2 - lat1)
    delta_lon = math.radians(lon2 - lon1)
    
    a = math.sin(delta_lat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(delta_lon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    
    return R * c

def update_item_image(db: Session, item_id: int, image_url: str):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        item.image_url = image_url
        db.commit()
        db.refresh(item)
    return item

def delete_item(db: Session, item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()

def delete_expired_items(db: Session):
    now = datetime.utcnow()
    expired = db.query(models.Item).filter(models.Item.expires_at < now)
    count = expired.count()
    expired.delete(synchronize_session=False)
    db.commit()
    return count
