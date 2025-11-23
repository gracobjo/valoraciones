# JurisMed AI - Sistema de Análisis Legal-Médico

Sistema inteligente de análisis legal-médico basado en el **Real Decreto 888/2022** para el reconocimiento, declaración y calificación del grado de discapacidad. Utiliza Procesamiento de Lenguaje Natural (NLP) e Inteligencia Artificial para analizar documentos médico-legales, detectar incongruencias y generar informes comparativos detallados.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [Uso de la Aplicación](#-uso-de-la-aplicación)
- [Documentación de la API (Swagger)](#-documentación-de-la-api-swagger)
- [Endpoints Disponibles](#-endpoints-disponibles)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Base Legal](#-base-legal)
- [Contribuciones](#-contribuciones)

## ✨ Características Principales

### 1. **Análisis Multi-Documento**
   - Soporta múltiples tipos de documentos: **Informes médicos/periciales**, **Sentencias judiciales** y **Resoluciones administrativas**
   - Detección automática del tipo de documento mediante análisis de contenido
   - Extracción de texto mediante OCR para documentos escaneados y nativos digitales

### 2. **Extracción Inteligente de Entidades**
   - **Diagnósticos médicos**: Identifica patologías y condiciones médicas con lista blanca extensa (100+ diagnósticos validados)
   - **Métricas funcionales**: Extrae grados de movilidad articular (ROM), balance muscular, porcentajes de pérdida funcional
   - **Códigos médicos**: Detecta códigos CIE-10
   - **Valoraciones existentes**: Identifica porcentajes de discapacidad ya otorgados

### 3. **Motor Legal (RD 888/2022)**
   - **Clasificación automática** de deficiencias según los capítulos del RD 888/2022:
     - Capítulo 2: Visión
     - Capítulo 3: Audición y comunicación
     - Capítulo 4: Sistema cardiovascular
     - Capítulo 5: Sistema respiratorio
     - Capítulo 6: Sistema digestivo
     - Capítulo 7: Sistema endocrino y metabólico
     - Capítulo 8: Sistema musculoesquelético
     - Capítulo 9: Sistema hematológico
     - Capítulo 10: Sistema inmunológico y alergias
     - Capítulo 15: Trastornos mentales
   - **Deduplicación semántica**: Elimina diagnósticos duplicados y variaciones
   - **Agrupación jerárquica**: Agrupa patologías relacionadas (causa-efecto) para evitar doble valoración
   - **Asignación de clases de deficiencia** (0-4) según severidad:
     - Clase 0: Sin deficiencia (0%)
     - Clase 1: Deficiencia leve (5-24%)
     - Clase 2: Deficiencia moderada (25-49%)
     - Clase 3: Deficiencia grave (50-74%)
     - Clase 4: Deficiencia muy grave (75-100%)
   - **Cálculo del BDGP** (Baremo de Deficiencia Global de la Persona) mediante fórmula de combinación

### 4. **Análisis Comparativo y Detección de Discrepancias**
   - **Comparación patología por patología** entre documentos
   - **Tabla comparativa** de lesiones detectadas en cada documento
   - **Análisis de discrepancias globales**: Detecta diferencias en porcentajes y clasificaciones
   - **Detección de omisiones**: Identifica patologías presentes en informes periciales pero no reconocidas en resoluciones administrativas

### 5. **Generación de Informes Legales Completos**
   - **Informe comparativo detallado** con:
     - Análisis individual de cada documento (pericial, judicial, administrativo)
     - Desglose patología por patología con justificación legal
     - Fórmula de combinación paso a paso
     - Tabla comparativa de valoraciones
     - Análisis de discrepancias con recomendaciones específicas
   - **Recomendaciones legales fundamentadas**: Incluye plazos, procedimientos y documentación a aportar
   - **Exportación** de informes en formato texto

### 6. **Interfaz de Usuario Moderna**
   - Diseño responsive con **Tailwind CSS**
   - Carga drag-and-drop de documentos
   - Visualización interactiva de análisis
   - Indicadores de confianza para cada valoración
   - Tooltips explicativos de acrónimos (BDGP, BLA, BRP, BFCA, GDA, VIA, etc.)

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura de **cliente-servidor** con separación clara entre frontend y backend:

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│  - Interfaz de usuario                                       │
│  - Carga de documentos                                       │
│  - Visualización de resultados                               │
│  - Generación y descarga de informes                         │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/REST
┌──────────────────────▼──────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ OCR Service  │  │ NLP Service  │  │Legal Engine  │      │
│  │  - PyMuPDF   │  │  - spaCy     │  │  - RD 888    │      │
│  │  - EasyOCR   │  │  - Regex     │  │  - Clasif.   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │        Report Generator                               │  │
│  │  - Análisis comparativo                               │  │
│  │  - Generación de informes legales                     │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

## 📦 Instalación

### Requisitos Previos

- **Python 3.9+**
- **Node.js 16+** y **npm**
- **Git**

### Backend

1. **Clonar el repositorio**:
```bash
git clone https://github.com/gracobjo/valoraciones.git
cd valoraciones/backend
```

2. **Crear entorno virtual**:
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**:
```bash
pip install -r requirements.txt
```

4. **Descargar modelo de spaCy** (español):
```bash
python -m spacy download es_core_news_sm
# O para mejor calidad (recomendado):
python -m spacy download es_core_news_lg
```

### Frontend

1. **Navegar al directorio frontend**:
```bash
cd ../frontend
```

2. **Instalar dependencias**:
```bash
npm install
```

## ⚙️ Configuración

### Backend

El servidor se ejecuta por defecto en `http://localhost:8000`. Puedes modificar el puerto editando `backend/run.py` o ejecutando directamente:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

El frontend se ejecuta en `http://localhost:3000` (o `http://localhost:5173` según la configuración de Vite). El proxy está configurado para comunicarse con el backend en `http://localhost:8000`.

## 🚀 Uso de la Aplicación

### Inicio Rápido

1. **Iniciar el backend**:
```bash
cd backend
python run.py
# O alternativamente:
uvicorn main:app --reload
```

2. **Iniciar el frontend** (en otra terminal):
```bash
cd frontend
npm run dev
```

3. **Abrir el navegador** en `http://localhost:3000`

### Flujo de Trabajo

1. **Carga de Documentos**:
   - Haz clic en "Seleccionar Archivo" para cada tipo de documento:
     - **Informe Médico/Pericial**: Documento médico con diagnósticos
     - **Sentencia Judicial**: Sentencia que reconoce valoraciones
     - **Resolución Administrativa**: Resolución previa sobre discapacidad
   - El sistema analiza automáticamente cada documento cargado

2. **Revisión de Análisis**:
   - Visualiza los diagnósticos detectados
   - Revisa las valoraciones asignadas (clase y porcentaje)
   - Consulta la confianza del análisis

3. **Generación de Informe Legal**:
   - Haz clic en "Generar Informe Legal Completo"
   - El sistema genera un informe comparativo detallado que incluye:
     - Análisis de cada documento
     - Comparación patología por patología
     - Discrepancias detectadas
     - Recomendaciones legales específicas
   - Descarga el informe en formato texto

## 📚 Documentación de la API (Swagger)

FastAPI genera automáticamente documentación interactiva usando **Swagger UI** y **ReDoc**.

### Acceso a la Documentación

Una vez iniciado el servidor backend, accede a:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Uso de Swagger UI

1. **Abrir Swagger UI**: Navega a `http://localhost:8000/docs`

2. **Explorar Endpoints**:
   - Cada endpoint está agrupado por funcionalidad
   - Haz clic en cualquier endpoint para ver detalles

3. **Probar Endpoints**:
   - Haz clic en "Try it out" en cualquier endpoint
   - Rellena los parámetros requeridos
   - Para endpoints con archivos (`/api/analyze`):
     - Haz clic en "Choose File"
     - Selecciona un PDF, DOC o DOCX
     - Opcionalmente, especifica el tipo de documento
     - Haz clic en "Execute"

4. **Ver Respuestas**:
   - La respuesta aparecerá con código de estado HTTP
   - Puedes ver el esquema de respuesta expandido
   - Ejemplos de respuesta están disponibles

5. **Modelos de Datos**:
   - Haz scroll hacia abajo para ver los esquemas de datos (models)
   - Cada modelo muestra su estructura y tipos de datos

### Ejemplo de Uso desde Swagger

#### Analizar un Documento

1. Abre `/docs` en tu navegador
2. Encuentra `POST /api/analyze`
3. Haz clic en "Try it out"
4. Haz clic en "Choose File" y selecciona un PDF médico
5. Opcionalmente, en `document_type`, escribe: `clinical`, `judicial` o `administrative`
6. Haz clic en "Execute"
7. Revisa la respuesta JSON con:
   - Diagnósticos detectados
   - Valoraciones asignadas
   - Análisis legal completo

#### Generar Informe Comparativo

1. Encuentra `POST /api/generate/report`
2. Haz clic en "Try it out"
3. En el campo "Request body", proporciona un JSON con los análisis:
```json
{
  "clinical": { /* análisis del informe pericial */ },
  "judicial": { /* análisis de la sentencia */ },
  "administrative": { /* análisis de la resolución */ }
}
```
4. Haz clic en "Execute"
5. Recibe el informe completo en formato texto

## 🔌 Endpoints Disponibles

### Endpoints Principales

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Información de la API |
| `GET` | `/health` | Health check del servidor |
| `GET` | `/docs` | Documentación Swagger UI |
| `GET` | `/redoc` | Documentación ReDoc |
| `POST` | `/api/analyze` | Analiza un documento (PDF, DOC, DOCX) |
| `POST` | `/api/generate/report` | Genera informe legal comparativo completo |
| `POST` | `/api/generate/inconsistency-report` | Genera informe de inconsistencias |
| `POST` | `/api/analyze/inconsistencies` | Detecta inconsistencias entre documentos |
| `POST` | `/api/download-and-analyze` | Descarga y analiza documento desde URL |

### Detalles de Endpoints

#### `POST /api/analyze`

Analiza un documento y extrae diagnósticos, métricas y valoraciones.

**Parámetros**:
- `file` (FormData, requerido): Archivo PDF, DOC o DOCX
- `document_type` (string, opcional): `clinical`, `judicial`, o `administrative`

**Respuesta**:
```json
{
  "document_type": "clinical",
  "filename": "informe.pdf",
  "entities": {
    "DIAGNOSIS": [...],
    "METRIC": [...],
    "CODE": [...],
    "RATING": [...]
  },
  "legal_analysis": {
    "detected_diagnoses": [...],
    "chapter_valuations": [...],
    "final_valuation": {
      "bdgp_percentage": 75.0,
      "final_class": "4",
      "formula": "..."
    }
  }
}
```

#### `POST /api/generate/report`

Genera un informe legal comparativo detallado.

**Body** (JSON):
```json
{
  "clinical": { /* análisis del informe pericial */ },
  "judicial": { /* análisis de la sentencia */ },
  "administrative": { /* análisis de la resolución */ }
}
```

**Respuesta**:
```json
{
  "report": "INFORME LEGAL COMPLETO - RD 888/2022\n\n..."
}
```

## 📁 Estructura del Proyecto

```
valoraciones/
├── backend/
│   ├── app/
│   │   ├── models/
│   │   │   └── schemas.py          # Modelos Pydantic
│   │   └── services/
│   │       ├── ocr_service.py      # Extracción de texto (OCR)
│   │       ├── nlp_service.py      # Procesamiento NLP
│   │       ├── legal_engine.py     # Motor legal RD 888/2022
│   │       ├── report_generator.py # Generador de informes
│   │       └── inconsistency_detector.py
│   ├── docs/                       # Documentación adicional
│   ├── main.py                     # Aplicación FastAPI principal
│   ├── run.py                      # Script de inicio
│   └── requirements.txt            # Dependencias Python
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── DocumentUpload.jsx  # Componente de carga
│   │   ├── App.jsx                 # Componente principal
│   │   ├── main.jsx                # Punto de entrada
│   │   └── index.css               # Estilos globales
│   ├── package.json
│   └── vite.config.js              # Configuración Vite
│
└── README.md                        # Este archivo
```

## 🛠️ Tecnologías Utilizadas

### Backend

- **FastAPI**: Framework web moderno y rápido
- **PyMuPDF (fitz)**: Extracción de texto de PDFs nativos
- **EasyOCR**: OCR para documentos escaneados
- **python-docx**: Lectura de documentos Word
- **spaCy**: Procesamiento de lenguaje natural
- **Transformers (BERT)**: Modelos de lenguaje para NLP
- **Pydantic**: Validación de datos y modelos

### Frontend

- **React 18**: Biblioteca de UI
- **Vite**: Build tool y dev server
- **Tailwind CSS**: Framework de estilos
- **Lucide React**: Iconos modernos
- **Axios**: Cliente HTTP

## ⚖️ Base Legal

Este sistema está basado en:

- **Real Decreto 888/2022**, de 18 de octubre, por el que se establece el procedimiento para el reconocimiento, declaración y calificación del grado de discapacidad.

El sistema implementa los baremos y criterios establecidos en:
- **Anexo III**: Baremo de Deficiencia Global de la Persona (BDGP)
- **Anexo IV**: Baremo de Limitaciones en la Actividad (BLA)
- **Anexo V**: Baremo de Restricciones en la Participación (BRP)
- **Anexo VI**: Baremo de Factores Contextuales y Barreras Ambientales (BFCA)

## 📝 Notas Importantes

- **Precisión del Análisis**: Los resultados generados son estimaciones basadas en análisis automático y deben ser revisados por profesionales médico-legales calificados.
- **Confianza**: Cada valoración incluye un nivel de confianza que refleja la certeza del análisis.
- **Uso Legal**: Este sistema es una herramienta de apoyo y no sustituye el juicio profesional en procedimientos legales.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es de código abierto. Ver archivo `LICENSE` para más detalles.

## 👥 Autor

Proyecto desarrollado para análisis legal-médico basado en RD 888/2022.

---

**JurisMed AI** - Sistema de Análisis Legal-Médico basado en RD 888/2022
