import os  # <--- Añade esta importación
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. Intentamos leer la ruta del .env; si no existe, usamos la local por defecto
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./pantry.db")

# 2. Creamos el engine (el resto se queda igual)
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()