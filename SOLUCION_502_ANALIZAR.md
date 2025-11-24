# Solución Error 502 al Analizar Documentos

## Problema
Error 502 (Bad Gateway) al intentar analizar documentos en `https://jurismed-frontend.onrender.com/`

## Causas Posibles

### 1. Backend Dormido (Plan Gratuito de Render)
El plan gratuito de Render pone los servicios a dormir después de 15 minutos de inactividad. El primer request puede tardar 30-60 segundos en despertar el servicio.

**Solución**: Esperar 30-60 segundos después del primer intento y volver a intentar.

### 2. Backend No Responde
El backend puede estar caído o no estar funcionando correctamente.

**Verificación**:
1. Abre en el navegador: `https://jurismed-backend.onrender.com/health`
2. Debería responder con: `{"status": "healthy"}`
3. Si no responde, el backend está caído y necesita ser reiniciado desde el Dashboard de Render

### 3. Variable de Entorno BACKEND_URL Incorrecta
La variable de entorno `BACKEND_URL` en el servicio frontend puede estar mal configurada.

**Verificación en Render Dashboard**:
1. Ve a `jurismed-frontend` service
2. Ve a "Environment" tab
3. Verifica que `BACKEND_URL` = `https://jurismed-backend.onrender.com`
4. Si no está o está mal, añádela/corrígela y reinicia el servicio

### 4. Problema con Nginx Proxy
El proxy de Nginx puede tener problemas de configuración.

**Verificación**:
1. Ve a los logs del servicio `jurismed-frontend` en Render
2. Busca errores en `/var/log/nginx/api_error.log`
3. Verifica que la configuración muestre:
   ```
   FINAL_BACKEND_URL: https://jurismed-backend.onrender.com
   BACKEND_HOSTNAME: jurismed-backend.onrender.com
   ```

## Soluciones Implementadas

### Mejoras en entrypoint.sh
- Mejor manejo de errores con `proxy_next_upstream`
- Verificación de conectividad con el backend al iniciar
- Logging mejorado para debugging
- Configuración SSL mejorada

### Pasos para Resolver

1. **Verificar Backend**:
   ```bash
   curl https://jurismed-backend.onrender.com/health
   ```
   Debe responder: `{"status": "healthy"}`

2. **Verificar Variables de Entorno**:
   - En Render Dashboard → `jurismed-frontend` → Environment
   - Debe existir: `BACKEND_URL=https://jurismed-backend.onrender.com`

3. **Reiniciar Servicios**:
   - En Render Dashboard, reinicia ambos servicios:
     - `jurismed-backend`
     - `jurismed-frontend`

4. **Verificar Logs**:
   - Revisa los logs del frontend para ver si hay errores de conexión
   - Revisa los logs del backend para ver si está recibiendo requests

5. **Esperar Despertar**:
   - Si el backend está dormido, el primer request puede tardar 30-60 segundos
   - Intenta de nuevo después de esperar

## Debugging Adicional

Si el problema persiste:

1. **Verificar que el backend esté despierto**:
   - Haz una petición manual a: `https://jurismed-backend.onrender.com/health`
   - Espera la respuesta antes de intentar analizar documentos

2. **Verificar logs del frontend**:
   - En Render Dashboard → `jurismed-frontend` → Logs
   - Busca mensajes de error relacionados con `proxy_pass` o `502`

3. **Verificar logs del backend**:
   - En Render Dashboard → `jurismed-backend` → Logs
   - Verifica que esté recibiendo requests del frontend

4. **Probar directamente el backend**:
   ```bash
   curl -X POST https://jurismed-backend.onrender.com/api/analyze \
     -F "file=@test.pdf" \
     -F "document_type=clinical"
   ```

## Nota sobre Plan Gratuito

El plan gratuito de Render tiene limitaciones:
- Los servicios se duermen después de 15 minutos de inactividad
- El primer request puede tardar 30-60 segundos en despertar el servicio
- Timeout máximo de ~10 minutos para peticiones

Si necesitas mejor rendimiento, considera actualizar al plan Starter ($7/mes).

