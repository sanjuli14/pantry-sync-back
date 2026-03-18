# Usamos la imagen oficial de Python basada en Debian Bookworm (estable para Debian 13)
FROM python:3.11-slim-bookworm

# Evitamos archivos temporales de Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# --- LIMPIEZA DE VULNERABILIDADES ---
# Actualizamos los índices, subimos de versión los paquetes instalados
# y borramos la caché para que la imagen no pese de más.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Instalamos dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiamos tu código modular
COPY . .

# Exponemos el puerto de FastAPI
EXPOSE 8000

# Ejecutamos con el host 0.0.0.0 para que CubePath lo vea
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]