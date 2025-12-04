# 🚀 Guía Completa de Despliegue en Render

Esta guía te ayudará a desplegar automáticamente los 3 microservicios de la API Recetario en Render.

## 📋 Prerequisitos

1. Cuenta en [GitHub](https://github.com)
2. Cuenta en [Render](https://render.com) (gratuita)
3. Código subido a tu repositorio de GitHub

---

## 🔧 Método 1: Despliegue Automático con Blueprint (RECOMENDADO)

Este método despliega los 3 servicios automáticamente usando el archivo `render.yaml`.

### Paso 1: Subir el código a GitHub

Si aún no lo has hecho:

```bash
git add .
git commit -m "Configuración para despliegue en Render"
git push origin master
```

### Paso 2: Crear Blueprint en Render

1. Ve a [Render Dashboard](https://dashboard.render.com/)
2. Haz clic en **"New +"** → **"Blueprint"**
3. Conecta tu repositorio de GitHub
4. Selecciona el repositorio `parcial3_python`
5. Render detectará automáticamente el archivo `render.yaml`
6. Haz clic en **"Apply"**

### Paso 3: Esperar el Despliegue

Render desplegará automáticamente:
- ✅ `api-recetario-gateway` (Puerto asignado dinámicamente)
- ✅ `api-recetario-recetas` (Puerto asignado dinámicamente)
- ✅ `api-recetario-ingredientes` (Puerto asignado dinámicamente)

El proceso toma **5-10 minutos** para cada servicio.

### Paso 4: Obtener las URLs

Una vez desplegados, encontrarás las URLs en:
- Dashboard → Services → `api-recetario-gateway`
- La URL será algo como: `https://api-recetario-gateway.onrender.com`

---

## 🛠️ Método 2: Despliegue Manual (Alternativo)

Si prefieres desplegar cada servicio manualmente:

### Desplegar Microservicio de Ingredientes

1. Clic en **"New +"** → **"Web Service"**
2. Conecta tu repositorio
3. Configuración:
   ```
   Name: api-recetario-ingredientes
   Region: Oregon (US West)
   Branch: master
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: chmod +x start_ingredientes.sh && ./start_ingredientes.sh
   Instance Type: Free
   ```
4. Variables de entorno:
   ```
   PYTHON_VERSION=3.13.7
   DATABASE_URL=sqlite:////opt/render/project/src/data/recetario.db
   ```
5. Clic en **"Create Web Service"**

### Desplegar Microservicio de Recetas

Repite el proceso con:
```
Name: api-recetario-recetas
Start Command: chmod +x start_recetas.sh && ./start_recetas.sh
```

### Desplegar API Gateway

1. Clic en **"New +"** → **"Web Service"**
2. Configuración:
   ```
   Name: api-recetario-gateway
   Start Command: chmod +x start_gateway.sh && ./start_gateway.sh
   ```
3. Variables de entorno:
   ```
   PYTHON_VERSION=3.13.7
   RECETAS_SERVICE_URL=https://api-recetario-recetas.onrender.com
   INGREDIENTES_SERVICE_URL=https://api-recetario-ingredientes.onrender.com
   DATABASE_URL=sqlite:////opt/render/project/src/data/recetario.db
   ```

**⚠️ IMPORTANTE:** Reemplaza las URLs con las URLs reales de tus microservicios desplegados.

---

## 📡 Acceder a tu API Desplegada

### URLs de Acceso

- **API Gateway:** `https://api-recetario-gateway.onrender.com`
- **Documentación Interactiva:** `https://api-recetario-gateway.onrender.com/docs`
- **Health Check:** `https://api-recetario-gateway.onrender.com/health`

### Probar con Postman

1. Abre tu colección `Recetario_API.postman_collection.json`
2. Ve a Variables de la colección
3. Actualiza `gateway_url` con tu URL de Render:
   ```
   gateway_url = https://api-recetario-gateway.onrender.com
   ```
4. Ejecuta los requests normalmente

### Ejemplo de Request

```bash
curl https://api-recetario-gateway.onrender.com/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "gateway": "operational",
  "services": {
    "recetas": "healthy",
    "ingredientes": "healthy"
  }
}
```

---

## 🔍 Monitoreo y Logs

### Ver Logs en Tiempo Real

1. Ve a tu Dashboard de Render
2. Selecciona el servicio que quieres monitorear
3. Haz clic en la pestaña **"Logs"**

### Health Checks

Render verifica automáticamente el endpoint `/health` cada 30 segundos. Si falla, intentará reiniciar el servicio.

---

## ⚠️ Limitaciones del Plan Gratuito

- **Suspensión por Inactividad:** Los servicios se duermen después de 15 minutos sin requests
- **Tiempo de Activación:** El primer request después de dormir tarda 30-60 segundos
- **Compartir Base de Datos:** SQLite no es ideal para múltiples instancias (considera PostgreSQL para producción)
- **750 horas/mes:** Por servicio (suficiente para 1 servicio 24/7)

### Solución para la Suspensión

Puedes usar un servicio de ping como [UptimeRobot](https://uptimerobot.com/) para mantener tu API activa:
- Crea un monitor HTTP(S)
- URL: `https://api-recetario-gateway.onrender.com/health`
- Intervalo: 5 minutos

---

## 🐛 Solución de Problemas

### Error: "Build Failed"

**Causa:** Problemas con dependencias.

**Solución:**
```bash
# Verifica que requirements.txt esté actualizado
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Actualizar dependencias"
git push
```

### Error: "Health Check Failed"

**Causa:** El servicio no responde en `/health`.

**Solución:**
1. Verifica los logs del servicio
2. Asegúrate de que el puerto sea `$PORT` (variable de Render)
3. Confirma que el endpoint `/health` existe en tu código

### Error: "Cannot connect to other services"

**Causa:** URLs de microservicios incorrectas.

**Solución:**
1. Ve a Settings → Environment Variables
2. Actualiza `RECETAS_SERVICE_URL` y `INGREDIENTES_SERVICE_URL` con las URLs correctas
3. Reinicia el servicio manualmente

### Base de Datos No Persiste

**Causa:** SQLite en disco efímero de Render.

**Solución a largo plazo:**
1. Considera migrar a PostgreSQL (Render ofrece base de datos gratuita)
2. O usa Render Disk para persistencia (plan de pago)

---

## 🔄 Actualizar el Despliegue

### Actualización Automática

Render despliega automáticamente cuando haces push a master:

```bash
git add .
git commit -m "Actualización de funcionalidad"
git push origin master
```

Render detectará el cambio y redesplegará en 3-5 minutos.

### Redespliegue Manual

1. Ve a tu servicio en Render Dashboard
2. Clic en **"Manual Deploy"** → **"Deploy latest commit"**

---

## 📊 Siguiente Nivel: Producción

Para un entorno de producción robusto:

### 1. Migrar a PostgreSQL

```python
# Render ofrece PostgreSQL gratuito
DATABASE_URL=postgresql://user:password@host/database
```

### 2. Usar Redis para Cache

```python
# Cachear respuestas frecuentes
REDIS_URL=redis://...
```

### 3. Implementar CORS Apropiado

```python
# api_gateway/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tu-frontend.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Agregar Autenticación

```python
# JWT tokens, OAuth, etc.
```

---

## 📞 Soporte

- **Documentación Render:** [docs.render.com](https://docs.render.com)
- **Comunidad Render:** [community.render.com](https://community.render.com)
- **Repositorio del Proyecto:** https://github.com/valentinaBarreto18/parcial3_python

---

## ✅ Checklist de Despliegue

- [ ] Código subido a GitHub
- [ ] Archivo `render.yaml` en el repositorio
- [ ] Blueprint creado en Render
- [ ] 3 servicios desplegados exitosamente
- [ ] Health checks respondiendo correctamente
- [ ] URLs actualizadas en Postman
- [ ] API funcionando con requests de prueba
- [ ] Logs monitoreados sin errores

¡Listo! Tu API está en producción 🎉

## ⚠️ Notas

- Plan gratuito: El servicio duerme después de 15 min de inactividad
- Primera petición: Puede tardar 30-60 segundos en despertar
- SQLite: Los datos se pierden en reinicios (usar PostgreSQL para persistencia)
