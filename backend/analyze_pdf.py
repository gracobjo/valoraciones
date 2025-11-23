"""Script para analizar un PDF y mostrar las entidades extraídas"""
import asyncio
import sys
from pathlib import Path

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from app.services.ocr_service import OCRService
from app.services.nlp_service import NLPService
from app.services.legal_engine import LegalEngine

async def analyze_pdf(pdf_path: str):
    """Analiza un PDF y muestra las entidades extraídas"""
    
    print("=" * 80)
    print(f"ANÁLISIS DEL PDF: {pdf_path}")
    print("=" * 80)
    print()
    
    # Leer el archivo PDF
    print("1. Extrayendo texto del PDF...")
    ocr_service = OCRService()
    
    try:
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        extracted_text = await ocr_service.extract_text(pdf_content, pdf_path)
        print(f"   [OK] Texto extraido: {len(extracted_text)} caracteres")
        print()
    except Exception as e:
        print(f"   [ERROR] Error al leer el PDF: {e}")
        return
    
    # Detectar tipo de documento
    print("2. Detectando tipo de documento...")
    nlp_service = NLPService()
    doc_type = await nlp_service.detect_document_type(extracted_text)
    print(f"   [OK] Tipo detectado: {doc_type}")
    print()
    
    # Extraer entidades
    print("3. Extrayendo entidades...")
    entities = await nlp_service.extract_entities(extracted_text)
    print(f"   [OK] Entidades extraidas")
    print()
    
    # Mostrar entidades
    print("=" * 80)
    print("ENTIDADES EXTRAÍDAS")
    print("=" * 80)
    print()
    
    # DIAGNOSIS
    diagnoses = entities.get("DIAGNOSIS", [])
    print(f"[DIAGNOSTICOS] ({len(diagnoses)} encontrados):")
    print("-" * 80)
    if diagnoses:
        for i, diag in enumerate(diagnoses, 1):
            text = diag.get("text", "").strip()
            if text:
                print(f"  {i}. {text}")
    else:
        print("  (ninguno encontrado)")
    print()
    
    # METRIC
    metrics = entities.get("METRIC", [])
    print(f"[METRICAS] ({len(metrics)} encontradas):")
    print("-" * 80)
    if metrics:
        for i, metric in enumerate(metrics, 1):
            text = metric.get("text", "").strip()
            value = metric.get("value")
            metric_type = metric.get("type", "")
            if text:
                print(f"  {i}. {text}")
                if value:
                    print(f"     -> Valor: {value}, Tipo: {metric_type}")
    else:
        print("  (ninguna encontrada)")
    print()
    
    # CODE
    codes = entities.get("CODE", [])
    print(f"[CODIGOS] ({len(codes)} encontrados):")
    print("-" * 80)
    if codes:
        for i, code in enumerate(codes, 1):
            text = code.get("text", "").strip()
            if text:
                print(f"  {i}. {text}")
    else:
        print("  (ninguno encontrado)")
    print()
    
    # RATING
    ratings = entities.get("RATING", [])
    print(f"[VALORACIONES] ({len(ratings)} encontradas):")
    print("-" * 80)
    if ratings:
        for i, rating in enumerate(ratings, 1):
            text = rating.get("text", "").strip()
            value = rating.get("value")
            if text:
                print(f"  {i}. {text}")
                if value:
                    print(f"     -> Valor: {value}")
    else:
        print("  (ninguna encontrada)")
    print()
    
    # Procesar con el motor legal
    print("=" * 80)
    print("ANÁLISIS LEGAL (con deduplicación)")
    print("=" * 80)
    print()
    
    legal_engine = LegalEngine()
    analysis = await legal_engine.analyze(entities, doc_type)
    
    # Mostrar diagnósticos deduplicados
    unique_diagnoses = analysis.get("detected_diagnoses", [])
    print(f"[DIAGNOSTICOS UNICOS] (despues de deduplicacion): {len(unique_diagnoses)}")
    print("-" * 80)
    if unique_diagnoses:
        for i, diag in enumerate(unique_diagnoses, 1):
            text = diag.get("text", "").strip()
            body_part = diag.get("body_part", "")
            if text:
                print(f"  {i}. {text}")
                if body_part:
                    print(f"     -> Parte del cuerpo: {body_part}")
    else:
        print("  (ninguno encontrado)")
    print()
    
    # Mostrar valoraciones por capítulo
    chapter_valuations = analysis.get("chapter_valuations", [])
    print(f"[VALORACIONES POR CAPITULO]: {len(chapter_valuations)}")
    print("-" * 80)
    if chapter_valuations:
        for i, val in enumerate(chapter_valuations, 1):
            diagnosis = val.get("diagnosis", "")
            chapter = val.get("chapter", "")
            percentage = val.get("percentage", 0)
            class_num = val.get("class", "")
            print(f"  {i}. {diagnosis}")
            print(f"     -> Capitulo: {chapter}")
            print(f"     -> Clase: {class_num}, Porcentaje: {percentage}%")
    else:
        print("  (ninguna encontrada)")
    print()
    
    # Mostrar valoración final
    final_valuation = analysis.get("final_valuation")
    if final_valuation:
        print("=" * 80)
        print("VALORACIÓN FINAL (GDA)")
        print("=" * 80)
        print(f"  BDGP (Anexo III): {final_valuation.get('bdgp_percentage', 0)}%")
        print(f"  GDA Final: {final_valuation.get('gda_percentage', 0)}%")
        print(f"  Clase: {final_valuation.get('final_class', 'N/A')}")
        print(f"  Componentes: {final_valuation.get('components_count', 0)}")
        print()
    
    # Mostrar resumen
    print("=" * 80)
    print("RESUMEN")
    print("=" * 80)
    print(f"  Diagnósticos originales: {len(diagnoses)}")
    print(f"  Diagnósticos únicos: {len(unique_diagnoses)}")
    print(f"  Reducción: {len(diagnoses) - len(unique_diagnoses)} duplicados eliminados")
    print(f"  Métricas: {len(metrics)}")
    print(f"  Códigos: {len(codes)}")
    print(f"  Valoraciones: {len(ratings)}")
    print("=" * 80)

if __name__ == "__main__":
    # Ruta del PDF
    pdf_path = "../15.-Informe_pericial_Gemma_devesa_Hombro_Dr_Alonso-06_05_2024.pdf"
    
    # Verificar que el archivo existe
    from pathlib import Path
    if not Path(pdf_path).exists():
        print(f"Error: No se encontró el archivo: {pdf_path}")
        print("Buscando en el directorio raíz...")
        pdf_path = "15.-Informe_pericial_Gemma_devesa_Hombro_Dr_Alonso-06_05_2024.pdf"
        if not Path(pdf_path).exists():
            print(f"Error: No se encontró el archivo: {pdf_path}")
            sys.exit(1)
    
    asyncio.run(analyze_pdf(pdf_path))

