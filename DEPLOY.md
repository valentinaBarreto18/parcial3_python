# Guía de Despliegue en Render

## 🚀 Pasos para Desplegar

### 1. Subir a GitHub

```bash
git init
git add .
git commit -m "API Recetario"
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### 2. Crear Web Service en Render

1. Ir a [https://render.com](https://render.com) y crear cuenta
2. Clic en **"New +"** → **"Web Service"**
3. Conectar repositorio de GitHub

### 3. Configuración

```
Name: api-recetario
Runtime: Python 3
Build Command: pip install -r requirements.txt
Start Command: chmod +x start.sh && ./start.sh
Instance Type: Free
```

### 4. Variables de Entorno

```
RECETAS_SERVICE_URL=http://localhost:8001
INGREDIENTES_SERVICE_URL=http://localhost:8002
DATABASE_URL=sqlite:////opt/render/project/data/recetario.db
PYTHON_VERSION=3.11.0
```

### 5. Desplegar

Clic en **"Create Web Service"** y esperar 5-10 minutos.

## 📡 Acceder a la API

- URL Base: `https://tu-servicio.onrender.com`
- Documentación: `https://tu-servicio.onrender.com/docs`
- Health Check: `https://tu-servicio.onrender.com/health`

## ⚠️ Notas

- Plan gratuito: El servicio duerme después de 15 min de inactividad
- Primera petición: Puede tardar 30-60 segundos en despertar
- SQLite: Los datos se pierden en reinicios (usar PostgreSQL para persistencia)
