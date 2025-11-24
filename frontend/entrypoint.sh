#!/bin/sh
# Script de entrada para generar nginx.conf dinámicamente

# Construir URL del backend desde variables de entorno
if [ -n "$BACKEND_URL" ]; then
  # BACKEND_URL ya está configurada completamente
  FINAL_BACKEND_URL="$BACKEND_URL"
elif [ -n "$BACKEND_HOST" ]; then
  # Construir URL desde BACKEND_HOST
  # Si BACKEND_HOST ya incluye el dominio completo, usarlo
  # Si no, asumir que es un servicio de Render y agregar .onrender.com
  case "$BACKEND_HOST" in
    *.*)
      # Ya tiene dominio completo
      FINAL_BACKEND_URL="https://${BACKEND_HOST}"
      ;;
    *)
      # Solo tiene el nombre del servicio, construir URL de Render
      FINAL_BACKEND_URL="https://${BACKEND_HOST}.onrender.com"
      ;;
  esac
else
  # Valor por defecto para desarrollo local (Docker Compose)
  FINAL_BACKEND_URL="http://backend:8000"
fi

# Asegurar que la URL termine con / para proxy_pass
case "$FINAL_BACKEND_URL" in
  */) ;;
  *) FINAL_BACKEND_URL="${FINAL_BACKEND_URL}/" ;;
esac

# Validar que la URL tenga esquema (http:// o https://)
case "$FINAL_BACKEND_URL" in
  http://*|https://*)
    # URL válida con esquema
    ;;
  *)
    # Falta esquema, agregar https:// por defecto
    FINAL_BACKEND_URL="https://${FINAL_BACKEND_URL}"
    ;;
esac

# Reemplazar placeholder en el template
sed "s|\${BACKEND_URL}|$FINAL_BACKEND_URL|g" /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Log para debugging
echo "Nginx config generated with BACKEND_URL: $FINAL_BACKEND_URL"
echo "Backend host: ${BACKEND_HOST:-not set}"
echo "Backend URL env: ${BACKEND_URL:-not set}"

# Validar que el archivo de configuración se generó correctamente
if [ ! -f /etc/nginx/conf.d/default.conf ]; then
  echo "ERROR: Failed to generate nginx config file"
  exit 1
fi

# Mostrar configuración generada (primeras líneas)
echo "Generated nginx config (first 10 lines):"
head -10 /etc/nginx/conf.d/default.conf

# Iniciar nginx
exec nginx -g "daemon off;"

