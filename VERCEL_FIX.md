# Solución al Error 404 en Vercel

## Problema
Error 404 NOT_FOUND al acceder a la aplicación desplegada en Vercel.

## Solución

### Opción 1: Configurar Root Directory en Vercel Dashboard (Recomendado)

1. Ve a tu proyecto en Vercel: https://vercel.com/gracobjos-projects/valoraciones
2. Ve a **Settings** → **General**
3. En la sección **Root Directory**, deja vacío (o pon `.`)
4. En **Build & Development Settings**:
   - **Framework Preset**: Vite
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Output Directory**: `frontend/dist`
   - **Install Command**: `cd frontend && npm install`
5. Guarda los cambios
6. Haz un nuevo deploy

### Opción 2: Verificar que el Frontend se Construya

El problema puede ser que el frontend no se está construyendo. Verifica en los logs de build que aparezca:
- `Running "cd frontend && npm install && npm run build"`
- `Building for production...`
- `dist/` directory created

### Opción 3: Verificar Rutas

Si el frontend se construye pero sigue dando 404, verifica:
1. Que `frontend/dist/index.html` existe después del build
2. Que las rutas en `vercel.json` estén correctas
3. Que la función serverless en `api/index.py` esté accesible

## Verificación

Después de aplicar los cambios, verifica:
- Frontend: `https://tu-proyecto.vercel.app/`
- API Health: `https://tu-proyecto.vercel.app/api/health`
- API Docs: `https://tu-proyecto.vercel.app/api/docs`

