# 🚀 Guía de Despliegue en Vercel

Esta guía te llevará paso a paso para desplegar JurisMed AI en Vercel.

## 📋 Prerequisitos

1. **Cuenta en Vercel**: Regístrate en [vercel.com](https://vercel.com) (puedes usar GitHub para registro)
2. **Repositorio en GitHub**: Tu código debe estar en GitHub (ya lo tienes en https://github.com/gracobjo/valoraciones.git)

## 🔧 Paso 1: Conectar el Repositorio

1. **Iniciar sesión en Vercel**:
   - Ve a https://vercel.com
   - Inicia sesión con tu cuenta de GitHub

2. **Importar Proyecto**:
   - Click en "Add New..." → "Project"
   - Selecciona el repositorio `gracobjo/valoraciones`
   - Click en "Import"

## ⚙️ Paso 2: Configurar el Proyecto

### Configuración del Proyecto:

- **Framework Preset**: Vite
- **Root Directory**: `./frontend` (o dejar vacío si usas la configuración de vercel.json)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Output Directory**: `frontend/dist`
- **Install Command**: `cd frontend && npm install`

### Variables de Entorno (si es necesario):

Por ahora no necesitas variables de entorno, pero puedes agregar:
- `CORS_ORIGINS`: Orígenes permitidos para CORS (opcional)

## 📦 Paso 3: Configuración de la API (Backend)

Vercel detectará automáticamente:
- La carpeta `api/` con funciones serverless
- El archivo `api/index.py` como punto de entrada
- El archivo `api/requirements.txt` para instalar dependencias Python

### Estructura de Archivos:

```
.
├── api/
│   ├── index.py          # Wrapper para FastAPI
│   └── requirements.txt  # Dependencias Python
├── backend/              # Código del backend
├── frontend/             # Código del frontend
└── vercel.json          # Configuración de Vercel
```

## 🚀 Paso 4: Desplegar

1. **Click en "Deploy"**
2. Vercel comenzará a:
   - Instalar dependencias del frontend
   - Construir el frontend
   - Instalar dependencias Python
   - Desplegar las funciones serverless

### ⏱️ Tiempo de Despliegue:

- **Primera vez**: 5-10 minutos (descarga de modelos ML puede tardar)
- **Despliegues siguientes**: 2-3 minutos

## ✅ Paso 5: Verificar el Despliegue

### Frontend:
- Ve a la URL proporcionada por Vercel (ej: `https://valoraciones.vercel.app`)
- Deberías ver la interfaz de la aplicación

### Backend API:
- Ve a `https://tu-proyecto.vercel.app/api/health`
- Deberías ver: `{"status": "healthy"}`
- Ve a `https://tu-proyecto.vercel.app/api/docs`
- Deberías ver la documentación Swagger

## 🔄 Paso 6: Actualizaciones Automáticas

Cada push a la rama `main` en GitHub:
- Vercel detectará automáticamente los cambios
- Iniciará un nuevo despliegue
- Creará una preview URL para cada commit

## 🐛 Solución de Problemas

### Error: "Module not found" o errores de importación

**Causa**: Las rutas de importación no encuentran los módulos  
**Solución**: Verifica que `api/index.py` tenga el path correcto al backend

### Error: "Function timeout"

**Causa**: Las funciones serverless tienen un límite de tiempo (10s en plan gratuito)  
**Solución**: 
- Optimiza el código
- Considera usar el plan Pro para funciones de hasta 60s
- Para análisis largos, considera procesamiento asíncrono

### Error: "Package too large"

**Causa**: Los modelos ML (EasyOCR, spaCy) son muy grandes  
**Solución**:
- Vercel tiene límites de tamaño para funciones serverless
- Considera usar modelos más pequeños
- O usa un servicio externo para el procesamiento pesado

### El frontend no se conecta al backend

**Causa**: Las rutas de la API no están configuradas correctamente  
**Solución**: 
- Verifica que `vercel.json` tenga las rewrites correctas
- Asegúrate de que las llamadas en el frontend usen `/api/...`

## 📊 Monitoreo

### Ver Logs:
1. Ve a tu proyecto en Vercel Dashboard
2. Click en "Functions" → Selecciona la función
3. Verás logs en tiempo real

### Ver Estado:
- Cada deployment muestra su estado:
  - ✅ Ready: Funcionando
  - 🔄 Building: Construyendo
  - ❌ Error: Error

## 🔐 Configuración Adicional

### Dominio Personalizado:
1. Ve a tu proyecto
2. Click en "Settings" → "Domains"
3. Agrega tu dominio
4. Sigue las instrucciones para configurar DNS

### Variables de Entorno:
1. Ve a "Settings" → "Environment Variables"
2. Agrega variables según necesites

## 📝 Notas Importantes

1. **Plan Gratuito**:
   - ✅ 100GB bandwidth/mes
   - ✅ Funciones serverless ilimitadas
   - ⚠️ Límite de 10s por función
   - ⚠️ Límite de 50MB por función

2. **Modelos ML**:
   - Los modelos de EasyOCR y spaCy son grandes
   - Pueden causar problemas en el plan gratuito
   - Considera usar modelos más pequeños o servicios externos

3. **Cold Starts**:
   - La primera llamada después de inactividad puede tardar más
   - Esto es normal en funciones serverless

## ✅ Checklist de Despliegue

- [ ] Repositorio conectado en Vercel
- [ ] Configuración del proyecto correcta
- [ ] Frontend se construye correctamente
- [ ] Backend API responde en `/api/health`
- [ ] Frontend se conecta al backend
- [ ] Aplicación funcionando end-to-end

## 🎉 ¡Listo!

Tu aplicación debería estar disponible en:
- **Frontend + API**: `https://tu-proyecto.vercel.app`
- **API Docs**: `https://tu-proyecto.vercel.app/api/docs`
- **Health Check**: `https://tu-proyecto.vercel.app/api/health`

## 🔗 Enlaces Útiles

- [Vercel Dashboard](https://vercel.com/dashboard)
- [Documentación de Vercel](https://vercel.com/docs)
- [Soporte de Vercel](https://vercel.com/support)

---

**¿Necesitas ayuda?** Abre un issue en el repositorio o contacta con el soporte de Vercel.

