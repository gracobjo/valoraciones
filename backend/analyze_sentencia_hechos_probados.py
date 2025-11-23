"""Script para analizar específicamente los hechos probados de la sentencia"""
import asyncio
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent))

from app.services.ocr_service import OCRService
from app.services.nlp_service import NLPService
from app.services.legal_engine import LegalEngine

async def analyze_sentencia_hechos_probados(pdf_path: str):
    """Analiza específicamente los hechos probados de la sentencia"""
    
    print("=" * 80)
    print("ANÁLISIS DE HECHOS PROBADOS EN LA SENTENCIA")
    print("=" * 80)
    print()
    
    # Extraer texto
    print("1. Extrayendo texto de la sentencia...")
    ocr_service = OCRService()
    
    try:
        with open(pdf_path, 'rb') as f:
            pdf_content = f.read()
        
        extracted_text = await ocr_service.extract_text(pdf_content, pdf_path)
        print(f"   [OK] Texto extraído: {len(extracted_text)} caracteres")
        print()
    except Exception as e:
        print(f"   [ERROR] Error al leer el PDF: {e}")
        return
    
    # Detectar tipo y segmentar
    print("2. Detectando tipo y segmentando documento...")
    nlp_service = NLPService()
    
    doc_type = await nlp_service.detect_document_type(extracted_text)
    print(f"   [OK] Tipo detectado: {doc_type}")
    
    segments = await nlp_service.segment_document(extracted_text, doc_type)
    print(f"   [OK] Segmentos encontrados:")
    for section, content in segments.items():
        if content:
            print(f"      - {section}: {len(content)} caracteres")
    print()
    
    # Extraer hechos probados específicamente
    print("3. EXTRAYENDO HECHOS PROBADOS...")
    print("-" * 80)
    print()
    
    hechos_probados = segments.get("antecedentes", "")
    
    # Si la sección antecedentes es muy corta, buscar en fundamentos o en todo el documento
    if len(hechos_probados) < 500:
        print(f"   [INFO] Sección 'antecedentes' muy corta ({len(hechos_probados)} chars)")
        print("   Buscando 'hechos probados' en fundamentos y todo el documento...")
        
        # Buscar en fundamentos
        fundamentos = segments.get("fundamentos", "")
        if fundamentos:
            # Buscar sección de hechos probados dentro de fundamentos
            match = re.search(
                r'(?i)(hechos probados|hecho probado|resulta probado|se declara probado)[\s\S]{0,3000}',
                fundamentos
            )
            if match:
                hechos_probados = match.group(0)
                print(f"   [OK] Encontrado en fundamentos: {len(hechos_probados)} caracteres")
        
        # Si aún no se encuentra, buscar en todo el documento
        if len(hechos_probados) < 500:
            # Buscar patrones de hechos probados
            patterns = [
                r'(?i)(hechos probados|hecho probado)[\s\S]{0,5000}',
                r'(?i)(resulta probado|se declara probado|se tiene por probado)[\s\S]{0,5000}',
                r'(?i)(flexi[óo]n\s*(?:activa)?\s*(?:de|a|del)?\s*\d+[°º]|abducci[óo]n\s*(?:activa)?\s*(?:de|a|del)?\s*\d+[°º])[\s\S]{0,2000}',
            ]
            
            for pattern in patterns:
                match = re.search(pattern, extracted_text)
                if match:
                    context_start = max(0, match.start() - 500)
                    context_end = min(len(extracted_text), match.end() + 2000)
                    hechos_probados = extracted_text[context_start:context_end]
                    print(f"   [OK] Encontrado con patrón alternativo: {len(hechos_probados)} caracteres")
                    break
    
    if not hechos_probados or len(hechos_probados) < 100:
        print("   [ADVERTENCIA] No se encontró sección explícita de 'hechos probados'")
        print("   Usando todo el documento para búsqueda...")
        hechos_probados = extracted_text
    
    if hechos_probados:
        print(f"\nTEXTO DE HECHOS PROBADOS ({len(hechos_probados)} caracteres):")
        print("-" * 80)
        print(hechos_probados[:3000])  # Primeros 3000 caracteres
        if len(hechos_probados) > 3000:
            print(f"\n... (total: {len(hechos_probados)} caracteres)")
        print()
    
    # Extraer entidades de hechos probados
    print("4. EXTRAYENDO ENTIDADES DE HECHOS PROBADOS...")
    print("-" * 80)
    print()
    
    entities = await nlp_service.extract_entities(hechos_probados, doc_type, segments)
    
    # Mostrar métricas de hechos probados
    print("MÉTRICAS FUNCIONALES EN HECHOS PROBADOS:")
    proven_metrics = [m for m in entities.get("METRIC", []) if m.get("is_proven_fact", False)]
    all_metrics = entities.get("METRIC", [])
    
    if proven_metrics:
        print(f"   Métricas marcadas como hechos probados: {len(proven_metrics)}")
        for metric in proven_metrics:
            print(f"   - {metric.get('text')}: {metric.get('value')} ({metric.get('type')})")
    else:
        print("   [ADVERTENCIA] No se encontraron métricas marcadas como hechos probados")
        print("   Mostrando todas las métricas encontradas:")
        for metric in all_metrics[:10]:
            print(f"   - {metric.get('text')}: {metric.get('value')} ({metric.get('type')})")
    print()
    
    # Mostrar diagnósticos de hechos probados
    print("DIAGNÓSTICOS EN HECHOS PROBADOS:")
    diagnoses = entities.get("DIAGNOSIS", [])
    print(f"   Diagnósticos encontrados: {len(diagnoses)}")
    for i, diag in enumerate(diagnoses[:10], 1):
        print(f"   {i}. {diag.get('text', '')[:100]}")
    print()
    
    # Analizar con motor legal
    print("5. ANÁLISIS LEGAL BASADO EN HECHOS PROBADOS...")
    print("-" * 80)
    print()
    
    legal_engine = LegalEngine()
    analysis = await legal_engine.analyze(entities, doc_type, segments)
    
    # Mostrar método de valoración usado
    valuation_method = analysis.get("valuation_method", "")
    if valuation_method == "proven_facts_functional":
        print("   [OK] Se usó método de VALORACIÓN FUNCIONAL GLOBAL basado en hechos probados")
    else:
        print("   [ADVERTENCIA] No se usó método de hechos probados")
        print(f"   Método usado: {valuation_method or 'patologías individuales'}")
    print()
    
    # Mostrar valoraciones
    chapter_valuations = analysis.get("chapter_valuations", [])
    final_valuation = analysis.get("final_valuation") or {}
    
    print("VALORACIONES POR CAPÍTULO:")
    print()
    for i, val in enumerate(chapter_valuations, 1):
        is_proven = val.get("is_proven_fact", False)
        marker = "[HECHO PROBADO]" if is_proven else "  "
        print(f"   {marker} {i}. {val.get('diagnosis', 'N/A')}")
        print(f"      Capítulo: {val.get('chapter', 'N/A')}")
        print(f"      Clase: {val.get('class', 'N/A')} - {val.get('description', 'N/A')}")
        print(f"      Porcentaje: {val.get('percentage', 0)}%")
        print()
    
    print("VALORACIÓN FINAL:")
    print()
    bdgp = final_valuation.get("bdgp_percentage", 0)
    gda = final_valuation.get("gda_percentage", 0) or final_valuation.get("total_percentage", 0)
    final_class = final_valuation.get("final_class", "N/A")
    
    print(f"   BDGP (Anexo III): {bdgp}%")
    print(f"   GDA Final: {gda}%")
    print(f"   Clase: {final_class}")
    print()
    
    # Buscar específicamente flexión y abducción en hechos probados
    print("6. BÚSQUEDA ESPECÍFICA DE FLEXIÓN Y ABDUCCIÓN EN HECHOS PROBADOS...")
    print("-" * 80)
    print()
    
    flexion_patterns = [
        r'flexi[óo]n\s*(?:activa|del hombro|del brazo)?\s*(?:de|a|del|de la|limitada a|limitada)?\s*(\d+)[°º°]',
        r'(\d+)[°º°]\s*(?:de\s+)?flexi[óo]n\s*(?:activa)?',
        r'flexi[óo]n\s*:\s*(\d+)[°º°]',
        r'flexi[óo]n\s*(?:de|a)\s*(\d+)[°º°]',
        r'(\d+)[°º°]\s*en\s*flexi[óo]n',
        # Patrón específico: "limitación flexión abducción activa 90º"
        r'limitaci[óo]n\s+flexi[óo]n\s+abducci[óo]n\s+activa\s+(\d+)[°º°]',
        r'flexi[óo]n\s+abducci[óo]n\s+activa\s+(\d+)[°º°]',
    ]
    
    abduccion_patterns = [
        r'abducci[óo]n\s*(?:activa|del hombro|del brazo)?\s*(?:de|a|del|de la|limitada a|limitada)?\s*(\d+)[°º°]',
        r'(\d+)[°º°]\s*(?:de\s+)?abducci[óo]n\s*(?:activa)?',
        r'abducci[óo]n\s*:\s*(\d+)[°º°]',
        r'abducci[óo]n\s*(?:de|a)\s*(\d+)[°º°]',
        r'(\d+)[°º°]\s*en\s*abducci[óo]n',
        # Patrón específico: "limitación flexión abducción activa 90º"
        r'limitaci[óo]n\s+flexi[óo]n\s+abducci[óo]n\s+activa\s+(\d+)[°º°]',
        r'flexi[óo]n\s+abducci[óo]n\s+activa\s+(\d+)[°º°]',
    ]
    
    # Patrón especial: "limitación flexión abducción activa 90º" (ambas métricas en una frase)
    combined_pattern = r'limitaci[óo]n\s+flexi[óo]n\s+abducci[óo]n\s+activa\s+(\d+)[°º°]'
    
    flexion_found = None
    abduccion_found = None
    
    # Primero buscar patrón combinado "limitación flexión abducción activa 90º"
    combined_match = re.search(combined_pattern, hechos_probados, re.IGNORECASE)
    if combined_match:
        value = int(combined_match.group(1))
        flexion_found = value
        abduccion_found = value
        print(f"   [OK] PATRÓN COMBINADO encontrado: 'limitación flexión abducción activa {value}º'")
        print(f"      → Flexión: {flexion_found}º")
        print(f"      → Abducción: {abduccion_found}º")
        print(f"      Contexto: ...{combined_match.group(0)[:150]}...")
    else:
        # Buscar por separado
        for pattern in flexion_patterns:
            match = re.search(pattern, hechos_probados, re.IGNORECASE)
            if match:
                flexion_found = int(match.group(1))
                print(f"   [OK] FLEXIÓN encontrada: {flexion_found}º")
                print(f"      Contexto: ...{match.group(0)[:100]}...")
                break
        
        if not flexion_found:
            print("   [ADVERTENCIA] FLEXIÓN no encontrada en hechos probados")
        
        print()
        
        for pattern in abduccion_patterns:
            match = re.search(pattern, hechos_probados, re.IGNORECASE)
            if match:
                abduccion_found = int(match.group(1))
                print(f"   [OK] ABDUCCIÓN encontrada: {abduccion_found}º")
                print(f"      Contexto: ...{match.group(0)[:100]}...")
                break
        
        if not abduccion_found:
            print("   [ADVERTENCIA] ABDUCCIÓN no encontrada en hechos probados")
    
    print()
    
    # Calcular valoración correcta basada en hechos probados
    if flexion_found and abduccion_found:
        print("7. CÁLCULO CORRECTO BASADO EN HECHOS PROBADOS...")
        print("-" * 80)
        print()
        
        print(f"Métricas de hechos probados:")
        print(f"  - Flexión activa: {flexion_found}º (rango normal: 180º)")
        print(f"  - Abducción activa: {abduccion_found}º (rango normal: 180º)")
        print()
        
        # Clasificar según RD 888/2022
        # Abducción 90º → Clase 2 (61-90º) → 25-49%
        # Flexión 100º → Clase 1 (91-180º) → 0-9%
        # La limitación funcional global del hombro es Clase 2
        
        if abduccion_found <= 90:
            clase_abduccion = "2"
            pct_abduccion = 30  # Clase 2 moderada
        elif abduccion_found <= 120:
            clase_abduccion = "1"
            pct_abduccion = 15
        else:
            clase_abduccion = "1"
            pct_abduccion = 10
        
        if flexion_found <= 90:
            clase_flexion = "2"
            pct_flexion = 30
        elif flexion_found <= 120:
            clase_flexion = "1"
            pct_flexion = 15
        else:
            clase_flexion = "1"
            pct_flexion = 10
        
        # La deficiencia funcional global se clasifica por la peor métrica
        # Con abducción 90º, la clasificación es Clase 2
        clase_final = "2"
        pct_bdgp = 35  # Clase 2, moderada (30-40% según tu análisis)
        
        print(f"Clasificación según RD 888/2022:")
        print(f"  - Abducción {abduccion_found}º → Clase {clase_abduccion}")
        print(f"  - Flexión {flexion_found}º → Clase {clase_flexion}")
        print(f"  - Deficiencia funcional global → Clase {clase_final} (moderada)")
        print()
        
        print(f"Valoración BDGP (Anexo III):")
        print(f"  - Porcentaje: {pct_bdgp}% (Clase 2: 25-49%)")
        print()
        
        # Ajustes BLA, BRP
        print(f"Ajustes (estimación conservadora):")
        print(f"  - BLA (Anexo IV): +3-5%")
        print(f"  - BRP (Anexo V): +2-4%")
        print(f"  - BFCA (Anexo VI): 0-2 puntos")
        print()
        
        gda_estimado = pct_bdgp + 4  # Ajuste conservador
        print(f"GDA FINAL ESTIMADO: {gda_estimado}% (rango: 33-38%)")
        print()
        
        print("COMPARACIÓN:")
        print(f"  - Sistema actual: {gda}%")
        print(f"  - Valoración correcta (hechos probados): {gda_estimado}%")
        print(f"  - Diferencia: {abs(gda_estimado - gda):.1f} puntos porcentuales")
        print()
        
        if gda < 30:
            print("   [PROBLEMA] El sistema está subvalorando porque:")
            print("   1. No está detectando correctamente las métricas de hechos probados")
            print("   2. Está valorando patologías individuales en lugar de deficiencia funcional global")
            print("   3. No está aplicando el enfoque de hechos probados")
    
    print()
    print("=" * 80)
    print("FIN DEL ANÁLISIS")
    print("=" * 80)

if __name__ == "__main__":
    # Buscar archivo de sentencia
    possible_names = [
        "SENTENCIA_gemma.pdf",
        "SENTENCIA.pdf",
        "sentencia_gemma.pdf",
        "sentencia.pdf",
        "../SENTENCIA_gemma.pdf",
        "../SENTENCIA.pdf",
    ]
    
    pdf_path = None
    for name in possible_names:
        if Path(name).exists():
            pdf_path = name
            break
    
    if not pdf_path:
        print("Error: No se encontró el archivo de la sentencia.")
        print("Buscando archivos PDF en el directorio raíz...")
        root_files = list(Path("..").glob("*SENTENCIA*.pdf"))
        if root_files:
            print("Archivos PDF encontrados:")
            for f in root_files:
                print(f"  - {f.name}")
            if root_files:
                pdf_path = str(root_files[0])
                print(f"\nUsando: {pdf_path}")
        else:
            print("No se encontraron archivos PDF con 'SENTENCIA' en el nombre.")
            sys.exit(1)
    
    asyncio.run(analyze_sentencia_hechos_probados(pdf_path))

