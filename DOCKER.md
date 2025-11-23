# Guía de Dockerización - JurisMed AI

Esta guía explica cómo construir, ejecutar y desplegar la aplicación JurisMed AI usando Docker.

## 📋 Requisitos Previos

- **Docker** 20.10+ instalado
- **Docker Compose** 2.0+ instalado
- Al menos **4GB de RAM** disponible (para modelos ML)

## 🚀 Inicio Rápido

### Desarrollo Local

1. **Clonar el repositorio**:
```bash
git clone https://github.com/gracobjo/valoraciones.git
cd valoraciones
```

2. **Construir y ejecutar con Docker Compose**:
```bash
docker-compose up --build
```

3. **Acceder a la aplicación**:
   - Frontend: http://localhost
   - Backend API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs

### Producción

```bash
docker-compose -f docker-compose.prod.yml up --build -d
```

## 🏗️ Construcción Manual

### Backend

```bash
cd backend
docker build -t jurismed-backend:latest .
docker run -p 8000:8000 jurismed-backend:latest
```

### Frontend

```bash
cd frontend
docker build -t jurismed-frontend:latest .
docker run -p 80:80 jurismed-frontend:latest
```

## 📦 Publicar en Docker Hub

### 1. Preparar las Imágenes

```bash
# Construir las imágenes
docker-compose build

# Etiquetar las imágenes
docker tag jurismed-backend:latest tu-usuario/jurismed-backend:latest
docker tag jurismed-frontend:latest tu-usuario/jurismed-frontend:latest
```

### 2. Subir a Docker Hub

```bash
# Iniciar sesión en Docker Hub
docker login

# Subir las imágenes
docker push tu-usuario/jurismed-backend:latest
docker push tu-usuario/jurismed-frontend:latest
```

### 3. Usar Imágenes Públicas

Crea un `docker-compose.public.yml`:

```yaml
version: '3.8'

services:
  backend:
    image: tu-usuario/jurismed-backend:latest
    ports:
      - "8000:8000"
    networks:
      - jurismed-network

  frontend:
    image: tu-usuario/jurismed-frontend:latest
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - jurismed-network

networks:
  jurismed-network:
    driver: bridge
```

Luego ejecuta:
```bash
docker-compose -f docker-compose.public.yml up
```

## 🌐 Desplegar en Servicios Gratuitos

### Railway

1. **Instalar Railway CLI**:
```bash
npm i -g @railway/cli
railway login
```

2. **Inicializar proyecto**:
```bash
railway init
```

3. **Desplegar**:
```bash
railway up
```

### Render

1. **Crear cuenta en Render.com**
2. **Nuevo Web Service** desde el repositorio de GitHub
3. **Configuración**:
   - Build Command: `docker-compose build`
   - Start Command: `docker-compose up`
   - Environment: Agregar variables necesarias

### Fly.io

1. **Instalar Fly CLI**:
```bash
curl -L https://fly.io/install.sh | sh
```

2. **Inicializar**:
```bash
fly launch
```

3. **Desplegar**:
```bash
fly deploy
```

### Heroku (con Container Registry)

1. **Instalar Heroku CLI**
2. **Login y crear app**:
```bash
heroku login
heroku create jurismed-ai
heroku container:login
```

3. **Subir y desplegar**:
```bash
heroku container:push web --app jurismed-ai
heroku container:release web --app jurismed-ai
```

## 🔧 Variables de Entorno

### Backend

Puedes configurar variables de entorno creando un archivo `.env` en `backend/`:

```env
CORS_ORIGINS=http://localhost,http://localhost:80
PYTHONUNBUFFERED=1
```

O pasarlas en `docker-compose.yml`:

```yaml
services:
  backend:
    environment:
      - CORS_ORIGINS=http://localhost
      - PYTHONUNBUFFERED=1
```

## 🐛 Solución de Problemas

### El backend no inicia

```bash
# Ver logs
docker-compose logs backend

# Entrar al contenedor
docker-compose exec backend bash

# Verificar que el modelo de spaCy está instalado
python -c "import spacy; spacy.load('es_core_news_sm')"
```

### El frontend no se conecta al backend

1. Verificar que ambos contenedores están en la misma red:
```bash
docker network ls
docker network inspect valoraciones_jurismed-network
```

2. Verificar la configuración de nginx:
```bash
docker-compose exec frontend cat /etc/nginx/conf.d/default.conf
```

### Problemas de memoria

Los modelos ML pueden requerir mucha memoria. Aumenta el límite en Docker Desktop:
- Settings → Resources → Memory → Aumentar a 4GB+

## 📊 Monitoreo

### Ver logs en tiempo real

```bash
docker-compose logs -f
```

### Ver logs de un servicio específico

```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

### Verificar salud de los servicios

```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost
```

## 🔄 Actualizar la Aplicación

```bash
# Detener contenedores
docker-compose down

# Reconstruir imágenes
docker-compose build --no-cache

# Iniciar de nuevo
docker-compose up -d
```

## 📝 Notas Importantes

- **Primera ejecución**: La primera vez puede tardar varios minutos mientras descarga modelos ML
- **Espacio en disco**: Las imágenes Docker pueden ocupar varios GB
- **Puertos**: Asegúrate de que los puertos 80 y 8000 estén libres
- **Producción**: Usa `docker-compose.prod.yml` que no monta volúmenes de código

## 🎯 Próximos Pasos

- Configurar HTTPS con Let's Encrypt
- Agregar base de datos PostgreSQL
- Implementar CI/CD con GitHub Actions
- Configurar monitoreo con Prometheus/Grafana

