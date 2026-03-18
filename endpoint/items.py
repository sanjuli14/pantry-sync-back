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

@router .get("/", response_model=List[schemas.ItemResponse])
def read_items(db: Session = Depends(get_db)):
    return endpoint.get_items(db)

@router.get("/zone/{zone}", response_model=List[schemas.ItemResponse])
def read_items_by_zone(zone: str, db: Session = Depends(get_db)):
    return endpoint.get_items_by_zone(db, zone=zone)

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    success = endpoint.delete_item(db, item_id=item_id)
    if not success:
        raise HTTPException(status_code=404, detail="El producto no existe")
    return {"message": "Producto retirado con éxito"}