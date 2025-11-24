# 🔧 Solución de Problemas - Render

Guía para diagnosticar y resolver problemas comunes al desplegar en Render.

## ❌ Error 502 Bad Gateway

### Síntomas
- El frontend carga correctamente
- Al intentar subir un documento, aparece error 502
- En la consola del navegador: `Failed to load resource: the server responded with a status of 502`

### Diagnóstico

#### 1. Verificar que el Backend esté funcionando

En Render Dashboard:
1. Ve a tu servicio `jurismed-backend`
2. Verifica que el estado sea **🟢 Live**
3. Ve a la pestaña **Logs**
4. Verifica que no haya errores críticos

#### 2. Probar el Backend directamente

Abre en tu navegador:
```
https://tu-backend.onrender.com/health
```

Deberías ver:
```json
{"status": "healthy"}
```

Si ves un error o el servicio no responde:
- ✅ **El backend está dormido**: En Render Free, los servicios se duermen después de 15 minutos de inactividad. La primera petición puede tardar 30-60 segundos en "despertar".
- ❌ **El backend tiene errores**: Revisa los logs en Render Dashboard

#### 3. Verificar la configuración del Frontend

En Render Dashboard:
1. Ve a tu servicio `jurismed-frontend`
2. Ve a **Environment**
3. Verifica que exista la variable `BACKEND_HOST` o `BACKEND_URL`

**Si falta o está incorrecta**, agrega manualmente:
```
BACKEND_URL=https://jurismed-backend.onrender.com
```

⚠️ **Importante**: Reemplaza `jurismed-backend` con el nombre real de tu servicio backend.

#### 4. Verificar los Logs del Frontend

En Render Dashboard → Frontend Service → Logs:
- Busca: `Nginx config generated with BACKEND_URL: ...`
- Verifica que la URL sea correcta (debe ser `https://...`)
- Busca errores de nginx

#### 5. Verificar los Logs del Backend

En Render Dashboard → Backend Service → Logs:
- Busca errores de Python
- Verifica que la aplicación esté iniciando correctamente
- Busca mensajes de uvicorn como: `Uvicorn running on http://0.0.0.0:8000`

### Soluciones

#### Solución 1: Configurar BACKEND_URL manualmente

1. En Render Dashboard, ve a **Frontend Service → Environment**
2. Agrega nueva variable:
   - **Key**: `BACKEND_URL`
   - **Value**: `https://jurismed-backend.onrender.com`
   (reemplaza con tu URL real)
3. Guarda y espera a que se redespliegue

#### Solución 2: Verificar que el Backend esté despierto

1. Haz una petición directa al backend: `https://tu-backend.onrender.com/health`
2. Espera 30-60 segundos (si estaba dormido)
3. Luego intenta subir el documento desde el frontend

#### Solución 3: Aumentar timeouts

Si el backend tarda mucho en procesar (archivos grandes):
- Los timeouts ya están configurados a 300 segundos
- Si necesitas más, puedes ajustarlos en `frontend/entrypoint.sh`

## ⏱️ Error: Timeout

### Síntomas
- El documento se está subiendo pero nunca termina
- Después de varios minutos, aparece error de timeout

### Solución

En Render Free, hay límites de tiempo. Para archivos grandes:
1. Reduce el tamaño del archivo (máximo 10MB)
2. O considera actualizar al plan Starter ($7/mes) que tiene más recursos

## 🔍 Cómo verificar la configuración

### Ver la configuración de nginx generada

1. Ve a Frontend Service → Logs
2. Busca: `Nginx config generated with BACKEND_URL:`
3. Verifica que la URL sea correcta

### Probar la conexión manualmente

Desde tu terminal (o usar Postman):

```bash
# Probar health check
curl https://tu-backend.onrender.com/health

# Probar endpoint de análisis (con archivo)
curl -X POST https://tu-backend.onrender.com/api/analyze \
  -F "file=@documento.pdf" \
  -F "document_type=clinical"
```

## 📊 Verificar Estado de los Servicios

### Backend
- **URL**: `https://jurismed-backend.onrender.com`
- **Health Check**: `https://jurismed-backend.onrender.com/health`
- **Docs**: `https://jurismed-backend.onrender.com/docs`

### Frontend
- **URL**: `https://jurismed-frontend.onrender.com`

## 🔄 Reiniciar Servicios

Si algo no funciona, intenta reiniciar:

1. En Render Dashboard, ve al servicio
2. Click en **Manual Deploy**
3. Selecciona **Clear build cache & deploy**

## 📝 Verificar Variables de Entorno

### Frontend debe tener:
- `BACKEND_HOST` (automático desde render.yaml) O
- `BACKEND_URL` (manual: `https://jurismed-backend.onrender.com`)

### Backend debe tener:
- `CORS_ORIGINS` (debe incluir la URL del frontend)
- `PYTHONUNBUFFERED=1`

## 🐛 Logs Útiles

### Frontend Logs (buscar):
```
Nginx config generated with BACKEND_URL: ...
Backend hostname extracted: ...
Nginx configuration is valid
```

### Backend Logs (buscar):
```
Uvicorn running on http://0.0.0.0:8000
Application startup complete
```

## 💡 Consejos

1. **Primera vez**: Puede tardar 10-15 minutos en desplegar completamente
2. **Servicios dormidos**: La primera petición después de 15min inactivos puede tardar 30-60 segundos
3. **Logs**: Revisa siempre los logs en Render Dashboard cuando hay errores
4. **URLs**: Verifica que las URLs sean exactas (con https://)

## ❓ ¿Aún no funciona?

Si después de seguir estos pasos el error persiste:

1. **Verifica los logs completos** en Render Dashboard
2. **Prueba el backend directamente** en tu navegador
3. **Verifica que las URLs sean correctas** en las variables de entorno
4. **Asegúrate de que ambos servicios estén en "Live"**

Si el problema continúa, comparte:
- Logs del frontend (especialmente la línea con BACKEND_URL)
- Logs del backend
- URL exacta de tu backend
- Respuesta del endpoint `/health` del backend

