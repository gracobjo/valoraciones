# 🚀 Guía de Despliegue en Render

Esta guía te llevará paso a paso para desplegar JurisMed AI en Render.

## 📋 Prerequisitos

1. **Cuenta en Render**: Regístrate en [render.com](https://render.com) (puedes usar GitHub para registro)
2. **Repositorio en GitHub**: Tu código debe estar en GitHub (ya lo tienes en https://github.com/gracobjo/valoraciones.git)

## 🔧 Paso 1: Preparar el Repositorio

Ya está todo listo. El archivo `render.yaml` está configurado y listo para usar.

## 📦 Paso 2: Crear Servicios en Render

### Opción A: Despliegue Automático con render.yaml (Recomendado)

1. **Iniciar sesión en Render**:
   - Ve a https://dashboard.render.com
   - Inicia sesión con tu cuenta de GitHub

2. **Crear Nuevo Blueprint**:
   - Click en "New +" en la parte superior
   - Selecciona "Blueprint"
   - Conecta tu repositorio de GitHub `gracobjo/valoraciones`
   - Render detectará automáticamente el archivo `render.yaml`
   - Click en "Apply"

3. **Render creará automáticamente**:
   - Servicio backend (`jurismed-backend`)
   - Servicio frontend (`jurismed-frontend`)
   - Configurará las variables de entorno necesarias

### Opción B: Crear Servicios Manualmente

Si prefieres crear los servicios manualmente:

#### Backend Service

1. **Crear Web Service**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio: `gracobjo/valoraciones`

2. **Configuración**:
   - **Name**: `jurismed-backend`
   - **Region**: `Oregon (US West)`
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `backend/Dockerfile`
   - **Docker Context**: `backend`
   - **Plan**: `Free`

3. **Variables de Entorno**:
   ```
   CORS_ORIGINS=https://jurismed-frontend.onrender.com
   PYTHONUNBUFFERED=1
   ```

4. **Health Check Path**: `/health`

5. **Click en "Create Web Service"**

#### Frontend Service

1. **Esperar a que el backend termine de desplegar** (necesitas su URL)

2. **Crear otro Web Service**:
   - Click en "New +" → "Web Service"
   - Conecta el mismo repositorio: `gracobjo/valoraciones`

3. **Configuración**:
   - **Name**: `jurismed-frontend`
   - **Region**: `Oregon (US West)` (mismo que backend)
   - **Branch**: `main`
   - **Root Directory**: (dejar vacío)
   - **Runtime**: `Docker`
   - **Dockerfile Path**: `frontend/Dockerfile`
   - **Docker Context**: `frontend`
   - **Plan**: `Free`

4. **Variables de Entorno**:
   ```
   BACKEND_URL=https://jurismed-backend.onrender.com
   ```
   ⚠️ **Importante**: Reemplaza `jurismed-backend` con el nombre real de tu servicio backend

5. **Click en "Create Web Service"**

## ⏱️ Paso 3: Esperar el Despliegue

- **Primera vez**: Puede tardar 10-15 minutos mientras:
  - Descarga las imágenes base
  - Instala dependencias
  - Descarga modelos de ML (puede tardar varios minutos)
  - Construye las imágenes Docker

- **Despliegues siguientes**: 3-5 minutos normalmente

## ✅ Paso 4: Verificar el Despliegue

### Backend

1. Ve a la URL de tu servicio backend: `https://jurismed-backend.onrender.com`
2. Deberías ver: `{"name": "JurisMed AI API", ...}`
3. Ve a `https://jurismed-backend.onrender.com/health`
4. Deberías ver: `{"status": "healthy"}`
5. Ve a `https://jurismed-backend.onrender.com/docs`
6. Deberías ver la documentación Swagger

### Frontend

1. Ve a la URL de tu servicio frontend: `https://jurismed-frontend.onrender.com`
2. Deberías ver la interfaz de la aplicación
3. Intenta cargar un documento de prueba

## 🔄 Paso 5: Actualizar CORS (si es necesario)

Si el frontend y backend tienen nombres diferentes:

1. Ve al dashboard de Render
2. Selecciona tu servicio `jurismed-backend`
3. Ve a "Environment"
4. Actualiza `CORS_ORIGINS` con la URL completa de tu frontend:
   ```
   CORS_ORIGINS=https://tu-frontend-url.onrender.com
   ```
5. Click en "Save Changes"
6. Render reiniciará automáticamente el servicio

## 🐛 Solución de Problemas

### Error: "Service unavailable" o timeout

**Causa**: Los modelos ML están descargándose (primera vez)
**Solución**: Espera 10-15 minutos y recarga

### Error: CORS bloqueado

**Causa**: La URL del frontend no está en CORS_ORIGINS
**Solución**: 
1. Verifica la URL exacta de tu frontend
2. Actualiza `CORS_ORIGINS` en las variables de entorno del backend
3. Incluye la URL completa con `https://`

### Error: "502 Bad Gateway" en frontend

**Causa**: El backend no está disponible o la URL es incorrecta
**Solución**:
1. Verifica que el backend esté corriendo
2. Verifica que `BACKEND_URL` en el frontend apunte a la URL correcta
3. Asegúrate de que la URL termine con `/` (ej: `https://backend.onrender.com/`)

### El servicio se "duerme"

**Causa**: Los servicios gratuitos de Render se duermen después de 15 minutos de inactividad
**Solución**: 
- La primera petición después de dormir puede tardar 30-60 segundos en "despertar"
- Esto es normal en el plan gratuito
- Considera un servicio de ping para mantenerlo despierto (opcional)

### Build falla por falta de memoria

**Causa**: Los modelos ML requieren mucha memoria durante el build
**Solución**: 
- Render Free tiene límites. Si falla, considera:
  - Usar un modelo más pequeño de spaCy (`es_core_news_sm` ya está configurado)
  - O actualizar al plan Starter ($7/mes) que tiene más recursos

## 📊 Monitoreo

### Ver Logs

1. Ve a tu servicio en Render Dashboard
2. Click en "Logs"
3. Puedes ver logs en tiempo real

### Ver Estado

1. Cada servicio muestra su estado:
   - 🟢 Live: Funcionando
   - 🟡 Building: Construyendo
   - 🔴 Failed: Error

## 🔐 Configuración Adicional (Opcional)

### Dominio Personalizado

1. Ve a tu servicio
2. Click en "Settings"
3. Scroll hasta "Custom Domains"
4. Agrega tu dominio
5. Sigue las instrucciones para configurar DNS

### Variables de Entorno Adicionales

Puedes agregar más variables según necesites:

**Backend**:
```
LOG_LEVEL=info
MAX_UPLOAD_SIZE=10485760  # 10MB
```

**Frontend**:
```
ENABLE_ANALYTICS=false
```

## 📝 Notas Importantes

1. **Plan Gratuito**:
   - ✅ 750 horas/mes gratis
   - ⚠️ Servicios se duermen después de 15min inactividad
   - ⚠️ Límite de 512MB RAM por servicio
   - ⚠️ Builds pueden tardar más tiempo

2. **Primera Vez**:
   - El build inicial puede tardar 15-20 minutos
   - Los modelos ML se descargan automáticamente

3. **Actualizaciones**:
   - Cada push a `main` despliega automáticamente
   - Puedes hacer deploy manual desde el dashboard

## ✅ Checklist de Despliegue

- [ ] Cuenta de Render creada
- [ ] Repositorio conectado en Render
- [ ] Servicio backend creado y desplegado
- [ ] Backend responde en `/health`
- [ ] Servicio frontend creado y desplegado
- [ ] Frontend se conecta al backend
- [ ] CORS configurado correctamente
- [ ] Aplicación funcionando end-to-end

## 🎉 ¡Listo!

Tu aplicación debería estar disponible en:
- **Frontend**: `https://jurismed-frontend.onrender.com`
- **Backend API**: `https://jurismed-backend.onrender.com`
- **Swagger Docs**: `https://jurismed-backend.onrender.com/docs`

## 🔗 Enlaces Útiles

- [Render Dashboard](https://dashboard.render.com)
- [Documentación de Render](https://render.com/docs)
- [Soporte de Render](https://render.com/docs/support)

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o contacta con el soporte de Render.

