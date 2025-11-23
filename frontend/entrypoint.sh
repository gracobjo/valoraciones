#!/bin/sh
# Script de entrada para generar nginx.conf dinámicamente

# Obtener URL del backend desde variable de entorno o usar valor por defecto
BACKEND_URL=${BACKEND_URL:-http://backend:8000}

# Asegurar que la URL termine con / si no termina con /
case "$BACKEND_URL" in
  */) ;;
  *) BACKEND_URL="${BACKEND_URL}/" ;;
esac

# Reemplazar placeholder en el template
sed "s|\${BACKEND_URL}|$BACKEND_URL|g" /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Log para debugging
echo "Nginx config generated with BACKEND_URL: $BACKEND_URL"

# Iniciar nginx
exec nginx -g "daemon off;"

