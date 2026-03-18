# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from endpoint import items  # Importamos nuestro router

# Creamos las tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pantry-Sync API")

# CORS (Se queda aquí porque es configuración global)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# REGISTRAMOS EL ROUTER
app.include_router(items.router)

@app.get("/")
def home():
    return {"status": "Pantry-Sync Online", "architecture": "Modular"}