"""
Aplicación FastAPI principal para JurisMed AI
Backend de análisis legal-médico con NLP basado en RD 888/2022
"""
from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from typing import Optional
import uvicorn

# Importar modelos
from app.models.schemas import (
    DocumentAnalysisResponse,
    InconsistencyReport
)

# Importar servicios
from app.services.ocr_service import OCRService
from app.services.nlp_service import NLPService
from app.services.legal_engine import LegalEngine
from app.services.report_generator import ReportGenerator

app = FastAPI(
    title="JurisMed AI API",
    description="API para análisis legal-médico basado en RD 888/2022",
    version="1.0.0"
)

# Configurar CORS
# Permitir orígenes desde variables de entorno o valores por defecto
import os
default_origins = "http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173,http://localhost,https://*.vercel.app"
cors_origins_env = os.getenv("CORS_ORIGINS", default_origins)
cors_origins = [origin.strip() for origin in cors_origins_env.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Información de la API"""
    return {
        "name": "JurisMed AI API",
        "version": "1.0.0",
        "description": "API para análisis legal-médico basado en RD 888/2022",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


@app.post("/api/analyze")
async def analyze_document(
    file: UploadFile = File(...),
    document_type: Optional[str] = Form(default=None)
):
    """
    Analiza un documento (PDF, DOC, DOCX)
    
    Args:
        file: Archivo a analizar
        document_type: Tipo de documento (clinical, judicial, administrative)
    
    Returns:
        DocumentAnalysisResponse con el análisis del documento
    """
    try:
        # Leer el contenido del archivo
        file_content = await file.read()
        debug_logs = []
        debug_logs.append(f"Archivo recibido: {file.filename}")
        debug_logs.append(f"Tipo MIME: {file.content_type}")
        debug_logs.append(f"Tamaño: {len(file_content)} bytes")
        
        # 1. Extraer texto usando OCRService
        debug_logs.append("Iniciando extracción de texto...")
        ocr_service = OCRService()
        extracted_text = await ocr_service.extract_text(file_content, file.filename)
        ocr_logs = ocr_service.get_logs()
        debug_logs.extend(ocr_logs)
        debug_logs.append(f"Texto extraído: {len(extracted_text)} caracteres")
        
        if not extracted_text or len(extracted_text.strip()) == 0:
            raise HTTPException(
                status_code=400, 
                detail="No se pudo extraer texto del documento. Verifique que el archivo sea válido."
            )
        
        # 2. Detectar tipo de documento y extraer entidades usando NLPService
        debug_logs.append("Iniciando análisis NLP...")
        nlp_service = NLPService()
        
        # Detectar tipo de documento si no se proporcionó
        if not document_type:
            detected_type = await nlp_service.detect_document_type(extracted_text)
            document_type = detected_type
            debug_logs.append(f"Tipo de documento detectado: {detected_type}")
        else:
            debug_logs.append(f"Tipo de documento proporcionado: {document_type}")
        
        # Extraer entidades
        entities = await nlp_service.extract_entities(extracted_text)
        debug_logs.append(f"Entidades extraídas: {sum(len(v) for v in entities.values())} total")
        
        # 3. Análisis legal usando LegalEngine
        debug_logs.append("Iniciando análisis legal...")
        legal_engine = LegalEngine()
        legal_analysis = await legal_engine.analyze(entities, document_type)
        debug_logs.append("Análisis legal completado")
        debug_logs.append(f"Diagnósticos detectados: {len(legal_analysis.get('detected_diagnoses', []))}")
        if legal_analysis.get('detected_diagnoses'):
            debug_logs.append(f"Lista de diagnósticos: {[d.get('text', str(d)) if isinstance(d, dict) else str(d) for d in legal_analysis.get('detected_diagnoses', [])]}")
        
        # Preparar respuesta
        response_data = {
            "document_type": document_type or "unknown",
            "extracted_text": extracted_text[:5000] if len(extracted_text) > 5000 else extracted_text,  # Limitar para respuesta
            "segments": {},
            "entities": entities,
            "legal_analysis": legal_analysis,
            "filename": file.filename,
            "debug_logs": debug_logs,
            "full_extracted_text": extracted_text,  # Texto completo para depuración
            "full_extracted_text_length": len(extracted_text),
            "downloaded_from_url": None
        }
        
        return JSONResponse(status_code=200, content=response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error al analizar el documento: {str(e)}"
        traceback_str = traceback.format_exc()
        debug_logs.append(f"[ERROR] {error_detail}")
        debug_logs.append(f"[ERROR] Traceback: {traceback_str}")
        # En Vercel, también loguear a stderr para que aparezca en los logs
        print(f"ERROR en /api/analyze: {error_detail}", file=sys.stderr)
        print(f"Traceback: {traceback_str}", file=sys.stderr)
        raise HTTPException(
            status_code=500, 
            detail=f"Error al analizar el documento: {str(e)}. Revisa los logs para más detalles."
        )


@app.post("/api/analyze/inconsistencies")
async def analyze_inconsistencies(analyses: dict):
    """
    Detecta incongruencias entre documentos analizados
    
    Args:
        analyses: Diccionario con los análisis de los documentos
    
    Returns:
        InconsistencyReport con las inconsistencias detectadas
    """
    try:
        # TODO: Implementar detección de inconsistencias real
        # Por ahora, retornamos una respuesta básica
        return JSONResponse(
            status_code=200,
            content={
                "inconsistencies": [],
                "total_count": 0,
                "severity_levels": {
                    "critical": 0,
                    "high": 0,
                    "medium": 0,
                    "low": 0
                }
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar inconsistencias: {str(e)}")


@app.post("/api/generate/report")
async def generate_report(analyses_data: dict):
    """
    Genera un informe legal completo basado en todos los análisis disponibles
    Compara valoraciones entre documentos y destaca discrepancias
    
    Args:
        analyses_data: Diccionario con análisis de clinical, judicial, administrative
    
    Returns:
        Reporte en formato texto con comparación de documentos
    """
    try:
        # Obtener todos los análisis
        clinical_data = analyses_data.get('clinical')
        judicial_data = analyses_data.get('judicial')
        administrative_data = analyses_data.get('administrative')
        
        # Si solo hay un análisis (compatibilidad hacia atrás), procesarlo como antes
        if not clinical_data and not judicial_data and not administrative_data:
            # Formato antiguo: un solo documento
            clinical_data = analyses_data
            judicial_data = None
            administrative_data = None
        
        # Generar informe comparativo
        report_generator = ReportGenerator()
        report = report_generator.generate_comparative_report(
            clinical_data=clinical_data,
            judicial_data=judicial_data,
            administrative_data=administrative_data
        )
        
        return JSONResponse(
            status_code=200,
            content={"report": report}
        )
    except Exception as e:
        import traceback
        raise HTTPException(
            status_code=500, 
            detail=f"Error al generar el reporte: {str(e)}\n{traceback.format_exc()}"
        )


@app.post("/api/generate/inconsistency-report")
async def generate_inconsistency_report(analyses: dict):
    """
    Genera un informe de inconsistencias entre documentos
    
    Args:
        analyses: Diccionario con los análisis de los documentos
    
    Returns:
        Reporte de inconsistencias en formato texto
    """
    try:
        # TODO: Implementar generación de reporte de inconsistencias real
        report = "Informe de Inconsistencias - RD 888/2022\n\n"
        report += "Este es un reporte de ejemplo. La funcionalidad completa será implementada."
        
        return JSONResponse(
            status_code=200,
            content={"report": report}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al generar el reporte de inconsistencias: {str(e)}")


@app.post("/api/download-and-analyze")
async def download_and_analyze(request_data: dict):
    """
    Descarga un documento desde una URL y lo analiza
    
    Args:
        request_data: Diccionario con 'url' y 'document_type'
    
    Returns:
        DocumentAnalysisResponse con el análisis del documento descargado
    """
    try:
        url = request_data.get("url")
        document_type = request_data.get("document_type", "unknown")
        
        if not url:
            raise HTTPException(status_code=400, detail="URL no proporcionada")
        
        # TODO: Implementar descarga y análisis real
        return JSONResponse(
            status_code=200,
            content={
                "document_type": document_type,
                "extracted_text": f"Texto extraído desde {url}",
                "segments": {},
                "entities": {},
                "legal_analysis": {},
                "filename": "documento_descargado.pdf",
                "debug_logs": [f"Descargado desde: {url}"],
                "full_extracted_text": None,
                "full_extracted_text_length": None,
                "downloaded_from_url": url
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al descargar y analizar: {str(e)}")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
