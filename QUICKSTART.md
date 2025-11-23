# Guía de Inicio Rápido - JurisMed AI

## Requisitos Previos

- Python 3.9 o superior
- Node.js 16 o superior
- npm o yarn

## Instalación Rápida

### 1. Backend

```bash
cd backend

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Descargar modelo spaCy
python -m spacy download es_core_news_sm
```

### 2. Frontend

```bash
cd frontend

# Instalar dependencias
npm install
```

## Ejecución

### ⚠️ IMPORTANTE: Debes arrancar AMBOS servicios

### Terminal 1 - Backend (OBLIGATORIO)

```bash
cd backend
python run.py
```

**O alternativamente:**
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Verificación:**
- Deberías ver: `INFO: Uvicorn running on http://0.0.0.0:8000`
- Abre en el navegador: http://localhost:8000/docs (debe cargar la documentación)

El backend estará disponible en: http://localhost:8000
Documentación API: http://localhost:8000/docs

### Terminal 2 - Frontend

```bash
cd frontend
npm run dev
```

**Verificación:**
- Deberías ver: `Local: http://localhost:3000/`

El frontend estará disponible en: http://localhost:3000

### ⚠️ Si ves "Error de conexión"

**El backend NO está ejecutándose.** Debes:
1. Abrir una terminal
2. Ir a la carpeta `backend`
3. Ejecutar `python run.py`
4. Esperar a ver el mensaje "Uvicorn running"
5. Luego intentar cargar el documento de nuevo

## Uso Básico

1. Abre el navegador en http://localhost:3000
2. Carga un documento PDF (informe clínico, sentencia o resolución)
3. Espera a que se complete el análisis
4. Si has cargado múltiples documentos, haz clic en "Verificar Incongruencias"
5. Revisa los resultados y las alertas detectadas

## Ejemplo de Uso de la API

### Analizar un documento

```bash
curl -X POST "http://localhost:8000/api/analyze/document" \
  -F "file=@documento.pdf" \
  -F "document_type=clinical"
```

### Clasificar una deficiencia

```bash
curl -X POST "http://localhost:8000/api/legal/classify" \
  -H "Content-Type: application/json" \
  -d '{
    "diagnosis": "Rotura manguito rotador hombro derecho",
    "metrics": {
      "abduccion": 75,
      "flexion": 80,
      "rotacion": 20
    },
    "body_part": "hombro"
  }'
```

## Solución de Problemas

### Error: "Modelo spaCy no encontrado"
```bash
python -m spacy download es_core_news_sm
```

### Error: "No se puede conectar al backend"
- Verifica que el backend esté ejecutándose en el puerto 8000
- Revisa la configuración de CORS en `backend/main.py`

### Error al instalar EasyOCR
EasyOCR requiere dependencias del sistema. En Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install libgl1-mesa-glx libglib2.0-0
```

## Notas Importantes

- El primer análisis puede tardar más tiempo debido a la carga de modelos
- Los modelos BERT se descargan automáticamente la primera vez
- Para producción, considera usar modelos más ligeros o servicios externos

