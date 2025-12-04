# Dockerfile para API Gateway
FROM python:3.11-slim

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código del gateway y la base de datos
COPY api_gateway/ ./api_gateway/
COPY database/ ./database/

# Exponer puerto
EXPOSE 8000

# Comando para ejecutar
CMD ["python", "-m", "uvicorn", "api_gateway.app:app", "--host", "0.0.0.0", "--port", "8000"]
