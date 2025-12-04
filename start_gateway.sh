#!/bin/bash
# Script de inicio para el API Gateway en Render

echo "🚀 Iniciando API Gateway..."
echo "Puerto: ${PORT:-8000}"

# Crear directorio para base de datos
mkdir -p /opt/render/project/src/data

# Iniciar el servicio
exec uvicorn api_gateway.app:app --host 0.0.0.0 --port ${PORT:-8000} --log-level info
