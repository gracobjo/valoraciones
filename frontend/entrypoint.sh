#!/bin/sh
# Script de entrada para generar nginx.conf dinámicamente

# Obtener URL del backend desde variable de entorno o usar valor por defecto
BACKEND_URL=${BACKEND_URL:-http://backend:8000}

# Si es una URL de Render (contiene .onrender.com), asegurar que termine con /
if echo "$BACKEND_URL" | grep -q "\.onrender\.com"; then
  BACKEND_URL="${BACKEND_URL%/}/"
fi

# Reemplazar placeholder en el template
sed "s|\${BACKEND_URL}|$BACKEND_URL|g" /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Iniciar nginx
exec nginx -g "daemon off;"

