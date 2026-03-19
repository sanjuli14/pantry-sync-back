# endpoint/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import schemas, auth
from database import get_db
from datetime import timedelta

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/register", response_model=schemas.UserResponse)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = auth.get_user_by_alias(db, user.alias)
    if existing:
        raise HTTPException(status_code=400, detail="El alias ya está registrado")
    
    existing_phone = auth.get_user_by_phone(db, user.phone)
    if existing_phone:
        raise HTTPException(status_code=400, detail="El teléfono ya está registrado")
    
    return auth.register_user(db, user)

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Alias o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = auth.create_access_token(
        data={"sub": str(user.id)},
        expires_delta=timedelta(hours=auth.ACCESS_TOKEN_EXPIRE_HOURS)
    )
        
    print(f"=== LOGIN ===")
    print(f"User ID: {user.id}")
    print(f"Token created: {access_token[:30]}...")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": auth.ACCESS_TOKEN_EXPIRE_HOURS * 3600
    }

@router.get("/me", response_model=schemas.UserResponse)
def get_me(current_user: auth.models.User = Depends(auth.get_current_user)):
    return current_user
