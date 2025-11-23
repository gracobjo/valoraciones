"""
Esquemas Pydantic para validación de datos
"""
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any


class Entity(BaseModel):
    """Entidad extraída del texto"""
    text: str
    start: Optional[int] = None
    end: Optional[int] = None
    value: Optional[Any] = None
    type: Optional[str] = None


class EntitiesDict(BaseModel):
    """Diccionario de entidades por tipo"""
    DIAGNOSIS: List[Entity] = []
    METRIC: List[Entity] = []
    CODE: List[Entity] = []
    RATING: List[Entity] = []


class LegalAnalysis(BaseModel):
    """Análisis legal aplicado"""
    detected_diagnoses: List[Dict] = []
    detected_metrics: Dict[str, float] = {}
    suggested_classification: Optional[Dict] = None
    confidence: float = 0.0
    legal_basis: str = "RD 888/2022"


class DocumentAnalysisResponse(BaseModel):
    """Respuesta del análisis de documento"""
    document_type: str
    extracted_text: str
    segments: Dict[str, str] = {}
    entities: Dict[str, List[Dict]] = {}
    legal_analysis: Dict[str, Any] = {}
    filename: Optional[str] = None
    debug_logs: Optional[List[str]] = []  # Logs de depuración
    full_extracted_text_length: Optional[int] = None  # Longitud completa del texto extraído
    full_extracted_text: Optional[str] = None  # Texto completo para depuración
    downloaded_from_url: Optional[str] = None  # URL desde la que se descargó el documento
    
    class Config:
        arbitrary_types_allowed = True


class DocumentAnalysisRequest(BaseModel):
    """Request para análisis de documento"""
    document_type: Optional[str] = None
    filename: Optional[str] = None


class Inconsistency(BaseModel):
    """Inconsistencia detectada entre documentos"""
    type: str
    severity: str  # "critical", "high", "medium", "low"
    description: str
    source_document: str
    target_document: str
    recommendation: str


class InconsistencyReport(BaseModel):
    """Reporte de incongruencias"""
    inconsistencies: List[Inconsistency]
    total_count: int
    severity_levels: Dict[str, int]


class ClassificationRequest(BaseModel):
    """Request para clasificación de deficiencia"""
    diagnosis: str
    metrics: Dict[str, float]
    body_part: str = "hombro"


class ClassificationResponse(BaseModel):
    """Respuesta de clasificación"""
    class_name: str = Field(alias="class")
    class_number: str
    description: str
    percentage_range: List[int]
    suggested_percentage: Optional[float] = None
    confidence: float
    legal_basis: str
    criteria_met: List[str] = []
    
    class Config:
        populate_by_name = True

