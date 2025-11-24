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

# Asegurar que la URL NO termine con / al final
# Cuando proxy_pass NO termina con /, nginx pasa la ruta completa después del rewrite
# Si termina con /, nginx reescribe y quita parte del path
# Eliminar cualquier / al final que pueda haber quedado
FINAL_BACKEND_URL=$(echo "$FINAL_BACKEND_URL" | sed 's|/$||')

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

# Extraer solo el hostname de la URL para proxy_set_header Host
# Esto es necesario porque nginx necesita el hostname correcto
BACKEND_HOSTNAME=$(echo "$FINAL_BACKEND_URL" | sed -E 's|https?://([^/]+).*|\1|')

# Generar archivo de configuración de nginx
cat > /etc/nginx/conf.d/default.conf <<EOF
server {
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;
    
    # Tamaño máximo de archivo a subir
    client_max_body_size 10M;

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
    # El frontend envía /api/analyze, y el backend espera /api/analyze
    # Usamos rewrite para mantener la ruta completa al backend
    location /api {
        # Reescribir para mantener /api en el path
        rewrite ^/api(.*) /api\$1 break;
        
        # URL del backend SIN / al final para mantener la ruta completa
        proxy_pass $FINAL_BACKEND_URL;
        
        proxy_http_version 1.1;
        
        # Headers importantes - usar hostname del backend para SSL
        proxy_set_header Host $BACKEND_HOSTNAME;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header Origin "";
        
        # Desactivar buffering para streams de archivos grandes
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Timeouts extendidos (5 minutos) para procesamiento de documentos
        proxy_connect_timeout 300s;
        proxy_send_timeout 300s;
        proxy_read_timeout 300s;
        
        # Manejo de errores del backend
        proxy_next_upstream error timeout invalid_header http_500 http_502 http_503 http_504;
        
        # Headers CORS adicionales
        add_header Access-Control-Allow-Origin * always;
        add_header Access-Control-Allow-Methods "GET, POST, PUT, DELETE, OPTIONS" always;
        add_header Access-Control-Allow-Headers "Content-Type, Authorization" always;
        
        # Logging para debugging
        access_log /var/log/nginx/api_access.log;
        error_log /var/log/nginx/api_error.log;
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
echo "Backend hostname extracted: $BACKEND_HOSTNAME"
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

