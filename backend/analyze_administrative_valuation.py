"""Script para analizar cómo valora la Administración y comparar con nuestro sistema"""
import asyncio
import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent))

from app.services.ocr_service import OCRService
from app.services.nlp_service import NLPService
from app.services.legal_engine import LegalEngine

async def analyze_administrative_valuation(pdf_path: str):
    """Analiza la metodología de valoración de la Administración"""
    
    print("=" * 80)
    print("ANÁLISIS DE LA METODOLOGÍA DE VALORACIÓN ADMINISTRATIVA")
    print("=" * 80)
    print()
    
    # Extraer texto
    print("1. Extrayendo texto de la resolución...")
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
    
    # Analizar con nuestro sistema
    print("2. Analizando con nuestro sistema...")
    nlp_service = NLPService()
    legal_engine = LegalEngine()
    
    doc_type = await nlp_service.detect_document_type(extracted_text)
    entities = await nlp_service.extract_entities(extracted_text)
    analysis = await legal_engine.analyze(entities, doc_type)
    
    our_valuation = analysis.get("final_valuation") or {}
    our_percentage = our_valuation.get("gda_percentage", 0) or our_valuation.get("total_percentage", 0) if our_valuation else 0
    our_chapters = analysis.get("chapter_valuations", [])
    
    print(f"   [OK] Análisis completado")
    print(f"   - Porcentaje calculado por nuestro sistema: {our_percentage}%")
    print(f"   - Deficiencias detectadas: {len(our_chapters)}")
    print()
    
    # Buscar valoración administrativa en el texto
    print("3. Buscando valoración administrativa en el texto...")
    print("-" * 80)
    print()
    
    text_lower = extracted_text.lower()
    
    # Buscar porcentajes mencionados
    percentages_found = []
    pattern_percentage = r'(\d+)\s*%'
    for match in re.finditer(pattern_percentage, extracted_text):
        pct = int(match.group(1))
        if 0 <= pct <= 100:
            # Obtener contexto
            start = max(0, match.start() - 100)
            end = min(len(extracted_text), match.end() + 100)
            context = extracted_text[start:end]
            percentages_found.append({
                "percentage": pct,
                "context": context.strip()
            })
    
    print(f"   Porcentajes encontrados en el texto:")
    for pct_info in percentages_found[:10]:  # Primeros 10
        print(f"   - {pct_info['percentage']}%")
        print(f"     Contexto: ...{pct_info['context'][:150]}...")
        print()
    
    # Buscar diagnóstico reconocido
    print("4. Diagnóstico reconocido por la Administración:")
    print("-" * 80)
    print()
    
    admin_diagnosis = None
    admin_code = None
    
    # Buscar códigos CIE-10
    if "m75" in text_lower:
        pattern_code = r'm\s*75[\.\s]*\d*'
        matches = list(re.finditer(pattern_code, extracted_text, re.IGNORECASE))
        if matches:
            admin_code = matches[0].group(0)
            print(f"   ✓ Código CIE-10 encontrado: {admin_code}")
            # Buscar contexto
            start = max(0, matches[0].start() - 150)
            end = min(len(extracted_text), matches[0].end() + 150)
            context = extracted_text[start:end]
            print(f"     Contexto: ...{context}...")
            print()
    
    # Buscar "lesión no especificada" o diagnóstico genérico
    if "no especificada" in text_lower or "inespecificada" in text_lower:
        pattern = r'.{0,200}no\s+especificada.{0,200}'
        matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE))
        if matches:
            admin_diagnosis = matches[0].group(0)
            print(f"   ✓ Diagnóstico genérico encontrado:")
            print(f"     {admin_diagnosis}")
            print()
    
    # Buscar clase asignada
    print("5. Clase asignada por la Administración:")
    print("-" * 80)
    print()
    
    admin_class = None
    if "clase 1" in text_lower or "clase i" in text_lower:
        admin_class = "1"
        print("   ✓ Clase 1 (Deficiencia leve: 0-9%)")
        pattern = r'.{0,200}clase\s+1.{0,200}'
        matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE))
        if matches:
            context = matches[0].group(0)
            print(f"     Contexto: ...{context}...")
    elif "clase 2" in text_lower or "clase ii" in text_lower:
        admin_class = "2"
        print("   ✓ Clase 2 (Deficiencia moderada: 25-49%)")
    elif "clase 3" in text_lower or "clase iii" in text_lower:
        admin_class = "3"
        print("   ✓ Clase 3 (Deficiencia grave: 50-74%)")
    else:
        print("   - No se encontró clase explícita")
    print()
    
    # Buscar fundamentos legales mencionados
    print("6. Fundamentos legales mencionados en la resolución:")
    print("-" * 80)
    print()
    
    legal_bases = []
    if "rd 888" in text_lower or "real decreto 888" in text_lower:
        legal_bases.append("RD 888/2022")
        print("   ✓ Se menciona RD 888/2022")
    
    if "anexo iii" in text_lower or "anexo 3" in text_lower:
        legal_bases.append("Anexo III (BDGP)")
        print("   ✓ Se menciona Anexo III")
    
    if "anexo iv" in text_lower or "anexo 4" in text_lower:
        legal_bases.append("Anexo IV (BLA)")
        print("   ✓ Se menciona Anexo IV")
    
    if "anexo v" in text_lower or "anexo 5" in text_lower:
        legal_bases.append("Anexo V (BRP)")
        print("   ✓ Se menciona Anexo V")
    
    if not legal_bases:
        print("   - No se encontraron referencias explícitas a los anexos")
    print()
    
    # Buscar sección de motivación o fundamentos
    print("7. Sección de motivación/fundamentos:")
    print("-" * 80)
    print()
    
    # Buscar palabras clave de motivación
    motivation_keywords = ["fundamentos", "motivacion", "motivación", "considerando", 
                          "resulta que", "procede", "atendiendo"]
    
    for keyword in motivation_keywords:
        if keyword in text_lower:
            pattern = rf'.{{0,100}}{keyword}.{{0,500}}'
            matches = list(re.finditer(pattern, extracted_text, re.IGNORECASE | re.DOTALL))
            if matches:
                print(f"   Sección '{keyword.upper()}' encontrada:")
                context = matches[0].group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"   {context[:600]}...")
                print()
                break
    
    # Comparación
    print("=" * 80)
    print("COMPARACIÓN: ADMINISTRACIÓN vs NUESTRO SISTEMA")
    print("=" * 80)
    print()
    
    admin_percentage = None
    for pct_info in percentages_found:
        if 5 <= pct_info['percentage'] <= 15:  # Buscar porcentaje entre 5-15%
            admin_percentage = pct_info['percentage']
            break
    
    if not admin_percentage and percentages_found:
        admin_percentage = percentages_found[0]['percentage']
    
    print("METODOLOGÍA ADMINISTRATIVA:")
    print(f"  - Porcentaje reconocido: {admin_percentage}% (estimado)" if admin_percentage else "  - Porcentaje: No encontrado explícitamente")
    print(f"  - Diagnóstico: {admin_diagnosis or admin_code or 'No especificado'}")
    print(f"  - Clase asignada: Clase {admin_class or 'N/A'}")
    print(f"  - Fundamentos legales: {', '.join(legal_bases) if legal_bases else 'No especificados'}")
    print(f"  - Deficiencias reconocidas: 1 (diagnóstico genérico)")
    print()
    
    print("METODOLOGÍA DE NUESTRO SISTEMA:")
    print(f"  - Porcentaje calculado: {our_percentage}%")
    print(f"  - BDGP (Anexo III): {our_valuation.get('bdgp_percentage', 0)}%")
    print(f"  - GDA Final: {our_percentage}%")
    print(f"  - Clase asignada: Clase {our_valuation.get('final_class', 'N/A')}")
    print(f"  - Deficiencias detectadas: {len(our_chapters)}")
    print(f"  - Fundamentos legales: RD 888/2022, Art. 4.2 (Anexos I-VI)")
    print()
    
    if admin_percentage:
        diff = our_percentage - admin_percentage
        print("DIFERENCIAS CLAVE:")
        print()
        print("1. DIAGNÓSTICO:")
        print(f"   - Administración: Usa diagnóstico genérico ({admin_code or 'M75.91'})")
        print(f"   - Nuestro sistema: Detecta {len(our_chapters)} deficiencias específicas")
        print()
        print("2. METODOLOGÍA DE CÁLCULO:")
        print(f"   - Administración: Valoración única (Clase {admin_class or '1'})")
        print(f"   - Nuestro sistema: Fórmula de combinación para múltiples deficiencias")
        print()
        print("3. BAREOS APLICADOS:")
        print(f"   - Administración: Solo Anexo III (BDGP) - diagnóstico único")
        print(f"   - Nuestro sistema: BDGP + BLA + BRP + BFCA (Art. 4.2)")
        print()
        print("4. RESULTADO:")
        print(f"   - Diferencia: {abs(diff):.1f} puntos porcentuales")
        if diff > 20:
            print(f"   - La administración subestima significativamente el grado")
        elif diff > 10:
            print(f"   - La administración subestima el grado")
        else:
            print(f"   - Diferencia moderada")
        print()
    
    # Recomendaciones
    print("=" * 80)
    print("RECOMENDACIONES PARA VERIFICAR LA VALORACIÓN ADMINISTRATIVA")
    print("=" * 80)
    print()
    print("Para comprobar cómo valora la Administración, busca en la resolución:")
    print()
    print("1. SECCIÓN 'FUNDAMENTOS' o 'MOTIVACIÓN':")
    print("   - Debe explicar qué diagnóstico reconoce")
    print("   - Debe indicar qué anexo del RD 888/2022 aplica")
    print("   - Debe justificar la clase asignada")
    print()
    print("2. SECCIÓN 'DISPOSITIVO' o 'RESUELVE':")
    print("   - Debe indicar el porcentaje final reconocido")
    print("   - Debe mencionar la clase de deficiencia")
    print()
    print("3. VERIFICAR:")
    print("   - ¿Se mencionan todos los diagnósticos del pericial?")
    print("   - ¿Se aplica la fórmula de combinación para múltiples deficiencias?")
    print("   - ¿Se consideran los baremos BLA, BRP, BFCA?")
    print("   - ¿La clase asignada corresponde al porcentaje según RD 888/2022?")
    print()
    
    # Mostrar texto completo para análisis manual
    print("=" * 80)
    print("TEXTO COMPLETO DE LA RESOLUCIÓN (para análisis manual)")
    print("=" * 80)
    print()
    print(extracted_text)
    print()

if __name__ == "__main__":
    pdf_path = "../CopiaAutentica_NOTI GEMMA.pdf"
    if not Path(pdf_path).exists():
        pdf_path = "CopiaAutentica_NOTI GEMMA.pdf"
    
    if not Path(pdf_path).exists():
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
    
    asyncio.run(analyze_administrative_valuation(pdf_path))

