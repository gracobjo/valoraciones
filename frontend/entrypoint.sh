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

# Asegurar que la URL termine con / para proxy_pass (requerido por nginx)
case "$FINAL_BACKEND_URL" in
  */) 
    # Ya termina con /, perfecto
    ;;
  *) 
    FINAL_BACKEND_URL="${FINAL_BACKEND_URL}/"
    ;;
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

# Escapar la URL para uso en sed (reemplazar / con \/)
ESCAPED_URL=$(echo "$FINAL_BACKEND_URL" | sed 's|[\/&]|\\&|g')

# Generar archivo de configuración de nginx
cat > /etc/nginx/conf.d/default.conf <<EOF
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip compression
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;

    # SPA routing - todas las rutas van a index.html
    location / {
        try_files \$uri \$uri/ /index.html;
    }

    # Proxy para API
    location /api/ {
        proxy_pass $FINAL_BACKEND_URL;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$proxy_host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;
        proxy_set_header Origin "";
        proxy_redirect off;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # Cache estático
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Log para debugging
echo "Nginx config generated with BACKEND_URL: $FINAL_BACKEND_URL"
echo "Backend host: ${BACKEND_HOST:-not set}"
echo "Backend URL env: ${BACKEND_URL:-not set}"

# Validar que el archivo de configuración se generó correctamente
if [ ! -f /etc/nginx/conf.d/default.conf ]; then
  echo "ERROR: Failed to generate nginx config file"
  exit 1
fi

# Validar sintaxis de nginx
nginx -t
if [ $? -ne 0 ]; then
  echo "ERROR: Nginx configuration syntax error"
  cat /etc/nginx/conf.d/default.conf
  exit 1
fi

echo "Nginx configuration is valid"

# Iniciar nginx
exec nginx -g "daemon off;"

