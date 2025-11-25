"""
Servicio de NLP para extracción de entidades y detección de tipo de documento
Versión mejorada y más estricta para evitar falsos positivos.
"""
import re
from typing import Dict, List, Optional


class NLPService:
    """Servicio para procesamiento de lenguaje natural"""
    
    def __init__(self):
        # Mapeo de abreviaciones médicas a nombres completos
        self.abbreviation_expansion = {
            "toc": "trastorno obsesivo-compulsivo",
            "tept": "trastorno de estrés postraumático",
            "hta": "hipertensión arterial",
            "epoc": "enfermedad pulmonar obstructiva crónica",
            "irc": "insuficiencia renal crónica",
            "erc": "enfermedad renal crónica",
            "hbp": "hiperplasia benigna de próstata",
            "sahs": "síndrome de apnea hipopnea del sueño",
            "eii": "enfermedad inflamatoria intestinal",
            "sii": "síndrome del intestino irritable",
            "dm": "diabetes mellitus",
            "acv": "accidente cerebrovascular",
        }
    
    async def detect_document_type(self, text: str) -> str:
        """
        Detecta el tipo de documento basándose en palabras clave
        
        Args:
            text: Texto del documento
        
        Returns:
            Tipo de documento: 'clinical', 'judicial', o 'administrative'
        """
        text_lower = text.lower()
        
        # Palabras clave para documentos judiciales
        judicial_keywords = [
            "sentencia", "juzgado", "tribunal", "magistrado", "juez",
            "hechos probados", "fundamentos de derecho", "fallo",
            "recurso", "apelación", "procedimiento", "sala de lo social",
            "contencioso-administrativo", "suplicación"
        ]
        
        # Palabras clave para documentos administrativos
        administrative_keywords = [
            "resolución", "administración", "director general", "secretario general",
            "determina que", "resuelve", "dispone", "anexo", "baremo",
            "grado de discapacidad", "reconocimiento del grado", "consejería de",
            "departamento de", "centro de valoración"
        ]
        
        # Palabras clave para documentos clínicos
        clinical_keywords = [
            "informe médico", "informe pericial", "diagnóstico", "exploración",
            "paciente", "historia clínica", "examen físico", "pruebas complementarias",
            "antecedentes personales", "enfermedad actual", "juicio clínico",
            "evolución", "tratamiento"
        ]
        
        # Contar ocurrencias
        judicial_count = sum(1 for keyword in judicial_keywords if keyword in text_lower)
        administrative_count = sum(1 for keyword in administrative_keywords if keyword in text_lower)
        clinical_count = sum(1 for keyword in clinical_keywords if keyword in text_lower)
        
        # Determinar tipo basado en el mayor conteo
        if judicial_count > administrative_count and judicial_count > clinical_count:
            return "judicial"
        elif administrative_count > clinical_count:
            return "administrative"
        else:
            return "clinical"
    
    async def extract_entities(self, text: str) -> Dict[str, List[Dict]]:
        """
        Extrae entidades del texto (diagnósticos, métricas, códigos, valoraciones)
        
        Args:
            text: Texto del documento
        
        Returns:
            Diccionario con entidades por tipo
        """
        entities = {
            "DIAGNOSIS": [],
            "METRIC": [],
            "CODE": [],
            "RATING": []
        }
        
        # ==============================================================================
        # LISTA BLANCA DE DIAGNÓSTICOS VÁLIDOS (Ampliada y más específica)
        # ==============================================================================
        # Esta es la fuente principal de verdad. Se prefieren diagnósticos completos.
        valid_diagnoses_whitelist = [
            # Sistema Musculoesquelético - Hombro
            r"rotura\s+(?:del|de la|de)\s+manguito\s+rotador",
            r"lesión\s+(?:del|de la|de)\s+manguito\s+rotador",
            r"tendinopatía\s+(?:del|de la|de)\s+manguito\s+rotador",
            r"tendinitis\s+(?:del|de la|de)\s+manguito\s+rotador",
            r"síndrome\s+(?:del|de la|de)\s+hombro\s+doloroso",
            r"capsulitis\s+adhesiva(?:\s+de\s+hombro)?",
            r"hombro\s+congelado",
            r"omalgia(?:\s+crónica)?",
            r"luxación\s+(?:del|de la|de)\s+hombro",
            r"luxación\s+acromioclavicular",
            r"artrosis\s+(?:del|de la|de)\s+hombro",
            r"artrosis\s+acromioclavicular",
            r"bursitis\s+subacromial",
            r"impingement\s+(?:subacromial|de hombro)",

            # Sistema Musculoesquelético - Codo, Muñeca, Mano
            r"epicondilitis",
            r"epitrocleitis",
            r"síndrome\s+del\s+túnel\s+carpiano",
            r"sindrome\s+del\s+tunel\s+carpiano",
            r"artrosis\s+(?:de|del)\s+codo",
            r"artrosis\s+(?:de|de la)\s+muñeca",
            r"rizartrosis",
            r"dedo\s+en\s+resorte",
            r"enfermedad\s+de\s+duputyren",

            # Sistema Musculoesquelético - Columna Vertebral
            r"cervicalgia(?:\s+crónica)?",
            r"dorsalgia(?:\s+crónica)?",
            r"lumbalgia(?:\s+crónica)?",
            r"lumbago",
            r"cervicobraquialgia",
            r"lumbociatalgia",
            r"ciática",
            r"hernia\s+discal\s+(?:cervical|dorsal|lumbar)",
            r"protrusión\s+discal\s+(?:cervical|dorsal|lumbar)",
            r"espondilosis\s+(?:cervical|dorsal|lumbar)",
            r"espondiloartrosis\s+(?:cervical|dorsal|lumbar)",
            r"estenosis\s+de\s+canal\s+(?:cervical|lumbar)",
            r"escoliosis",
            r"cifosis",
            r"lordosis",

            # Sistema Musculoesquelético - Cadera, Rodilla
            r"coxartrosis",
            r"artrosis\s+de\s+cadera",
            r"gonartrosis",
            r"artrosis\s+de\s+rodilla",
            r"rotura\s+de\s+menisco",
            r"rotura\s+de\s+ligamento\s+cruzado\s+(?:anterior|posterior)",
            r"condropatía\s+rotuliana",
            r"trocanteritis",

            # Sistema Musculoesquelético - Tobillo, Pie
            r"síndrome\s+del\s+tarso",
            r"sindrome\s+del\s+tarso",
            r"síndrome\s+del\s+seno\s+del\s+tarso",
            r"esguince\s+de\s+tobillo(?:\s+crónico)?",
            r"inestabilidad\s+de\s+tobillo",
            r"artrosis\s+de\s+tobillo",
            r"tendinopatía\s+de\s+aquiles",
            r"tendinitis\s+aquílea",
            r"fascitis\s+plantar",
            r"espolón\s+calcáneo",
            r"hallux\s+valgus",
            r"pie\s+plano",
            r"pie\s+cavo",
            r"metatarsalgia",

            # Sistema Musculoesquelético - General/Otros
            r"fibromialgia",
            r"síndrome\s+de\s+fatiga\s+crónica",
            r"osteoporosis",
            r"artritis\s+reumatoide",
            r"espondilitis\s+anquilosante",
            r"lupus\s+eritematoso\s+sistémico",
            r"polimialgia\s+reumática",
            r"contractura\s+muscular(?:\s+crónica)?",
            r"amiotrofia\s+muscular",
            r"discinesia\s+escapular",

            # Sistema Cardiovascular
            r"hipertensión\s+arterial",
            r"hta",
            r"insuficiencia\s+cardíaca",
            r"cardiopatía\s+isquémica",
            r"infarto\s+agudo\s+de\s+miocardio",
            r"angina\s+de\s+pecho",
            r"arritmia\s+cardíaca",
            r"fibrilación\s+auricular",
            r"valvulopatía",
            r"insuficiencia\s+venosa\s+crónica",
            r"varices",
            r"trombosis\s+venosa\s+profunda",
            r"arteriopatía\s+periférica",

            # Sistema Respiratorio
            r"epoc",
            r"enfermedad\s+pulmonar\s+obstructiva\s+crónica",
            r"asma\s+bronquial",
            r"síndrome\s+de\s+apnea\s+hipopnea\s+obstructiva\s+del\s+sueño",
            r"síndrome\s+de\s+apnea\s+hipopnea\s+del\s+sueño",
            r"sahs",
            r"apnea\s+del\s+sueño",

            # Sistema Nervioso
            r"accidente\s+cerebrovascular",
            r"ictus",
            r"epilepsia",
            r"migraña(?:\s+crónica)?",
            r"cefalea\s+tensional",
            r"esclerosis\s+múltiple",
            r"parkinson",
            r"alzheimer",
            r"neuropatía\s+periférica",
            r"radiculopatía",

            # Trastornos Mentales
            r"trastorno\s+depresivo(?:\s+mayor)?",
            r"depresión\s+mayor",
            r"distimia",
            r"trastorno\s+de\s+ansiedad(?:\s+generalizada)?",
            r"ansiedad\s+generalizada",
            r"síndrome\s+ansioso\s+depresivo",
            r"sindrome\s+ansioso\s+depresivo",
            r"trastorno\s+mixto\s+ansioso\s+depresivo",
            r"trastorno\s+de\s+estrés\s+postraumático",
            r"\btept\b",
            r"trastorno\s+obsesivo\s+compulsivo",
            r"\btoc\b",
            r"trastorno\s+bipolar",
            r"esquizofrenia",
            r"trastorno\s+de\s+la\s+personalidad",
            r"trastorno\s+adaptativo(?:\s+con\s+ansiedad)?",
            r"trastorno\s+adaptativo\s+con\s+ansiedad",

            # Sistema Digestivo
            r"enfermedad\s+por\s+reflujo\s+gastroesofágico",
            r"erge",
            r"gastritis\s+crónica",
            r"úlcera\s+péptica",
            r"enfermedad\s+inflamatoria\s+intestinal",
            r"enfermedad\s+de\s+crohn",
            r"colitis\s+ulcerosa",
            r"síndrome\s+del\s+intestino\s+irritable",
            r"colon\s+irritable",
            r"hepatopatía\s+crónica",
            r"cirrosis\s+hepática",

            # Sistema Endocrino y Metabólico
            r"diabetes\s+mellitus(?:\s+tipo\s+[12])?",
            r"hipotiroidismo",
            r"hipertiroidismo",
            r"obesidad(?:\s+mórbida)?",
            r"dislipemia",
            r"hipercolesterolemia",

            # Otros
            r"anemia\s+ferropénica",
            r"anemia\s+crónica",
            r"insuficiencia\s+renal\s+crónica",
            r"dermatitis\s+atópica",
            r"psoriasis",
            r"hipoacusia",
            r"vértigo",
            r"mareo\s+subjetivo\s+crónico",
            r"mareo\s+postural\s+perceptivo\s+persistente",
            r"vestibulopatía\s+bilateral(?:\s+no\s+compensada)?",
            r"cofosis",
            r"implante\s+coclear",
            r"acúfenos",
            r"tinnitus",
            r"glaucoma",
            r"cataratas",
            r"degeneración\s+macular",

        ]
        
        # Patrones más restrictivos para capturar diagnósticos después de palabras clave
        diagnosis_patterns = [
            # Solo después de palabras clave médicas específicas y delimitado
            r"(?:diagnóstico|diagnostico|juicio clínico|orientación diagnóstica)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]{5,100})(?:[\.;:\n]|$)",
            r"(?:patología|patologia|enfermedad)[\s:]+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]{5,100})(?:[\.;:\n]|$)",
            # Secciones de conclusiones o antecedentes
            r"(?:conclusiones|consideraciones médico-legales)[\s:](?:.|\n)*?presenta\s+([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,]{5,100})(?:[\.;:\n]|$)",
            # Hechos probados en sentencias (formato con guiones o numeración)
            r"(?:hechos\s+probados|cuadro\s+clínico|presenta\s+el\s+siguiente)[\s:](?:.|\n)*?[-•]\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,150})(?:[\.;:\n]|$)",
            r"(?:SEXTO|SÉPTIMO|OCTAVO|NOVENO|DÉCIMO)[\.-]+\s*(?:.|\n)*?[-•]\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,150})(?:[\.;:\n]|$)",
            # Listas con guiones o viñetas
            r"^[-•]\s*([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,150})(?:[\.;:\n]|$)",
            # Diagnósticos en hechos probados (formato narrativo)
            r"(?:hechos\s+probados|hecho\s+probado)[\s:](?:.|\n){0,500}?(?:diagnóstico|diagnostico|con\s+diagnóstico|con\s+diagnostico)[\s:]+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,100})(?:[\.;,\n]|$)",
            # Diagnósticos mencionados en contexto de incapacidad/enfermedad
            r"(?:incapacidad|enfermedad|proceso)[\s:]+(?:.|\n){0,200}?(?:diagnóstico|diagnostico|con\s+diagnóstico|con\s+diagnostico)[\s:]+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,100})(?:[\.;,\n]|$)",
        ]
        
        seen_diagnoses = set()
        
        # Palabras/frases que invalidan un diagnóstico (más exhaustivo)
        invalid_phrases = [
            "urgencias", "hospital", "clínica", "centro de salud", "consulta", 
            "doctor", "doctora", "dr.", "dra.", "colegiado", "especialista",
            "pendiente de", "nuevas consultas", "pruebas", "tratamiento",
            "limitaciones que", "las limitaciones", "que presentaba", "refiere",
            "declaración del perito", "informe", "valoración", "paciente",
            "trabajadora", "trabajador", "interesado", "solicitante",
            "fecha", "edad", "años", "profesión", "mecanismo", "evolución",
            "antecedentes", "historia", "exploración", "situación actual",
            "pronóstico", "secuelas", "en su caso", "posible", "probable",
            "descartar", "compatible con", "sugerente de",
            "baremo", "anexo", "capítulo", "artículo", "rd 888", "real decreto",
            "grado", "discapacidad", "deficiencia", "clase", "porcentaje",
            "cálculo", "fórmula", "combinación", "puntos",
            "de tipo", "tipo de", "tipo", "general", "ósea", "crónica",
            "sin", "no", "ausencia de", "normal", "conservada"
        ]
        
        # Patrones que invalidan un diagnóstico (al inicio)
        invalid_patterns = [
            r"^(?:el\s+|la\s+|los\s+|las\s+|un\s+|una\s+)?(?:paciente|trabajador|interesado|solicitante)",
            r"^(?:en\s+|a\s+|de\s+|con\s+|por\s+)?(?:fecha|edad|profesión|mecanismo|evolución)",
            r"^(?:se\s+)?(?:solicita|realiza|aprecia|observa|constata|refiere)",
            r"^(?:pendiente\s+de|compatible\s+con|sugerente\s+de|descartar)",
            r"^(?:sin|no\s+se\s+aprecia|ausencia\s+de|normal|conservada)",
            r"^(?:baremo|anexo|capítulo|artículo|rd\s*888|real\s+decreto)",
            r"^(?:grado|discapacidad|deficiencia|clase\s+\d|porcentaje)",
            r"^(?:cálculo|fórmula|combinación|puntos)",
            r"^(?:de\s+tipo|tipo\s+de|tipo|general|ósea|crónica)$",
            r"^[a-z]{1,3}$", # Palabras muy cortas
            r"^\d", # Empieza por número
        ]
        
        def is_valid_diagnosis(text: str) -> bool:
            """Verifica si un texto es un diagnóstico médico válido (versión estricta)"""
            text_lower = text.lower().strip()
            
            # 1. Longitud mínima y máxima
            if len(text) < 5 or len(text) > 150:
                return False
            
            # 2. Validar contra patrones inválidos al inicio
            for pattern in invalid_patterns:
                if re.match(pattern, text_lower, re.IGNORECASE):
                    return False
            
            # 3. Validar contra frases inválidas en cualquier parte
            for phrase in invalid_phrases:
                # Asegurar que la frase es una palabra completa o está delimitada
                if re.search(r'\b' + re.escape(phrase) + r'\b', text_lower):
                    return False
            
            # 4. Debe contener al menos un término médico fuerte de una lista predefinida
            # Esta lista debe ser muy específica de enfermedades, no de síntomas o anatomía general.
            strong_medical_terms = [
                "síndrome", "sindrome", "tendinopatía", "tendinopatia", "tendinitis",
                "artrosis", "artritis", "anemia", "hipertensión", "hipertension",
                "gastroduodenitis", "gastritis", "lumbociatalgia", "cervicobraquialgia",
                "cervicalgia", "dorsalgia", "lumbalgia", "ciática",
                "hernia", "protrusión", "espondilosis", "estenosis", "escoliosis",
                "rotura", "fractura", "luxación", "esguince", "bursitis", "capsulitis",
                "epicondilitis", "epitrocleitis", "neuropatía", "radiculopatía",
                "fibromialgia", "osteoporosis", "espondilitis",
                "insuficiencia", "cardiopatía", "infarto", "angina", "arritmia",
                "fibrilación", "valvulopatía", "varices", "trombosis", "arteriopatía",
                "epoc", "asma", "apnea",
                "ictus", "epilepsia", "migraña", "esclerosis", "parkinson", "alzheimer",
                "trastorno", "depresión", "depresion", "ansiedad", "distimia",
                "esquizofrenia", "bipolar",
                "diabetes", "hipotiroidismo", "hipertiroidismo", "obesidad", "dislipemia",
                "dermatitis", "psoriasis", "hipoacusia", "vértigo", "mareo", "vestibulopatía",
                "cofosis", "implante", "coclear", "glaucoma", "cataratas",
                "limitación", "movilidad", "adaptativo"
            ]
            
            # También permitir diagnósticos que mencionan dolor/síntoma + parte del cuerpo
            # Ejemplo: "Dolor en el tobillo", "Dolor lumbar", etc.
            symptom_body_pattern = r"(?:dolor|dolores|limitación|limitaciones|deficiencia|deficiencias|lesión|lesiones)\s+(?:en|de|del|de la|del|en el|en la)\s+(?:el|la|los|las)?\s*(?:hombro|codo|muñeca|mano|dedo|cadera|rodilla|tobillo|pie|tarso|cervical|dorsal|lumbar|columna)"
            
            has_strong_term = any(re.search(r'\b' + re.escape(term) + r'\b', text_lower) for term in strong_medical_terms)
            has_symptom_body = bool(re.search(symptom_body_pattern, text_lower, re.IGNORECASE))
            
            if not has_strong_term and not has_symptom_body:
                return False
            
            # 5. No debe ser solo una palabra anatómica o vaga (pero permitir si tiene contexto)
            vague_single_words = ["lumbar", "cervical", "dorsal", "ósea", "osea", "óseo", "oseo",
                                "psiquiátrico", "psiquiatrico", "psiquiátrica", "psiquiatrica",
                                "crónico", "cronico", "crónica", "cronica", "tipo", "general",
                                "hombro", "codo", "muñeca", "mano", "cadera", "rodilla", "tobillo", "pie"]
            # Permitir si tiene más contexto (más de una palabra) o si está en formato de lista (hechos probados)
            if len(text.split()) == 1 and text_lower in vague_single_words:
                return False
            
            # 6. Permitir diagnósticos que empiezan con mayúscula en formato de lista (hechos probados)
            # Estos suelen ser más confiables
            if text[0].isupper() and len(text.split()) >= 2:
                # Si tiene al menos un término médico fuerte, es válido
                return True

            return True
        
        # --- ESTRATEGIA 0: Buscar diagnósticos en formato de lista (hechos probados) ---
        # Detectar listas con guiones o viñetas que contienen diagnósticos
        list_pattern = r"(?:^|\n)\s*[-•]\s*([A-ZÁÉÍÓÚÑ][^\.\n]{10,150})(?:\.|$|\n)"
        list_matches = re.finditer(list_pattern, text, re.MULTILINE)
        for match in list_matches:
            diagnosis_text = match.group(1).strip()
            
            # Limpiar el texto (quitar paréntesis con fechas, etc.)
            diagnosis_text = re.sub(r'\s*\([^)]*\)\s*', '', diagnosis_text).strip()
            
            # Validar que sea un diagnóstico válido
            if is_valid_diagnosis(diagnosis_text):
                normalized = re.sub(r'\s+', ' ', diagnosis_text.lower())
                if normalized not in seen_diagnoses:
                    seen_diagnoses.add(normalized)
                    entities["DIAGNOSIS"].append({
                        "text": diagnosis_text,
                        "start": match.start(1),
                        "end": match.end(1),
                        "source": "hechos_probados"
                    })
        
        # --- ESTRATEGIA 0.5: Buscar diagnósticos en hechos probados (formato narrativo) ---
        # Ejemplo: "con diagnóstico de Dolor en el tobillo"
        hechos_narrativo_patterns = [
            r"(?:con\s+diagnóstico|diagnóstico|diagnostico)[\s:]+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,100})(?:[\.;,\n]|$)",
            r"(?:proceso|enfermedad|incapacidad)[\s:]+(?:.|\n){0,100}?(?:con\s+diagnóstico|diagnóstico|diagnostico)[\s:]+(?:de\s+)?([A-ZÁÉÍÓÚÑ][a-záéíóúñ\s,()0-9]{5,100})(?:[\.;,\n]|$)",
        ]
        
        for pattern in hechos_narrativo_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                diagnosis_text = match.group(1).strip() if match.lastindex else match.group(0).strip()
                
                # Limpiar el texto - cortar en frases que indican fin del diagnóstico
                # Ejemplo: "Dolor en el tobillo, en relación al cual" -> "Dolor en el tobillo"
                cutoff_phrases = [
                    r",\s*en\s+relaci[óo]n\s+al\s+cual",
                    r",\s*en\s+relaci[óo]n\s+con",
                    r",\s*por\s+el\s+cual",
                    r",\s*por\s+lo\s+cual",
                    r",\s*siendo",
                    r",\s*que\s+",
                    r",\s*el\s+cual",
                    r",\s*la\s+cual",
                ]
                
                for cutoff in cutoff_phrases:
                    diagnosis_text = re.split(cutoff, diagnosis_text, flags=re.IGNORECASE)[0].strip()
                
                # Limpiar el texto
                diagnosis_text = diagnosis_text.rstrip('.,;:')
                diagnosis_text = re.sub(r'^[a-z]{1,4}[,\s]+', '', diagnosis_text, flags=re.IGNORECASE)
                diagnosis_text = diagnosis_text.strip()
                
                # Validar que sea un diagnóstico válido
                if is_valid_diagnosis(diagnosis_text):
                    normalized = re.sub(r'\s+', ' ', diagnosis_text.lower())
                    if normalized not in seen_diagnoses:
                        seen_diagnoses.add(normalized)
                        entities["DIAGNOSIS"].append({
                            "text": diagnosis_text,
                            "start": match.start(1) if match.lastindex else match.start(),
                            "end": match.start(1) + len(diagnosis_text) if match.lastindex else match.start() + len(diagnosis_text),
                            "source": "hechos_probados_narrativo"
                        })
        
        # --- ESTRATEGIA 1: Buscar diagnósticos de la LISTA BLANCA (Prioridad Alta) ---
        for pattern in valid_diagnoses_whitelist:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                diagnosis_text = match.group(0).strip()
                
                # Expandir abreviaciones a nombres completos
                diagnosis_text_lower = diagnosis_text.lower()
                if diagnosis_text_lower in self.abbreviation_expansion:
                    diagnosis_text = self.abbreviation_expansion[diagnosis_text_lower]
                
                # Normalizar y verificar duplicados
                normalized = re.sub(r'\s+', ' ', diagnosis_text.lower())
                if normalized in seen_diagnoses:
                    continue
                
                seen_diagnoses.add(normalized)
                entities["DIAGNOSIS"].append({
                    "text": diagnosis_text,
                    "start": match.start(),
                    "end": match.end(),
                    "source": "whitelist" # Indicar origen
                })
        
        # --- ESTRATEGIA 2: Buscar diagnósticos con patrones genéricos (Prioridad Media) ---
        for pattern in diagnosis_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                diagnosis_text = match.group(1).strip() if match.lastindex else match.group(0).strip()
                
                # Limpieza del texto extraído
                diagnosis_text = diagnosis_text.rstrip('.,;:')
                diagnosis_text = re.sub(r'^[a-z]{1,4}[,\s]+', '', diagnosis_text, flags=re.IGNORECASE)
                diagnosis_text = re.sub(r'\s+(?:y|e|o|u|con)\s*$', '', diagnosis_text, flags=re.IGNORECASE) # Eliminar conjunciones al final
                diagnosis_text = diagnosis_text.strip()
                
                # Validar estrictamente
                if not is_valid_diagnosis(diagnosis_text):
                    continue
                
                # Normalizar y verificar duplicados
                normalized = re.sub(r'\s+', ' ', diagnosis_text.lower())
                if normalized in seen_diagnoses:
                    continue
                
                # Separar diagnósticos combinados (más robusto)
                # Busca patrones como: "Diag1, Diag2 y Diag3"
                parts = re.split(r'(?:,\s*|\s+y\s+|\s+e\s+)', diagnosis_text)
                
                if len(parts) > 1:
                    current_start = match.start()
                    if match.lastindex:
                        current_start = match.start(1)
                        
                    for part in parts:
                        part = part.strip()
                        if not part: continue
                        
                        # Validar cada parte individualmente
                        if is_valid_diagnosis(part):
                            part_normalized = re.sub(r'\s+', ' ', part.lower())
                            if part_normalized not in seen_diagnoses:
                                seen_diagnoses.add(part_normalized)
                                
                                # Calcular posición aproximada (puede no ser exacta)
                                part_start = text.find(part, current_start)
                                if part_start != -1:
                                    entities["DIAGNOSIS"].append({
                                        "text": part,
                                        "start": part_start,
                                        "end": part_start + len(part),
                                        "source": "pattern_split"
                                    })
                                    current_start = part_start + len(part)
                else:
                    # Si no se pudo separar, agregar el diagnóstico completo si es válido
                    seen_diagnoses.add(normalized)
                    entities["DIAGNOSIS"].append({
                        "text": diagnosis_text,
                        "start": match.start(1) if match.lastindex else match.start(),
                        "end": match.end(1) if match.lastindex else match.end(),
                        "source": "pattern"
                    })
        
        # Extraer métricas (grados, porcentajes)
        metric_patterns = [
            r"(\d+(?:\.\d+)?)\s*°\s*(?:de\s+)?(?:abducción|flexión|extensión|rotación|balance\s+articular|movilidad)",
            r"(?:abducción|flexión|extensión|rotación|balance\s+articular|movilidad)[\s:]+(\d+(?:\.\d+)?)\s*°",
            r"(\d+(?:\.\d+)?)\s*%\s*(?:de\s+)?(?:pérdida|déficit|limitación)",
            r"(?:balance\s+muscular)[\s:]+(\d)(?:/5)?", # Balance muscular (ej: 2/5)
        ]
        
        metric_types = {
            "abducción": "abduccion",
            "flexión": "flexion",
            "extensión": "extension",
            "rotación": "rotacion",
            "balance articular": "rom_global",
            "movilidad": "rom_global",
            "balance muscular": "fuerza"
        }
        
        for pattern in metric_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match.group(1))
                except ValueError:
                    continue # Si no es un número válido
                    
                metric_text = match.group(0)
                metric_type = None
                
                # Determinar tipo de métrica
                for key, val in metric_types.items():
                    if key in metric_text.lower():
                        metric_type = val
                        break
                
                # Si es porcentaje de pérdida, se puede guardar como un tipo especial
                if "%" in metric_text and not metric_type:
                    metric_type = "perdida_funcional"
                
                if metric_type:
                    entities["METRIC"].append({
                        "text": metric_text,
                        "value": value,
                        "type": metric_type,
                        "start": match.start(),
                        "end": match.end()
                    })
        
        # Extraer códigos (CIE-10)
        code_patterns = [
            r"(?:CIE[- ]?10|CIE10|Código)[\s:]+([A-Z]\d{2}(?:\.\d{1,2})?)",
            r"([A-Z]\d{2}(?:\.\d{1,2})?)\s*(?:CIE|CIE-10)",
        ]
        
        for pattern in code_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                code_text = match.group(1)
                entities["CODE"].append({
                    "text": code_text,
                    "start": match.start(),
                    "end": match.end()
                })
        
        # Extraer valoraciones (porcentajes de discapacidad ya otorgados)
        rating_patterns = [
            r"(?:grado|porcentaje|valoración)[\s:]+(?:de\s+)?(?:discapacidad|minusvalía)?[\s:]+(\d+(?:\.\d+)?)\s*%",
            r"(\d+(?:\.\d+)?)\s*%\s*(?:de\s+)?(?:discapacidad|minusvalía|deficiencia\s+global)",
            r"(?:reconocimiento|reconocido|tiene\s+reconocido)[\s:]+(?:por\s+)?(?:la\s+)?(?:Junta|Administración|Gobierno)?[\s:]+(?:un\s+)?(?:grado|porcentaje)[\s:]+(?:de\s+)?(?:discapacidad|minusvalía)[\s:]+(?:del\s+)?(\d+(?:\.\d+)?)\s*%",
            r"(?:grado\s+de\s+discapacidad\s+del\s+)(\d+(?:\.\d+)?)\s*%",
            r"baremo\s+(\d+(?:\.\d+)?)",
            # Movilidad reducida
            r"(?:movilidad\s+reducida|movilidad\s+valorada)[\s:]+(?:en\s+)?(\d+(?:\.\d+)?)\s*(?:puntos?|%)",
            # Situación de dependencia
            r"(?:situación\s+de\s+dependencia|grado\s+de\s+dependencia)[\s:]+(?:en\s+)?(?:grado\s+)?(\d+)",
        ]
        
        for pattern in rating_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    value = float(match.group(1))
                except ValueError:
                    continue
                    
                rating_text = match.group(0)
                entities["RATING"].append({
                    "text": rating_text,
                    "value": value,
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities
