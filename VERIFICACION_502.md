# 🔍 Verificación Paso a Paso: Error 502

Sigue estos pasos **en orden** para diagnosticar y resolver el error 502.

## ✅ Paso 1: Verificar que el Backend Funcione

**Abre en tu navegador:**
```
https://jurismed-backend.onrender.com/health
```

**Reemplaza `jurismed-backend` con el nombre REAL de tu servicio backend en Render.**

### Resultados posibles:

#### ✅ **Caso 1: Responde `{"status": "healthy"}`**
- El backend funciona correctamente
- Continúa al Paso 2

#### ⏳ **Caso 2: Tarda mucho o no responde (30-60 segundos)**
- El backend está **dormido** (plan gratuito de Render)
- Espera 30-60 segundos y recarga la página
- Una vez que responda, continúa al Paso 2

#### ❌ **Caso 3: Error 404, 500, o cualquier otro error**
- Hay un problema con el backend
- Ve a Render Dashboard → Backend Service → Logs
- Revisa los errores y corrígelos primero

---

## ✅ Paso 2: Verificar Variables de Entorno del Frontend

**En Render Dashboard:**
1. Ve a **jurismed-frontend** → **Environment** (Variables de entorno)
2. Busca una variable llamada `BACKEND_URL` o `BACKEND_HOST`

### ¿Qué deberías ver?

#### ✅ **Si existe `BACKEND_URL`:**
- Valor debe ser: `https://jurismed-backend.onrender.com`
- **IMPORTANTE**: Sin `/` al final
- Reemplaza `jurismed-backend` con tu nombre real

#### ✅ **Si existe `BACKEND_HOST`:**
- Valor debe ser: `jurismed-backend.onrender.com`
- El script construirá la URL automáticamente

#### ❌ **Si NO existe ninguna:**
- **Agregar manualmente:**
  1. Click en **"Add Environment Variable"**
  2. Key: `BACKEND_URL`
  3. Value: `https://jurismed-backend.onrender.com` (tu URL real)
  4. Guardar

---

## ✅ Paso 3: Verificar Logs del Frontend

**En Render Dashboard:**
1. Ve a **jurismed-frontend** → **Logs**
2. Busca estas líneas al inicio:

```
==========================================
NGINX CONFIGURATION DEBUG INFO
==========================================
BACKEND_URL env var: https://jurismed-backend.onrender.com
FINAL_BACKEND_URL: https://jurismed-backend.onrender.com
BACKEND_HOSTNAME: jurismed-backend.onrender.com
==========================================
```

### Verificaciones:

- ✅ La URL debe ser `https://...` (no `http://`)
- ✅ No debe tener `/` al final
- ✅ Debe ser la URL correcta de tu backend

### Si la URL está mal:

1. Ve a **Environment** del frontend
2. Corrige o agrega `BACKEND_URL`
3. Guarda y espera el redespliegue

---

## ✅ Paso 4: Verificar que Ambos Servicios Estén "Live"

**En Render Dashboard:**
- Ambos servicios (backend y frontend) deben estar en estado **🟢 Live**
- Si alguno está en otro estado (amarillo, rojo), haz clic en **Manual Deploy**

---

## ✅ Paso 5: Probar Nuevamente

Una vez completados los pasos anteriores:

1. Espera 2-3 minutos para que el frontend se redespliegue
2. Intenta subir un documento de nuevo
3. Si sigue fallando, revisa los logs del frontend para errores específicos

---

## 🔧 Solución Rápida: Configurar BACKEND_URL Manualmente

Si quieres hacerlo rápidamente:

1. **Render Dashboard** → **jurismed-frontend** → **Environment**
2. **Agregar Variable:**
   - **Key**: `BACKEND_URL`
   - **Value**: `https://tu-backend.onrender.com`
   (reemplaza `tu-backend` con el nombre real)
3. **Guardar**
4. Esperar 2-3 minutos
5. Probar de nuevo

---

## 📊 Verificar Logs de Errores

**Si después de todo sigue fallando:**

1. **Logs del Frontend** (Render Dashboard):
   - Busca líneas con `502`, `Bad Gateway`, `upstream`, `connect failed`
   - Copia el mensaje de error completo

2. **Logs del Backend** (Render Dashboard):
   - Busca errores de Python, import errors, etc.
   - Asegúrate de que el backend esté iniciando correctamente

---

## ⚠️ Problemas Comunes

| Problema | Causa | Solución |
|----------|-------|----------|
| Backend no responde | Está dormido | Esperar 30-60s y recargar `/health` |
| URL incorrecta | BACKEND_URL mal configurada | Configurar manualmente en Environment |
| Backend con errores | Error en código | Revisar logs del backend |
| Frontend no se redespliega | Cambios no detectados | Manual Deploy con "Clear cache" |

---

## 🆘 ¿Necesitas Ayuda?

Si después de seguir todos los pasos el problema persiste:

1. Verifica que el backend responda en `/health`
2. Verifica que `BACKEND_URL` esté configurada correctamente
3. Copia los logs del frontend (especialmente las líneas de configuración)
4. Copia cualquier error específico que veas

