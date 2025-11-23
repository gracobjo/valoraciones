#!/bin/sh
# Script de entrada para generar nginx.conf dinámicamente

# Construir URL del backend desde variables de entorno
# Si BACKEND_URL está definida, usarla directamente
# Si no, construir desde BACKEND_HOST o usar valor por defecto
if [ -n "$BACKEND_URL" ]; then
  # BACKEND_URL ya está configurada
  FINAL_BACKEND_URL="$BACKEND_URL"
elif [ -n "$BACKEND_HOST" ]; then
  # Construir URL desde BACKEND_HOST (formato: hostname.onrender.com)
  FINAL_BACKEND_URL="https://${BACKEND_HOST}"
else
  # Valor por defecto para desarrollo local
  FINAL_BACKEND_URL="http://backend:8000"
fi

# Asegurar que la URL termine con / si no termina con /
case "$FINAL_BACKEND_URL" in
  */) ;;
  *) FINAL_BACKEND_URL="${FINAL_BACKEND_URL}/" ;;
esac

# Reemplazar placeholder en el template
sed "s|\${BACKEND_URL}|$FINAL_BACKEND_URL|g" /etc/nginx/templates/nginx.conf.template > /etc/nginx/conf.d/default.conf

# Log para debugging
echo "Nginx config generated with BACKEND_URL: $FINAL_BACKEND_URL"

# Iniciar nginx
exec nginx -g "daemon off;"

