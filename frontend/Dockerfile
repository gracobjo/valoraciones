# Frontend Dockerfile - JurisMed AI
# Multi-stage build para optimizar tamaño

# Stage 1: Build
FROM node:18-alpine AS builder

WORKDIR /app

# Copiar archivos de dependencias
COPY package*.json ./

# Instalar dependencias
RUN npm ci

# Copiar código fuente
COPY . .

# Construir aplicación
RUN npm run build

# Stage 2: Production
FROM nginx:alpine

# Instalar herramientas necesarias
RUN apk add --no-cache gettext

# Copiar archivos construidos
COPY --from=builder /app/dist /usr/share/nginx/html

# Crear directorio para templates
RUN mkdir -p /etc/nginx/templates

# Copiar template de configuración de nginx
COPY nginx.conf.template /etc/nginx/templates/

# Copiar script de entrada
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Exponer puerto
EXPOSE 80

# Usar script de entrada
ENTRYPOINT ["/entrypoint.sh"]

