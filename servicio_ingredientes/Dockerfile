# Dockerfile para Microservicio de Ingredientes
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del servicio y la base de datos
COPY servicio_ingredientes/ ./servicio_ingredientes/
COPY database/ ./database/

# Exponer puerto
EXPOSE 8002

# Comando para ejecutar
CMD ["python", "-m", "uvicorn", "servicio_ingredientes.app:app", "--host", "0.0.0.0", "--port", "8002"]
