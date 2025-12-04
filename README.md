# 🍳 API Recetario de Cocina Familiar

API REST basada en microservicios para gestión de recetas de cocina y sus ingredientes.

## 📋 Descripción

Sistema de gestión de recetas con arquitectura de microservicios que permite crear, editar, eliminar y consultar recetas de cocina junto con sus ingredientes y pasos de preparación.

## 🏗️ Arquitectura

El proyecto está compuesto por 3 microservicios:

- **API Gateway** (Puerto 8000): Punto de entrada único que enruta las peticiones
- **Servicio de Recetas** (Puerto 8001): Gestiona recetas y pasos de preparación
- **Servicio de Ingredientes** (Puerto 8002): Gestiona ingredientes

## 🚀 Tecnologías

- **FastAPI**: Framework web de alto rendimiento
- **SQLAlchemy**: ORM para manejo de base de datos
- **SQLite**: Base de datos ligera
- **Docker & Docker Compose**: Contenedorización y orquestación
- **Pytest**: Framework de testing
- **Uvicorn**: Servidor ASGI

## 📦 Instalación y Ejecución

### Con Docker Compose (Recomendado)

```bash
# Construir y levantar los servicios
docker-compose up --build

# Modo detached (segundo plano)
docker-compose up -d

# Detener los servicios
docker-compose down
```

### Sin Docker

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar cada servicio en terminales separadas
python -m uvicorn api_gateway.app:app --host 0.0.0.0 --port 8000
python -m uvicorn servicio_recetas.app:app --host 0.0.0.0 --port 8001
python -m uvicorn servicio_ingredientes.app:app --host 0.0.0.0 --port 8002
```

## 🧪 Pruebas

```bash
# Ejecutar todas las pruebas
pytest tests/ -v

# Con cobertura
pytest tests/ -v --cov

# Pruebas específicas
pytest tests/test_recetas.py -v
pytest tests/test_ingredientes.py -v
pytest tests/test_gateway.py -v
```

### ✅ Resultados de las Pruebas

- **41/41 pruebas pasando** (100% de éxito)
- 12 pruebas del API Gateway
- 16 pruebas del servicio de Ingredientes
- 13 pruebas del servicio de Recetas

## 📖 Documentación de la API

Una vez que los servicios estén corriendo, puedes acceder a la documentación interactiva:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📬 Colección de Postman

El proyecto incluye una colección completa de Postman con ejemplos de uso:
- `Recetario_API.postman_collection.json`

## 🌐 Endpoints Principales

### API Gateway

- `GET /` - Información del API
- `GET /health` - Estado de los servicios

### Ingredientes

- `GET /api/ingredientes/` - Listar ingredientes
- `POST /api/ingredientes/` - Crear ingrediente
- `GET /api/ingredientes/{id}` - Obtener ingrediente
- `PUT /api/ingredientes/{id}` - Actualizar ingrediente
- `DELETE /api/ingredientes/{id}` - Eliminar ingrediente
- `GET /api/ingredientes/buscar/{nombre}` - Buscar por nombre

### Recetas

- `GET /api/recetas/` - Listar recetas
- `POST /api/recetas/` - Crear receta
- `GET /api/recetas/{id}` - Obtener receta
- `PUT /api/recetas/{id}` - Actualizar receta
- `DELETE /api/recetas/{id}` - Eliminar receta
- `POST /api/recetas/{id}/pasos` - Agregar paso
- `DELETE /api/recetas/{id}/pasos/{paso_id}` - Eliminar paso

## 📁 Estructura del Proyecto

```
apiRecetas/
├── api_gateway/          # API Gateway
│   ├── app.py
│   └── Dockerfile
├── servicio_recetas/     # Microservicio de Recetas
│   ├── app.py
│   └── Dockerfile
├── servicio_ingredientes/ # Microservicio de Ingredientes
│   ├── app.py
│   └── Dockerfile
├── database/             # Modelos y configuración de BD
│   ├── __init__.py
│   ├── db_config.py
│   └── models.py
├── tests/                # Pruebas unitarias
│   ├── test_gateway.py
│   ├── test_recetas.py
│   └── test_ingredientes.py
├── docker-compose.yml    # Orquestación de contenedores
├── requirements.txt      # Dependencias Python
└── README.md
```

## 🔧 Variables de Entorno

Las variables de entorno se configuran en `docker-compose.yml`:

- `RECETAS_SERVICE_URL`: URL del servicio de recetas
- `INGREDIENTES_SERVICE_URL`: URL del servicio de ingredientes
- `DATABASE_URL`: Ruta de la base de datos SQLite

## 📝 Ejemplo de Uso

### Crear un Ingrediente

```bash
curl -X POST http://localhost:8000/api/ingredientes/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Tomate",
    "unidad_medida": "gramos",
    "categoria": "vegetales"
  }'
```

### Crear una Receta

```bash
curl -X POST http://localhost:8000/api/recetas/ \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "Pasta Carbonara",
    "descripcion": "Receta italiana clásica",
    "tiempo_preparacion": 25,
    "porciones": 4,
    "pasos": [
      {
        "numero_paso": 1,
        "descripcion": "Hervir agua con sal"
      }
    ]
  }'
```

## 🌐 Despliegue en Producción

### Desplegar en Render

Este proyecto está configurado para desplegarse automáticamente en Render:

1. **Push a GitHub:**
   ```bash
   git push origin master
   ```

2. **Crear Blueprint en Render:**
   - Ve a [Render Dashboard](https://dashboard.render.com/)
   - Clic en **New +** → **Blueprint**
   - Conecta tu repositorio
   - Render detectará automáticamente `render.yaml` y desplegará los 3 servicios

3. **Acceder a tu API:**
   - URL: `https://api-recetario-gateway.onrender.com`
   - Docs: `https://api-recetario-gateway.onrender.com/docs`

📖 **Guía completa:** Lee [DEPLOY.md](DEPLOY.md) para instrucciones detalladas.

### Otras Plataformas

- **Heroku**: Usa el `Procfile` incluido
- **Railway**: Compatible con Docker Compose
- **AWS/Azure/GCP**: Usa los Dockerfiles individuales

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add: nueva característica'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

## 👨‍💻 Autor

Valentina Barreto - [GitHub](https://github.com/valentinaBarreto18)

Proyecto desarrollado como demostración de arquitectura de microservicios con FastAPI.

## 🔗 Links

- **Repositorio:** https://github.com/valentinaBarreto18/parcial3_python
- **Documentación de Despliegue:** [DEPLOY.md](DEPLOY.md)
- **Colección Postman:** [Recetario_API.postman_collection.json](Recetario_API.postman_collection.json)

---

⭐ Si te gusta este proyecto, dale una estrella en GitHub!
