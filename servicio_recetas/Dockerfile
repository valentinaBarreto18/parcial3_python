# Dockerfile para Microservicio de Recetas
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio y la base de datos
COPY servicio_recetas/ ./servicio_recetas/
COPY database/ ./database/

# Exponer puerto
EXPOSE 8001

# Comando para ejecutar
CMD ["python", "-m", "uvicorn", "servicio_recetas.app:app", "--host", "0.0.0.0", "--port", "8001"]
