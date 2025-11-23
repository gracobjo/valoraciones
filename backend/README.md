# JurisMed AI - Backend

Backend de análisis legal-médico con NLP basado en RD 888/2022.

## Instalación

1. Crear entorno virtual:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

3. Descargar modelo spaCy:
```bash
python -m spacy download es_core_news_sm
# O para mejor calidad:
python -m spacy download es_core_news_lg
```

## Ejecución

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

La API estará disponible en: http://localhost:8000

Documentación automática:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Estructura

```
backend/
├── main.py                 # Aplicación FastAPI principal
├── app/
│   ├── services/           # Servicios de negocio
│   │   ├── ocr_service.py  # Extracción de texto de PDFs
│   │   ├── nlp_service.py  # Procesamiento de lenguaje natural
│   │   ├── legal_engine.py # Motor de lógica legal (RD 888/2022)
│   │   └── inconsistency_detector.py  # Detección de incongruencias
│   └── models/
│       └── schemas.py      # Modelos Pydantic
└── requirements.txt
```

## Endpoints

- `GET /` - Información de la API
- `GET /health` - Health check
- `POST /api/analyze/document` - Analiza un documento PDF
- `POST /api/analyze/inconsistencies` - Detecta incongruencias entre documentos
- `POST /api/legal/classify` - Clasifica una deficiencia según RD 888/2022




