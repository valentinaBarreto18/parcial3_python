#!/bin/bash
# Script de inicio para el microservicio de Ingredientes en Render

echo "🥕 Iniciando Microservicio de Ingredientes..."
echo "Puerto: ${PORT:-8002}"

# Crear directorio para base de datos
mkdir -p /opt/render/project/src/data

# Iniciar el servicio
exec uvicorn servicio_ingredientes.app:app --host 0.0.0.0 --port ${PORT:-8002} --log-level info
