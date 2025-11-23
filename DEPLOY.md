# Guía de Despliegue en Servicios Gratuitos

Esta guía te ayudará a desplegar JurisMed AI en diferentes plataformas gratuitas.

## 🚀 Opciones de Despliegue Gratuito

### 1. Railway (Recomendado)

Railway ofrece despliegue automático desde GitHub con Docker.

#### Pasos:

1. **Crear cuenta en Railway**:
   - Visita https://railway.app
   - Inicia sesión con GitHub

2. **Crear nuevo proyecto**:
   - Click en "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Elige tu repositorio `valoraciones`

3. **Configurar servicios**:
   - Railway detectará automáticamente `docker-compose.yml`
   - O puedes configurar manualmente:
     - **Backend Service**: 
       - Dockerfile: `backend/Dockerfile`
       - Port: `8000`
     - **Frontend Service**:
       - Dockerfile: `frontend/Dockerfile`
       - Port: `80`

4. **Variables de entorno**:
   - En el servicio backend, agrega:
     ```
     CORS_ORIGINS=https://tu-app.railway.app
     ```

5. **Desplegar**:
   - Railway desplegará automáticamente en cada push a `main`

**Límites gratuitos**: $5 de crédito mensual

---

### 2. Render

Render ofrece hosting gratuito con Docker.

#### Pasos:

1. **Crear cuenta en Render**:
   - Visita https://render.com
   - Inicia sesión con GitHub

2. **Crear Web Service para Backend**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio
   - Configuración:
     - **Name**: `jurismed-backend`
     - **Environment**: `Docker`
     - **Dockerfile Path**: `backend/Dockerfile`
     - **Docker Context**: `backend`
     - **Port**: `8000`
   - Agregar variables de entorno:
     ```
     CORS_ORIGINS=https://jurismed-frontend.onrender.com
     ```

3. **Crear Web Service para Frontend**:
   - Click en "New +" → "Web Service"
   - Conecta tu repositorio
   - Configuración:
     - **Name**: `jurismed-frontend`
     - **Environment**: `Docker`
     - **Dockerfile Path**: `frontend/Dockerfile`
     - **Docker Context**: `frontend`
     - **Port**: `80`

4. **Alternativa con render.yaml**:
   - Render puede usar `render.yaml` para configurar ambos servicios automáticamente
   - Solo necesitas conectar el repositorio y Render detectará el archivo

**Límites gratuitos**: 
- Servicios se duermen después de 15 minutos de inactividad
- 750 horas/mes gratis

---

### 3. Fly.io

Fly.io ofrece hosting global con Docker.

#### Pasos:

1. **Instalar Fly CLI**:
```bash
# Windows (PowerShell)
iwr https://fly.io/install.ps1 -useb | iex

# Mac/Linux
curl -L https://fly.io/install.sh | sh
```

2. **Login**:
```bash
fly auth login
```

3. **Inicializar aplicación**:
```bash
fly launch
```
- Selecciona "No" para PostgreSQL (por ahora)
- Selecciona región cercana

4. **Desplegar**:
```bash
fly deploy
```

**Límites gratuitos**: 
- 3 VMs compartidas
- 160GB de transferencia/mes

---

### 4. Heroku (Container Registry)

Heroku soporta Docker mediante Container Registry.

#### Pasos:

1. **Instalar Heroku CLI**:
   - Descarga desde https://devcenter.heroku.com/articles/heroku-cli

2. **Login**:
```bash
heroku login
heroku container:login
```

3. **Crear aplicación**:
```bash
heroku create jurismed-ai
```

4. **Configurar variables**:
```bash
heroku config:set CORS_ORIGINS=https://jurismed-ai.herokuapp.com
```

5. **Construir y desplegar backend**:
```bash
cd backend
heroku container:push web --app jurismed-ai
heroku container:release web --app jurismed-ai
```

**Nota**: Heroku requiere apps separadas para frontend y backend.

**Límites gratuitos**: 
- ⚠️ Heroku eliminó su plan gratuito en 2022
- Requiere plan de pago mínimo

---

### 5. GitHub Codespaces (Desarrollo)

Para desarrollo y pruebas, puedes usar GitHub Codespaces.

#### Pasos:

1. **Crear Codespace**:
   - En tu repositorio, click en "Code" → "Codespaces"
   - "Create codespace on main"

2. **En el terminal del Codespace**:
```bash
docker-compose up --build
```

3. **Acceder**:
   - Codespaces expone los puertos automáticamente
   - Haz click en "Ports" para ver las URLs

**Límites gratuitos**: 
- 60 horas/mes para cuentas gratuitas
- 2 cores, 4GB RAM

---

## 🔧 Configuración Recomendada

### Variables de Entorno

Para producción, configura estas variables:

**Backend**:
```env
CORS_ORIGINS=https://tu-frontend-url.com
PYTHONUNBUFFERED=1
```

**Frontend** (si necesitas cambiar la URL del API):
```env
REACT_APP_API_URL=https://tu-backend-url.com
```

### Actualizar nginx.conf para Producción

Si el frontend y backend están en dominios diferentes, actualiza `frontend/nginx.conf`:

```nginx
location /api {
    proxy_pass https://tu-backend-url.com;
    # ... resto de configuración
}
```

## 📊 Comparación de Servicios

| Servicio | Plan Gratuito | Límites | Mejor Para |
|----------|---------------|---------|------------|
| **Railway** | $5 crédito/mes | Generoso | Desarrollo y producción pequeña |
| **Render** | 750h/mes | Se duerme tras 15min | Aplicaciones con poco tráfico |
| **Fly.io** | 3 VMs | 160GB transferencia | Aplicaciones globales |
| **Heroku** | ❌ No disponible | Requiere pago | No recomendado |
| **Codespaces** | 60h/mes | Solo desarrollo | Testing y desarrollo |

## 🎯 Recomendación

Para empezar, **Railway** es la mejor opción:
- ✅ Fácil configuración
- ✅ Despliegue automático desde GitHub
- ✅ Soporte Docker nativo
- ✅ $5 de crédito mensual (suficiente para desarrollo)

## 🐛 Solución de Problemas Comunes

### Error: "Out of memory"

**Solución**: Los modelos ML requieren memoria. En Railway/Render, asegúrate de tener al menos 2GB de RAM asignada.

### Error: "CORS blocked"

**Solución**: Verifica que `CORS_ORIGINS` incluya la URL exacta de tu frontend (con https://).

### Error: "Model not found"

**Solución**: El modelo de spaCy se descarga durante el build. Asegúrate de que el build tenga tiempo suficiente (puede tardar varios minutos).

### Servicios no se comunican

**Solución**: 
- Verifica que ambos servicios estén en la misma red (Docker)
- O configura las URLs completas en las variables de entorno

## 📝 Próximos Pasos

Después del despliegue:

1. ✅ Configurar dominio personalizado
2. ✅ Agregar SSL/HTTPS (automático en la mayoría de servicios)
3. ✅ Configurar monitoreo
4. ✅ Configurar backups (si usas base de datos)

---

¿Necesitas ayuda con algún servicio específico? Abre un issue en el repositorio.

