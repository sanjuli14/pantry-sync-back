FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

# ESTA LÍNEA ES CLAVE: Crea la carpeta para la base de datos
RUN mkdir -p /app/data

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]