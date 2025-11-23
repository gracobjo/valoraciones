"""Script para analizar la resolución con OCR mejorado"""
import asyncio
import sys
from pathlib import Path
import fitz  # PyMuPDF

sys.path.insert(0, str(Path(__file__).parent))

async def analyze_with_ocr(pdf_path: str):
    """Analiza el PDF con OCR mejorado"""
    
    print("=" * 80)
    print("ANÁLISIS DE LA RESOLUCIÓN CON OCR MEJORADO")
    print("=" * 80)
    print()
    
    try:
        # Abrir PDF
        doc = fitz.open(pdf_path)
        print(f"   PDF abierto: {len(doc)} páginas")
        print()
        
        # Extraer texto de cada página
        all_text = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Si el texto es muy corto, puede ser una imagen escaneada
            if len(text.strip()) < 100:
                print(f"   Página {page_num + 1}: Texto muy corto ({len(text)} chars), puede ser escaneada")
                # Intentar OCR si está disponible
                try:
                    from app.services.ocr_service import OCRService
                    ocr_service = OCRService()
                    with open(pdf_path, 'rb') as f:
                        pdf_content = f.read()
                    # Extraer solo esta página con OCR
                    # Por ahora, continuar con el texto disponible
                except:
                    pass
            
            all_text.append(f"=== PÁGINA {page_num + 1} ===\n{text}\n")
        
        full_text = "\n".join(all_text)
        doc.close()
        
        # Si el texto es muy corto, intentar con OCR completo
        if len(full_text.strip()) < 500:
            print("   Texto muy corto detectado. Intentando OCR...")
            try:
                from app.services.ocr_service import OCRService
                ocr_service = OCRService()
                with open(pdf_path, 'rb') as f:
                    pdf_content = f.read()
                full_text = await ocr_service.extract_text(pdf_content, pdf_path)
                print(f"   Texto extraído con OCR: {len(full_text)} caracteres")
            except Exception as e:
                print(f"   Error en OCR: {e}")
                print("   Continuando con texto disponible...")
        
        print(f"   Texto extraído: {len(full_text)} caracteres")
        print()
        
        # Buscar el 10%
        print("=" * 80)
        print("BÚSQUEDA DEL 10% Y SU JUSTIFICACIÓN")
        print("=" * 80)
        print()
        
        import re
        
        # Buscar "10%"
        pattern_10 = r'.{0,400}10\s*%.{0,400}'
        matches = list(re.finditer(pattern_10, full_text, re.IGNORECASE | re.DOTALL))
        
        if matches:
            print(f"   Se encontraron {len(matches)} menciones del 10%:")
            print()
            for i, match in enumerate(matches, 1):
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"   MENCION {i}:")
                print(f"   {context}")
                print()
        else:
            print("   No se encontró '10%' explícitamente.")
            print("   Buscando 'diez por ciento'...")
            pattern_diez = r'.{0,400}diez\s+por\s+ciento.{0,400}'
            matches = list(re.finditer(pattern_diez, full_text, re.IGNORECASE | re.DOTALL))
            if matches:
                for i, match in enumerate(matches, 1):
                    context = match.group(0)
                    context = re.sub(r'\s+', ' ', context)
                    print(f"   {i}. {context}")
                    print()
        
        # Buscar diagnóstico
        print("=" * 80)
        print("DIAGNÓSTICO RECONOCIDO")
        print("=" * 80)
        print()
        
        text_lower = full_text.lower()
        
        # Buscar M75
        if "m75" in text_lower:
            print("   ✓ Código M75 encontrado")
            pattern = r'.{0,300}m\s*75[^\s]*.{0,300}'
            matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
            for match in matches[:5]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
            print()
        
        # Buscar "lesión no especificada"
        if "no especificada" in text_lower or "inespecificada" in text_lower:
            print("   ✓ 'Lesión no especificada' encontrada")
            pattern = r'.{0,300}no\s+especificada.{0,300}'
            matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
            for match in matches[:3]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
            print()
        
        # Buscar "clase 1" o "deficiencia leve"
        if "clase 1" in text_lower or "clase i" in text_lower:
            print("   ✓ Clase 1 mencionada")
            pattern = r'.{0,300}clase\s+1.{0,300}'
            matches = list(re.finditer(pattern, full_text, re.IGNORECASE))
            for match in matches[:3]:
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"     ...{context}...")
            print()
        
        # Buscar sección RESUELVE o DISPOSITIVO
        print("=" * 80)
        print("SECCIÓN RESUELVE/DISPOSITIVO")
        print("=" * 80)
        print()
        
        pattern_resuelve = r'(?i)(resuelve|dispositivo|fallo).{0,1000}'
        matches = list(re.finditer(pattern_resuelve, full_text, re.DOTALL))
        if matches:
            for i, match in enumerate(matches, 1):
                context = match.group(0)
                context = re.sub(r'\s+', ' ', context)
                print(f"   {i}. {context[:800]}...")
                print()
        
        # Mostrar texto completo para análisis manual
        print("=" * 80)
        print("TEXTO COMPLETO DE LA RESOLUCIÓN")
        print("=" * 80)
        print()
        print(full_text)
        print()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    pdf_path = "../CopiaAutentica_NOTI GEMMA.pdf"
    if not Path(pdf_path).exists():
        pdf_path = "CopiaAutentica_NOTI GEMMA.pdf"
    
    asyncio.run(analyze_with_ocr(pdf_path))

