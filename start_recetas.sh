#!/bin/bash
# Script de inicio para el microservicio de Recetas en Render

echo "🍳 Iniciando Microservicio de Recetas..."
echo "Puerto: ${PORT:-8001}"

# Crear directorio para base de datos
mkdir -p /opt/render/project/src/data

# Iniciar el servicio
exec uvicorn servicio_recetas.app:app --host 0.0.0.0 --port ${PORT:-8001} --log-level info
