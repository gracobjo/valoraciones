"""Script para analizar la resolución administrativa y comparar con el informe pericial"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from app.services.ocr_service import OCRService
from app.services.nlp_service import NLPService
from app.services.legal_engine import LegalEngine
from app.services.report_generator import ReportGenerator

async def analyze_resolution(pdf_path: str):
    """Analiza la resolución administrativa"""
    
    print("=" * 80)
    print(f"ANÁLISIS DE LA RESOLUCIÓN ADMINISTRATIVA")
    print(f"Archivo: {pdf_path}")
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
    
    # Buscar porcentajes mencionados en el texto
    print("4. Buscando valoraciones mencionadas en la resolución...")
    print("-" * 80)
    
    # Buscar porcentajes
    import re
    percentages = re.findall(r'(\d+)\s*%', extracted_text)
    if percentages:
        print(f"   Porcentajes encontrados en el texto:")
        for pct in set(percentages):
            print(f"     - {pct}%")
    
    # Buscar texto alrededor de porcentajes importantes
    print()
    print("   Contexto de porcentajes encontrados:")
    for pct in ['10', '33', '25', '50', '67']:
        pattern = rf'.{{0,150}}{pct}\s*%.{{0,150}}'
        matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE))
        if matches:
            print(f"   {pct}%:")
            for match in matches[:2]:  # Primeros 2
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
    print()
    
    # Buscar diagnósticos reconocidos
    diagnoses = entities.get("DIAGNOSIS", [])
    print(f"5. Diagnósticos mencionados en la resolución: {len(diagnoses)}")
    print("-" * 80)
    if diagnoses:
        for i, diag in enumerate(diagnoses[:10], 1):  # Primeros 10
            text = diag.get("text", "").strip()
            if text:
                print(f"   {i}. {text[:100]}...")
    print()
    
    # Buscar códigos CIE-10
    codes = entities.get("CODE", [])
    print(f"6. Códigos CIE-10 mencionados: {len(codes)}")
    print("-" * 80)
    if codes:
        for i, code in enumerate(codes, 1):
            text = code.get("text", "").strip()
            if text:
                print(f"   {i}. {text}")
    print()
    
    # Procesar con el motor legal
    print("7. Análisis legal (valoración según RD 888/2022)...")
    print("-" * 80)
    
    legal_engine = LegalEngine()
    analysis = await legal_engine.analyze(entities, doc_type)
    
    # Mostrar valoración calculada
    final_valuation = analysis.get("final_valuation") or {}
    chapter_valuations = analysis.get("chapter_valuations", [])
    
    print(f"   Valoración calculada por el sistema:")
    if final_valuation:
        print(f"     BDGP: {final_valuation.get('bdgp_percentage', 0)}%")
        print(f"     GDA: {final_valuation.get('gda_percentage', 0)}%")
        print(f"     Clase: {final_valuation.get('final_class', 'N/A')}")
    else:
        print(f"     No se pudo calcular valoración (no hay diagnósticos detectados)")
    print(f"     Componentes: {len(chapter_valuations)} deficiencias")
    print()
    
    # Comparación
    print("=" * 80)
    print("COMPARACIÓN: RESOLUCIÓN vs INFORME PERICIAL")
    print("=" * 80)
    print()
    print("RESOLUCIÓN ADMINISTRATIVA:")
    print("  - Porcentaje reconocido: 10%")
    print(f"  - Diagnósticos detectados: {len(diagnoses)}")
    gda_calculado = final_valuation.get('gda_percentage', 0) if final_valuation else 0
    print(f"  - Valoración calculada por IA: {gda_calculado}%")
    print()
    print("INFORME PERICIAL (análisis anterior):")
    print("  - Porcentaje estimado: 67.4%")
    print("  - Componentes: 7 deficiencias")
    print("  - BDGP: 60.7%")
    print()
    print("DIFERENCIA:")
    diff = gda_calculado - 10
    print(f"  - Diferencia entre resolución (10%) y cálculo IA: {diff:.1f}%")
    print(f"  - Diferencia entre resolución (10%) y pericial (67.4%): 57.4%")
    print()
    
    # Buscar justificación del 10%
    print("8. Buscando justificación del 10% en la resolución...")
    print("-" * 80)
    
    # Buscar texto alrededor de "10%"
    text_lower = extracted_text.lower()
    if "10%" in extracted_text or "10 %" in extracted_text:
        # Buscar contexto alrededor del 10%
        pattern = r'.{0,200}10\s*%.{0,200}'
        matches = re.finditer(pattern, extracted_text, re.IGNORECASE)
        print("   Contexto donde se menciona el 10%:")
        print()
        for i, match in enumerate(list(matches)[:5], 1):  # Primeros 5
            context = match.group(0)
            # Limpiar saltos de línea múltiples
            context = re.sub(r'\s+', ' ', context)
            print(f"   {i}. ...{context}...")
            print()
    
    # Buscar diagnósticos específicos mencionados
    print("9. Diagnóstico específico reconocido en la resolución:")
    print("-" * 80)
    
    # Buscar patrones comunes en resoluciones
    diagnosticos_encontrados = []
    
    if "m75" in text_lower or "m 75" in text_lower or "m75.91" in text_lower:
        diagnosticos_encontrados.append("Código M75 (lesión de hombro)")
        print("   - Se menciona código M75 (lesión de hombro)")
    
    if "lesión no especificada" in text_lower or "lesion no especificada" in text_lower:
        diagnosticos_encontrados.append("Lesión no especificada")
        print("   - Se menciona 'lesión no especificada'")
    
    if "clase 1" in text_lower or "clase i" in text_lower:
        print("   - Se asigna Clase 1 (Deficiencia leve: 0-9%)")
    
    if "clase 2" in text_lower or "clase ii" in text_lower:
        print("   - Se menciona Clase 2 (Deficiencia moderada: 25-49%)")
    
    # Buscar texto completo de la resolución sobre el diagnóstico
    print()
    print("   Texto completo sobre el diagnóstico reconocido:")
    print("-" * 80)
    
    # Buscar secciones relevantes
    if "diagnóstico" in text_lower:
        # Buscar párrafos que contengan "diagnóstico" y "10%"
        pattern = r'.{0,300}diagnóstico.{0,300}10\s*%.{0,300}'
        matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE | re.DOTALL))
        if matches:
            for i, match in enumerate(matches[:3], 1):
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"   {i}. {context}")
                print()
    
    # Buscar la parte de "RESUELVE" o "DISPOSITIVO"
    if "resuelve" in text_lower or "dispositivo" in text_lower:
        print("   Sección RESUELVE/DISPOSITIVO encontrada")
        # Extraer esa sección
        pattern = r'(?i)(resuelve|dispositivo).{0,500}'
        matches = list(re.finditer(pattern, extracted_text, re.DOTALL))
        if matches:
            for match in matches[:1]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"   {context[:500]}...")
                print()
    
    print()
    
    # Mostrar texto completo para análisis manual
    print("=" * 80)
    print("TEXTO COMPLETO DE LA RESOLUCIÓN (para análisis)")
    print("=" * 80)
    print()
    print(extracted_text)
    print()
    print("=" * 80)
    print()
    
    # Buscar específicamente el 10% y su contexto
    print("10. ANÁLISIS ESPECÍFICO DEL 10%")
    print("-" * 80)
    print()
    
    # Buscar todas las menciones del 10%
    pattern_10 = r'.{0,300}10\s*%.{0,300}'
    matches_10 = list(re.finditer(pattern_10, extracted_text, re.IGNORECASE | re.DOTALL))
    
    if matches_10:
        print(f"   Se encontraron {len(matches_10)} menciones del 10%:")
        print()
        for i, match in enumerate(matches_10, 1):
            context = match.group(0)
            context = re.sub(r'\s+', ' ', context)
            print(f"   MENCION {i}:")
            print(f"   {context}")
            print()
    else:
        print("   No se encontró '10%' explícitamente en el texto.")
        print("   Buscando variaciones...")
        # Buscar "diez por ciento", "10 por ciento", etc.
        pattern_variations = [
            r'.{0,300}diez\s+por\s+ciento.{0,300}',
            r'.{0,300}10\s+por\s+ciento.{0,300}',
            r'.{0,300}grado\s+de\s+discapacidad.{0,300}10.{0,300}',
        ]
        for pattern in pattern_variations:
            matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE | re.DOTALL))
            if matches:
                print(f"   Encontrado con patrón alternativo:")
                for match in matches[:2]:
                    context = match.group(0)
                    context = re.sub(r'\s+', ' ', context)
                    print(f"   {context}")
                print()
    
    # Buscar el diagnóstico específico mencionado
    print("11. DIAGNÓSTICO RECONOCIDO EN LA RESOLUCIÓN:")
    print("-" * 80)
    print()
    
    # Buscar códigos M75 (lesión de hombro)
    if "m75" in text_lower or "m 75" in text_lower:
        print("   ✓ Se menciona código M75 (lesión de hombro)")
        # Buscar contexto
        pattern_m75 = r'.{0,200}m\s*75[^\s]*.{0,200}'
        matches_m75 = list(re.finditer(pattern_m75, extracted_text, re.IGNORECASE))
        if matches_m75:
            print("   Contexto del código M75:")
            for match in matches_m75[:3]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
        print()
    
    # Buscar "lesión no especificada"
    if "no especificada" in text_lower or "inespecificada" in text_lower:
        print("   ✓ Se menciona 'lesión no especificada' o similar")
        pattern_inespecifica = r'.{0,200}no\s+especificada.{0,200}'
        matches = list(re.finditer(pattern_inespecifica, extracted_text, re.IGNORECASE))
        if matches:
            print("   Contexto:")
            for match in matches[:2]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
        print()
    
    # Buscar "clase 1" o "deficiencia leve"
    if "clase 1" in text_lower or "clase i" in text_lower or "deficiencia leve" in text_lower:
        print("   ✓ Se asigna Clase 1 (Deficiencia leve: 0-9%)")
        print("   Esto explicaría el 10% (límite superior de Clase 1)")
        print()
    
    # Buscar la sección de motivación o fundamentos
    print("12. SECCIÓN DE MOTIVACIÓN/FUNDAMENTOS:")
    print("-" * 80)
    print()
    
    # Buscar "fundamentos", "motivación", "considerando"
    for keyword in ["fundamentos", "motivacion", "motivación", "considerando", "resuelve"]:
        if keyword in text_lower:
            pattern = rf'.{{0,100}}{keyword}.{{0,800}}'
            matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE | re.DOTALL))
            if matches:
                print(f"   Sección '{keyword.upper()}' encontrada:")
                for match in matches[:1]:
                    context = match.group(0)
                    context = re.sub(r'\s+', ' ', context)
                    print(f"   {context[:600]}...")
                print()
                break
    
    # Análisis de inconsistencia
    print("=" * 80)
    print("ANÁLISIS DE INCONSISTENCIA")
    print("=" * 80)
    print()
    print("POSIBLES RAZONES DEL 10% EN LA RESOLUCIÓN:")
    print()
    print("1. Diagnóstico genérico:")
    print("   - La resolución puede estar usando un código genérico (ej: M75.91)")
    print("   - No especifica las múltiples patologías detectadas en el pericial")
    print()
    print("2. Clasificación incorrecta:")
    print("   - Asigna Clase 1 (0-9%) en lugar de Clase 2 o 3")
    print("   - No considera la suma de múltiples deficiencias")
    print()
    print("3. Omisión de deficiencias:")
    print("   - Solo reconoce una lesión principal")
    print("   - No valora las 7 deficiencias detectadas en el pericial")
    print()
    print("4. No aplica fórmula de combinación:")
    print("   - No suma las deficiencias según RD 888/2022")
    print("   - No aplica ajustes por BLA, BRP, BFCA")
    print()
    print("RECOMENDACIÓN:")
    print("   La valoración del 10% parece subestimada. El análisis técnico indica")
    print("   que debería estar entre 60-67% según el RD 888/2022, considerando:")
    print("   - Múltiples deficiencias en el mismo sistema (hombro)")
    print("   - Limitaciones funcionales significativas")
    print("   - Restricciones en participación laboral")
    print()

if __name__ == "__main__":
    # Buscar el archivo
    possible_names = [
        "CopiaAutentica_NOTI GEMMA.pdf",
        "CopiaAutentica_NOTI_GEMMA.pdf",
        "CopiaAutentica NOTI GEMMA.pdf",
        "../CopiaAutentica_NOTI GEMMA.pdf",
        "../CopiaAutentica_NOTI_GEMMA.pdf",
    ]
    
    pdf_path = None
    for name in possible_names:
        if Path(name).exists():
            pdf_path = name
            break
    
    if not pdf_path:
        print("Error: No se encontró el archivo de la resolución.")
        print("Buscando archivos PDF en el directorio raíz...")
        root_files = list(Path("..").glob("*.pdf"))
        if root_files:
            print("Archivos PDF encontrados:")
            for f in root_files:
                print(f"  - {f.name}")
            if root_files:
                pdf_path = str(root_files[0])
                print(f"\nUsando: {pdf_path}")
        else:
            print("No se encontraron archivos PDF.")
            sys.exit(1)
    
    asyncio.run(analyze_resolution(pdf_path))

