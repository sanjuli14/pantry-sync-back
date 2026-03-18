# routers/items.py
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from typing import List, Optional
import schemas, endpoint, models, auth
from database import get_db
import os
import uuid
import shutil

router = APIRouter(
    prefix="/items",
    tags=["Items"]
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=schemas.ItemResponse)
def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_item = endpoint.create_item(db=db, item=item, user_id=current_user.id)
    return db_item

@router.get("/", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return endpoint.get_active_items(db)

@router.get("/nearby")
def read_nearby_items(
    lat: float = Query(..., ge=-90, le=90),
    lng: float = Query(..., ge=-180, le=180),
    radius: float = Query(default=0.5, gt=0, le=10),
    db: Session = Depends(get_db)
):
    return endpoint.get_nearby_items(db, lat, lng, radius)

@router.get("/mine", response_model=List[schemas.ItemResponse])
def read_my_items(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    return endpoint.get_user_items(db, current_user.id)

@router.get("/zone/{zone}", response_model=List[schemas.ItemResponse])
def read_items_by_zone(zone: str, db: Session = Depends(get_db)):
    return endpoint.get_items_by_zone(db, zone=zone)

@router.post("/{item_id}/image")
async def upload_item_image(
    item_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    if file.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(status_code=400, detail="Solo se permiten imágenes JPG, PNG o WebP")
    
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="No puedes subir imágenes a items de otros")
    
    ext = file.filename.split(".")[-1] if file.filename else "jpg"
    filename = f"{uuid.uuid4()}.{ext}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    image_url = f"/uploads/{filename}"
    updated_item = endpoint.update_item_image(db, item_id, image_url)
    
    return {"image_url": image_url, "item_id": item_id}

@router.delete("/{item_id}")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item no encontrado")
    
    if item.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Solo puedes eliminar tus propios items")
    
    endpoint.delete_item(db, item_id)
    return {"message": "Item eliminado"}

@router.delete("/system/cleanup", tags=["System"])
def cleanup(db: Session = Depends(get_db)):
    deleted = endpoint.delete_expired_items(db)
    return {"message": f"Se eliminaron {deleted} productos expirados."}