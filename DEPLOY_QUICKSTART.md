# 🚀 Guía Rápida de Despliegue en Render

## ⚡ Despliegue en 3 Pasos

### 1️⃣ Subir Código a GitHub

```bash
git add .
git commit -m "Configuración automática para Render"
git push origin master
```

### 2️⃣ Crear Blueprint en Render

1. Ir a: https://dashboard.render.com/
2. Clic en **"New +"** → **"Blueprint"**
3. Conectar repositorio: `valentinaBarreto18/parcial3_python`
4. Clic en **"Apply"**

### 3️⃣ ¡Listo! 🎉

En 5-10 minutos tendrás:
- ✅ API Gateway desplegado
- ✅ Microservicio de Recetas desplegado
- ✅ Microservicio de Ingredientes desplegado

---

## 📡 Acceder a tu API

Tu API estará disponible en:
```
https://api-recetario-gateway.onrender.com
```

### Endpoints principales:

- **Documentación:** `/docs`
- **Health Check:** `/health`
- **Recetas:** `/api/recetas/`
- **Ingredientes:** `/api/ingredientes/`

---

## 🧪 Probar con Postman

1. Abre `Recetario_API.postman_collection.json`
2. Edita la variable `gateway_url`:
   ```
   gateway_url = https://api-recetario-gateway.onrender.com
   ```
3. ¡Ejecuta tus requests!

---

## 🔍 Archivos Clave para Render

- **`render.yaml`** - Configuración de los 3 servicios
- **`start_gateway.sh`** - Script de inicio del Gateway
- **`start_recetas.sh`** - Script de inicio de Recetas
- **`start_ingredientes.sh`** - Script de inicio de Ingredientes
- **`requirements.txt`** - Dependencias de Python

---

## ⚠️ Importante

### Plan Gratuito de Render:
- ✅ 750 horas/mes por servicio
- ⚠️ Los servicios se duermen después de 15 minutos sin uso
- ⏱️ Primera petición después de dormir: 30-60 segundos

### Mantener Activo (Opcional):
Usa [UptimeRobot](https://uptimerobot.com/) para hacer ping cada 5 minutos:
```
https://api-recetario-gateway.onrender.com/health
```

---

## 🆘 Solución de Problemas

### Build Falla
```bash
# Actualizar dependencias
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Fix: actualizar dependencias"
git push
```

### Health Check Falla
1. Verifica logs en Render Dashboard
2. Confirma que el endpoint `/health` existe
3. Asegúrate de usar el puerto `$PORT`

### Servicios No Se Conectan
1. Ve a Settings → Environment Variables
2. Verifica URLs de `RECETAS_SERVICE_URL` y `INGREDIENTES_SERVICE_URL`
3. Reinicia el servicio manualmente

---

## 📚 Documentación Completa

Lee [DEPLOY.md](DEPLOY.md) para:
- Configuración detallada
- Despliegue manual paso a paso
- Migración a PostgreSQL
- Monitoreo y logs
- Mejores prácticas de producción

---

## 🎯 Checklist

- [ ] Código en GitHub
- [ ] Blueprint creado en Render
- [ ] 3 servicios desplegados
- [ ] Health checks OK
- [ ] API funciona correctamente
- [ ] Postman actualizado con nueva URL

---

**¿Necesitas ayuda?** Consulta [DEPLOY.md](DEPLOY.md) o la [documentación de Render](https://docs.render.com).
