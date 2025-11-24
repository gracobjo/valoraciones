# 🔧 Solución Rápida: Error 502 Bad Gateway

## Diagnóstico Inmediato

### Paso 1: Verificar que el Backend funcione

Abre en tu navegador (o usa curl):
```
https://jurismed-backend.onrender.com/health
```

**✅ Si responde**: Verás `{"status": "healthy"}`  
**❌ Si NO responde o tarda mucho**:
- El servicio está **dormido** (plan gratuito de Render)
- Espera 30-60 segundos y recarga
- Si sigue sin responder, hay un error en el backend

### Paso 2: Verificar Variables de Entorno del Frontend

En Render Dashboard:
1. Ve a **jurismed-frontend** → **Environment**
2. Debe existir una de estas variables:
   - `BACKEND_HOST` = `jurismed-backend.onrender.com`
   - O `BACKEND_URL` = `https://jurismed-backend.onrender.com`

**Si falta**, agrega manualmente:
```
BACKEND_URL=https://jurismed-backend.onrender.com
```
⚠️ **IMPORTANTE**: Reemplaza `jurismed-backend` con el nombre **real** de tu servicio backend en Render.

### Paso 3: Ver Logs del Frontend

En Render Dashboard → Frontend Service → **Logs**:
1. Busca la línea: `Nginx config generated with BACKEND_URL:`
2. Verifica que la URL sea: `https://jurismed-backend.onrender.com` (sin `/` al final)
3. Busca errores de nginx como: `connect() failed` o `upstream`

### Paso 4: Ver Logs del Backend

En Render Dashboard → Backend Service → **Logs**:
1. Debe mostrar: `Uvicorn running on http://0.0.0.0:8000`
2. No debe haber errores de Python
3. Si hay errores, copia y revisa el mensaje completo

## Soluciones

### Solución 1: Configurar BACKEND_URL Manualmente (RECOMENDADO)

1. **Render Dashboard** → **jurismed-frontend** → **Environment**
2. Click en **"Add Environment Variable"**
3. Agregar:
   - **Key**: `BACKEND_URL`
   - **Value**: `https://jurismed-backend.onrender.com`
   (reemplaza con tu URL real)
4. **Guardar** y esperar a que se redespliegue (2-3 minutos)

### Solución 2: Despertar el Backend

Si el backend está dormido:
1. Ve a: `https://jurismed-backend.onrender.com/health`
2. Espera 30-60 segundos (puede tardar en "despertar")
3. Debería responder: `{"status": "healthy"}`
4. Luego intenta subir el documento de nuevo

### Solución 3: Verificar que el Backend tenga CORS configurado

En Render Dashboard → Backend Service → **Environment**:
- Debe existir: `CORS_ORIGINS`
- Valor debe incluir: `https://jurismed-frontend.onrender.com`

Si falta o está mal:
```
CORS_ORIGINS=https://jurismed-frontend.onrender.com
```

### Solución 4: Reiniciar Servicios

1. **Render Dashboard** → Servicio → **Manual Deploy**
2. Selecciona **"Clear build cache & deploy"**
3. Espera a que termine el despliegue

## Verificación Final

Una vez configurado, verifica:

1. **Backend responde**: `https://tu-backend.onrender.com/health` → `{"status": "healthy"}`
2. **Frontend tiene BACKEND_URL**: Render Dashboard → Frontend → Environment
3. **Ambos servicios están "Live"**: Render Dashboard → ambos servicios deben estar en verde
4. **Logs sin errores**: Revisa logs de ambos servicios

## Causas Comunes del 502

| Causa | Síntoma | Solución |
|-------|---------|----------|
| Backend dormido | Primera petición tarda 30-60s | Esperar y recargar |
| BACKEND_URL incorrecta | Logs muestran URL errónea | Configurar manualmente |
| Backend con errores | Logs del backend muestran errores | Revisar y corregir errores |
| CORS mal configurado | Error 403 en lugar de 502 | Verificar CORS_ORIGINS |

## URLs para Verificar

- **Frontend**: `https://jurismed-frontend.onrender.com`
- **Backend Health**: `https://jurismed-backend.onrender.com/health`
- **Backend Docs**: `https://jurismed-backend.onrender.com/docs`

## Si Nada Funciona

1. **Verifica los logs completos** de ambos servicios
2. **Prueba el backend directamente** con Postman o curl
3. **Verifica que las URLs sean exactas** (con https://, sin / al final)
4. **Asegúrate de que ambos servicios estén en el mismo plan** (ambos free o ambos starter)

## Contacto

Si el problema persiste después de seguir estos pasos, comparte:
- Logs del frontend (especialmente la línea con BACKEND_URL)
- Logs del backend
- Respuesta de `https://tu-backend.onrender.com/health`
- Estado de las variables de entorno del frontend

