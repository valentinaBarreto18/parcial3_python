#!/bin/bash

# Script de inicio para Render
# Inicia los tres servicios en background y el gateway en foreground

echo "Iniciando microservicios..."

# Crear directorio para la base de datos si no existe
mkdir -p /opt/render/project/data

# Iniciar microservicio de ingredientes en background
echo "Iniciando servicio de ingredientes..."
uvicorn servicio_ingredientes.app:app --host 0.0.0.0 --port 8002 &

# Iniciar microservicio de recetas en background
echo "Iniciando servicio de recetas..."
uvicorn servicio_recetas.app:app --host 0.0.0.0 --port 8001 &

# Esperar un poco para que los servicios inicien
sleep 5

# Iniciar API Gateway en foreground (este es el proceso principal)
echo "Iniciando API Gateway..."
uvicorn api_gateway.app:app --host 0.0.0.0 --port ${PORT:-8000}
