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
# Eliminar cualquier / al final que pueda haber quedado
FINAL_BACKEND_URL=$(echo "$FINAL_BACKEND_URL" | sed 's|/$||')

# Verificar que la URL sea válida
if [ -z "$FINAL_BACKEND_URL" ] || [ "$FINAL_BACKEND_URL" = "http://backend:8000" ]; then
  echo "WARNING: Using default backend URL. This may not work in production!"
fi

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
    # Frontend: /api/analyze -> Backend: /api/analyze
    # IMPORTANTE: Sin / al final en proxy_pass = nginx mantiene la ruta completa
    location /api {
        # Usar la URL directamente en proxy_pass (sin variable para mejor compatibilidad)
        proxy_pass $FINAL_BACKEND_URL;
        
        proxy_http_version 1.1;
        
        # Headers críticos - usar hostname del backend para SSL/TLS
        proxy_set_header Host $BACKEND_HOSTNAME;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto https;
        proxy_set_header X-Forwarded-Host \$host;
        proxy_set_header Connection "";
        
        # Desactivar buffering para archivos grandes
        proxy_buffering off;
        proxy_request_buffering off;
        
        # Timeouts extendidos para OCR (puede tardar varios minutos)
        # En Render Free, el OCR puede tardar 5-10 minutos en documentos grandes
        proxy_connect_timeout 60s;
        proxy_send_timeout 600s;  # 10 minutos para enviar
        proxy_read_timeout 600s;  # 10 minutos para leer respuesta
        
        # SSL verification para HTTPS
        proxy_ssl_server_name on;
        proxy_ssl_verify off;
        
        # No interceptar errores - pasar directamente
        proxy_intercept_errors off;
        
        # Logging detallado
        access_log /var/log/nginx/api_access.log;
        error_log /var/log/nginx/api_error.log warn;
    }

    # Cache estático
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)\$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Log para debugging
echo "=========================================="
echo "NGINX CONFIGURATION DEBUG INFO"
echo "=========================================="
echo "BACKEND_HOST env var: ${BACKEND_HOST:-NOT SET}"
echo "BACKEND_URL env var: ${BACKEND_URL:-NOT SET}"
echo "FINAL_BACKEND_URL: $FINAL_BACKEND_URL"
echo "BACKEND_HOSTNAME: $BACKEND_HOSTNAME"
echo "=========================================="

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

