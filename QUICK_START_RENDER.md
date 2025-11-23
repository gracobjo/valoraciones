# ⚡ Inicio Rápido: Desplegar en Render en 5 Minutos

## 🚀 Pasos Rápidos

### 1. Crear Cuenta
- Ve a https://render.com
- Click en "Get Started for Free"
- Inicia sesión con GitHub

### 2. Conectar Repositorio
1. En Render Dashboard, click en **"New +"**
2. Selecciona **"Blueprint"**
3. Conecta tu repositorio: `gracobjo/valoraciones`
4. Click en **"Apply"**

### 3. Render Automáticamente:
- ✅ Creará el servicio backend
- ✅ Creará el servicio frontend  
- ✅ Configurará las variables de entorno
- ✅ Iniciará el despliegue

### 4. Esperar (10-15 minutos primera vez)
- Render construirá las imágenes Docker
- Descargará modelos ML
- Desplegará los servicios

### 5. ¡Listo!
- **Frontend**: `https://jurismed-frontend.onrender.com`
- **Backend**: `https://jurismed-backend.onrender.com/docs`

## 📝 Nota Importante

Si los nombres de tus servicios son diferentes, actualiza la variable de entorno `CORS_ORIGINS` en el backend con la URL de tu frontend.

## ❓ ¿Problemas?

Consulta la guía completa: [RENDER_DEPLOY.md](RENDER_DEPLOY.md)

