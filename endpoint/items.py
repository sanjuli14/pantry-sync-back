# routers/items.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import schemas, endpoint, models
from database import get_db

router = APIRouter(
    prefix="/items",
    tags=["Items"] # Esto organiza el /docs automáticamente
)

@router.post("/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return endpoint.create_item(db=db, item=item)

@router.get("/", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    # Usamos la nueva función que filtra expirados
    return endpoint.get_active_items(db)

@router.get("/zone/{zone}", response_model=List[schemas.ItemResponse])
def read_items_by_zone(zone: str, db: Session = Depends(get_db)):
    return endpoint.get_items_by_zone(db, zone=zone)

@router.delete("/system/cleanup", tags=["System"])
def cleanup(db: Session = Depends(get_db)):
    deleted = endpoint.delete_expired_items(db)
    return {"message": f"Se limpiaron {deleted} productos viejos."}