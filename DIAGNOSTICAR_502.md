# 🔍 Guía Rápida: Diagnosticar Error 502 en Render

## Pasos para diagnosticar el error 502

### 1. Verificar que el Backend funcione directamente

Abre en tu navegador:
```
https://jurismed-backend.onrender.com/health
```

**Si funciona**: Verás `{"status": "healthy"}`  
**Si no funciona**: 
- El servicio puede estar dormido → Espera 30-60 segundos y recarga
- Hay un error en el backend → Revisa los logs en Render Dashboard

### 2. Verificar variables de entorno del Frontend

En Render Dashboard:
1. Ve a **jurismed-frontend** → **Environment**
2. Debe existir:
   - `BACKEND_HOST` = `jurismed-backend.onrender.com` (automático)
   - O `BACKEND_URL` = `https://jurismed-backend.onrender.com` (manual)

### 3. Ver Logs del Frontend

En Render Dashboard → Frontend Service → Logs:
- Busca: `Nginx config generated with BACKEND_URL:`
- La URL debe ser: `https://jurismed-backend.onrender.com` (sin `/` al final)
- Si tiene `/` al final, ese es el problema

### 4. Solución Rápida

**Configurar BACKEND_URL manualmente:**

1. En Render Dashboard → Frontend Service → Environment
2. Agregar nueva variable:
   ```
   Key: BACKEND_URL
   Value: https://jurismed-backend.onrender.com
   ```
   ⚠️ **Sin `/` al final** y reemplaza `jurismed-backend` con el nombre real de tu backend
3. Guardar y esperar a que se redespliegue

### 5. Verificar Logs del Backend

En Render Dashboard → Backend Service → Logs:
- Debe mostrar: `Uvicorn running on http://0.0.0.0:8000`
- No debe haber errores de Python

## Causas comunes del 502

1. **Backend dormido** (plan gratuito): Primera petición tarda 30-60 segundos
2. **URL incorrecta**: BACKEND_URL mal configurada o con `/` al final
3. **Backend con errores**: Revisa logs del backend
4. **CORS**: Aunque esto causaría error CORS, no 502

## Solución definitiva

Si después de configurar `BACKEND_URL` manualmente sigue fallando:
1. Verifica que el backend responda en `/health`
2. Verifica los logs de ambos servicios
3. Asegúrate de que ambos servicios estén en estado "Live"

