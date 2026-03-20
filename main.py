# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine
import models
from endpoint import items, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pantry-Sync API")

origins = [
    "http://localhost:4200",      
    # "http://ip:4200", 
    # "http://dominio.com",      
]

app.add_middleware(
    CORSMiddleware,
    allow_origins={"*"},  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"], 
)

import os
os.makedirs("uploads", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

app.include_router(auth.router)
app.include_router(items.router)

@app.get("/")
def home():
    return {"status": "Pantry-Sync Online", "version": "1.0.0"}