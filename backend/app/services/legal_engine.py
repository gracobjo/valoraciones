"""
Motor de análisis legal basado en RD 888/2022
Genera valoraciones por capítulo y valoración final (GDA)
Versión corregida para usar Valores Iniciales de Ajuste (VIA) y mejorar la agrupación.
"""
import re
from typing import Dict, List, Optional, Any
import statistics


class LegalEngine:
    """Motor para análisis legal y valoración según RD 888/2022"""
    
    def __init__(self):
        # Mapeo de sistemas corporales a capítulos del RD 888/2022, Anexo III
        # Se han ampliado las palabras clave y patrones para una mejor detección.
        self.system_patterns = {
            "2": { # Sistema Nervioso
                "keywords": ["neurología", "neurológico", "cerebro", "encefalopatía", "ictus", "accidente cerebrovascular",
                             "acv", "epilepsia", "convulsiones", "migraña", "cefalea", "esclerosis múltiple", "parkinson",
                             "alzheimer", "demencia", "neuropatía", "polineuropatía", "radiculopatía", "nervio",
                             "parálisis", "paresia", "espasticidad", "ataxia", "temblor", "deterioro cognitivo"],
                "patterns": [r"neurol[óo]gico", r"encefalopat[íi]a", r"epilepsia", r"migraña", r"cefalea",
                             r"esclerosis", r"parkinson", r"alzheimer", r"demencia", r"neuropat[íi]a",
                             r"radiculopat[íi]a", r"par[áa]lisis", r"paresia", r"espasticidad", r"ataxia",
                             r"deterioro cognitivo"]
            },
            "3": { # Sistema Nervioso (continuación - funciones mentales superiores)
                 # A menudo se valora junto con el Cap. 2 o 15, dependiendo del origen.
                 # Por simplicidad, lo agrupamos aquí con patrones similares al 2 y 15.
                 "keywords": ["funciones mentales superiores", "memoria", "atención", "lenguaje", "praxias", "gnosias",
                              "funciones ejecutivas", "deterioro cognitivo leve"],
                 "patterns": [r"funciones mentales", r"memoria", r"atención", r"lenguaje", r"praxias", r"gnosias",
                              r"funciones ejecutivas", r"deterioro cognitivo leve"]
            },
            "4": {  # Sistema Cardiovascular
                "keywords": ["cardiología", "cardiológico", "corazón", "cardíaco", "vascular", "arterial", "venoso",
                             "hipertensión arterial", "hta", "insuficiencia cardíaca", "ic", "cardiopatía isquémica",
                             "infarto agudo de miocardio", "iam", "angina de pecho", "arritmia", "fibrilación auricular",
                             "fa", "valvulopatía", "estenosis valvular", "insuficiencia valvular", "insuficiencia venosa crónica",
                             "ivc", "varices", "trombosis venosa profunda", "tvp", "arteriopatía periférica", "claudicación intermitente"],
                "patterns": [r"cardiol[óo]gico", r"card[íi]aco", r"vascular", r"hipertensi[óo]n", r"hta",
                             r"insuficiencia card[íi]aca", r"cardiopat[íi]a", r"infarto", r"angina", r"arritmia",
                             r"fibrilaci[óo]n auricular", r"valvulopat[íi]a", r"insuficiencia venosa", r"varices",
                             r"trombosis", r"arteriopat[íi]a"]
            },
            "5": { # Sistema Respiratorio
                "keywords": ["neumología", "respiratorio", "pulmón", "pulmonar", "bronquios", "bronquial",
                             "epoc", "enfermedad pulmonar obstructiva crónica", "asma bronquial", "asma",
                             "síndrome de apnea hipopnea del sueño", "sahs", "apnea del sueño", "insuficiencia respiratoria",
                             "disnea", "fibrosis pulmonar", "bronquiectasias"],
                "patterns": [r"neumol[óo]gía", r"respiratorio", r"pulmonar", r"bronquial", r"epoc", r"asma",
                             r"apnea del sueño", r"sahs", r"insuficiencia respiratoria", r"disnea", r"fibrosis pulmonar"]
            },
            "6": {  # Sistema Endocrino
                "keywords": ["endocrinología", "endocrino", "hormonal", "metabolismo", "metabólico",
                             "diabetes mellitus", "diabetes", "dm", "tiroides", "tiroideo", "hipotiroidismo",
                             "hipertiroidismo", "bocio", "nódulo tiroideo", "obesidad mórbida", "obesidad",
                             "dislipemia", "hipercolesterolemia", "hipertrigliceridemia", "síndrome metabólico"],
                "patterns": [r"endocrinol[óo]gía", r"endocrino", r"hormonal", r"metab[óo]lico", r"diabetes",
                             r"tiroides", r"tiroideo", r"hipotiroidismo", r"hipertiroidismo", r"obesidad",
                             r"dislipemia", r"hipercolesterolemia"]
            },
             "7": { # Sistema Genitourinario
                 "keywords": ["urología", "urológico", "nefrología", "nefrológico", "renal", "riñón", "urinario",
                              "vejiga", "próstata", "genital", "insuficiencia renal crónica", "irc", "enfermedad renal crónica",
                              "erc", "diálisis", "trasplante renal", "incontinencia urinaria", "vejiga neurógena",
                              "hiperplasia benigna de próstata", "hbp", "cáncer de próstata", "cáncer renal", "cáncer de vejiga",
                              "disfunción eréctil", "infertilidad"],
                 "patterns": [r"urol[óo]gico", r"nefrol[óo]gico", r"renal", r"urinario", r"insuficiencia renal",
                              r"enfermedad renal", r"diálisis", r"trasplante renal", r"incontinencia urinaria",
                              r"vejiga neur[óo]gena", r"pr[óo]stata", r"disfunci[óo]n eréctil"]
             },
            "8": {  # Sistema Musculoesquelético
                "keywords": ["traumatología", "reumatología", "musculoesquelético", "osteoarticular", "hueso", "óseo",
                             "articulación", "articular", "músculo", "muscular", "tendón", "tendinoso", "ligamento",
                             "columna vertebral", "cervical", "dorsal", "lumbar", "sacro", "cóccix",
                             "hombro", "codo", "muñeca", "mano", "dedo", "cadera", "rodilla", "tobillo", "pie", "tarso",
                             "artrosis", "osteoartritis", "artritis", "artritis reumatoide", "espondilitis anquilosante",
                             "fibromialgia", "síndrome de fatiga crónica", "osteoporosis", "fractura", "luxación",
                             "esguince", "rotura muscular", "rotura tendinosa", "rotura ligamentosa", "lesión meniscal",
                             "tendinopatía", "tendinitis", "bursitis", "capsulitis", "sinovitis", "hernia discal",
                             "protrusión discal", "espondilosis", "espondiloartrosis", "estenosis de canal",
                             "escoliosis", "cifosis", "lordosis", "cervicalgia", "dorsalgia", "lumbalgia",
                             "lumbago", "cervicobraquialgia", "lumbociatalgia", "ciática", "síndrome del túnel carpiano",
                             "epicondilitis", "epitrocleitis", "fascitis plantar", "espolón calcáneo", "hallux valgus",
                             "pie plano", "pie cavo", "metatarsalgia", "síndrome del tarso", "prótesis", "artroplastia"],
                "patterns": [r"traumatol[óo]gía", r"reumatol[óo]gía", r"musculoesquel[eé]tico", r"osteoarticular",
                             r"[óo]se[ao]", r"articulaci[óo]n", r"articular", r"muscular", r"tendinoso",
                             r"columna", r"cervical", r"dorsal", r"lumbar", r"hombro", r"codo", r"muñeca",
                             r"cadera", r"rodilla", r"tobillo", r"tarso", r"artrosis", r"artritis",
                             r"fibromialgia", r"osteoporosis", r"fractura", r"luxaci[óo]n", r"esguince",
                             r"rotura", r"lesi[óo]n", r"tendinopat[íi]a", r"tendinitis", r"bursitis",
                             r"capsulitis", r"hernia discal", r"protrusi[óo]n", r"espondilosis",
                             r"espondiloartrosis", r"estenosis", r"escoliosis", r"cifosis", r"lordosis",
                             r"cervicalgia", r"dorsalgia", r"lumbalgia", r"lumbago", r"cervicobraquialgia",
                             r"lumbociatalgia", r"ci[áa]tica", r"t[úu]nel carpiano", r"epicondilitis",
                             r"epitrocleitis", r"fascitis plantar", r"espol[óo]n calcáneo", r"hallux valgus",
                             r"pie plano", r"pie cavo", r"metatarsalgia", r"s[íi]ndrome del tarso",
                             r"pr[óo]tesis", r"artroplastia"]
            },
            "9": {  # Sistema Hematológico
                "keywords": ["hematología", "hematológico", "sangre", "células sanguíneas", "glóbulos rojos",
                             "glóbulos blancos", "plaquetas", "hemoglobina", "hematocrito", "anemia",
                             "anemia ferropénica", "anemia megaloblástica", "anemia hemolítica", "leucopenia",
                             "neutropenia", "trombocitopenia", "pancitopenia", "leucemia", "linfoma", "mieloma múltiple",
                             "síndrome mielodisplásico", "coagulación", "trastorno de la coagulación", "hemofilia",
                             "trombofilia", "anticoagulación"],
                "patterns": [r"hematol[óo]gico", r"sangre", r"hemoglobina", r"anemia", r"leucopenia",
                             r"trombocitopenia", r"pancitopenia", r"leucemia", r"linfoma", r"mieloma",
                             r"coagulaci[óo]n", r"hemofilia", r"trombofilia"]
            },
            "10": {  # Sistema Digestivo
                "keywords": ["aparato digestivo", "digestivo", "gastrointestinal", "esófago", "estómago", "intestino",
                             "colon", "recto", "ano", "hígado", "vías biliares", "páncreas",
                             "enfermedad por reflujo gastroesofágico", "erge", "hernia de hiato", "gastritis",
                             "úlcera péptica", "úlcera gástrica", "úlcera duodenal", "infección por helicobacter pylori",
                             "enfermedad inflamatoria intestinal", "eii", "enfermedad de crohn", "colitis ulcerosa",
                             "síndrome del intestino irritable", "sii", "colon irritable", "estreñimiento crónico",
                             "diarrea crónica", "incontinencia fecal", "hepatopatía crónica", "cirrosis hepática",
                             "hepatitis crónica", "esteatosis hepática", "insuficiencia hepática", "litiasis biliar",
                             "colelitiasis", "pancreatitis crónica"],
                "patterns": [r"digestivo", r"gastrointestinal", r"es[óo]fago", r"est[óo]mago", r"intestino",
                             r"colon", r"h[íi]gado", r"p[áa]ncreas", r"reflujo gastroesof[áa]gico", r"erge",
                             r"gastritis", r"[úu]lcera", r"helicobacter pylori", r"enfermedad inflamatoria intestinal",
                             r"enfermedad de crohn", r"colitis ulcerosa", r"intestino irritable", r"colon irritable",
                             r"hepatopat[íi]a", r"cirrosis", r"hepatitis", r"esteatosis", r"insuficiencia hep[áa]tica",
                             r"litiasis biliar", r"colelitiasis", r"pancreatitis"]
            },
            # Capítulos 11, 12, 13, 14 se omiten por brevedad, pero seguirían la misma lógica.
            "15": {  # Trastornos Mentales
                "keywords": ["psiquiatría", "psiquiátrico", "psicología", "psicológico", "salud mental", "trastorno mental",
                             "enfermedad mental", "trastorno del estado de ánimo", "depresión", "trastorno depresivo",
                             "distimia", "trastorno bipolar", "manía", "hipomanía", "trastorno de ansiedad",
                             "ansiedad generalizada", "crisis de ansiedad", "ataque de pánico", "fobia", "agorafobia",
                             "trastorno obsesivo-compulsivo", "toc", "trastorno de estrés postraumático", "tept",
                             "trastorno de adaptación", "síndrome ansioso-depresivo", "trastorno mixto ansioso-depresivo",
                             "esquizofrenia", "trastorno esquizoafectivo", "trastorno delirante", "psicosis",
                             "trastorno de la personalidad", "trastorno de la conducta alimentaria", "anorexia nerviosa",
                             "bulimia nerviosa", "adicción", "trastorno por uso de sustancias", "alcoholismo", "drogodependencia"],
                "patterns": [r"psiqui[áa]trico", r"psicol[óo]gico", r"salud mental", r"trastorno mental",
                             r"depresi[óo]n", r"depresivo", r"distimia", r"bipolar", r"man[íi]a", r"ansiedad",
                             r"p[áa]nico", r"fobia", r"obsesivo-compulsivo", r"toc", r"estr[é]s postraum[áa]tico",
                             r"tept", r"adaptaci[óo]n", r"ansioso-depresivo", r"esquizofrenia", r"psicosis",
                             r"personalidad", r"conducta alimentaria", r"anorexia", r"bulimia", r"adicci[óo]n",
                             r"alcoholismo", r"drogodependencia"]
            }
        }
        
        # Definición de Clases y Valores Iniciales de Ajuste (VIA) según Anexo I del RD 888/2022
        # El VIA es el punto medio del rango de la clase.
        self.classes_via = {
            "0": {"range": (0, 4), "via": 0, "description": "Sin deficiencia"},
            "1": {"range": (5, 24), "via": 15, "description": "Deficiencia leve"},
            "2": {"range": (25, 49), "via": 37, "description": "Deficiencia moderada"},
            "3": {"range": (50, 70), "via": 60, "description": "Deficiencia grave"},
            "4": {"range": (71, 100), "via": 85, "description": "Deficiencia muy grave"}
        }

        # Definición de rangos de movilidad (ROM) para el Capítulo 8 (Sistema Musculoesquelético)
        # Estos valores son orientativos y deben ajustarse a las tablas específicas del Anexo III.
        # Se definen umbrales para clasificar la severidad de la limitación.
        self.rom_thresholds = {
            # Hombro (Flexión/Abducción) - Rangos aproximados basados en tablas 8.1 y 8.2
            "hombro": {"flexion_abduccion": {
                "leve": (121, 179),       # Clase 1
                "moderado": (61, 120),    # Clase 2
                "grave": (31, 60),        # Clase 3
                "muy_grave": (0, 30)      # Clase 4
            }},
            # Codo (Flexión/Extensión) - Rangos aproximados
            "codo": {"flexion_extension": {
                "leve": (111, 139),
                "moderado": (61, 110),
                "grave": (31, 60),
                "muy_grave": (0, 30)
            }},
            # Muñeca (Flexión/Extensión) - Rangos aproximados
            "muñeca": {"flexion_extension": {
                "leve": (51, 69),
                "moderado": (31, 50),
                "grave": (11, 30),
                "muy_grave": (0, 10)
            }},
             # Cadera (Flexión) - Rangos aproximados
            "cadera": {"flexion": {
                "leve": (81, 109),
                "moderado": (51, 80),
                "grave": (31, 50),
                "muy_grave": (0, 30)
            }},
            # Rodilla (Flexión) - Rangos aproximados
            "rodilla": {"flexion": {
                "leve": (91, 119),
                "moderado": (61, 90),
                "grave": (31, 60),
                "muy_grave": (0, 30)
            }},
            # Tobillo (Flexión dorsal/plantar) - Rangos aproximados
            "tobillo": {"flexion_extension": {
                "leve": (31, 49),
                "moderado": (16, 30),
                "grave": (6, 15),
                "muy_grave": (0, 5)
            }},
        }
    
    async def analyze(self, entities: Dict[str, List[Dict]], doc_type: str) -> Dict[str, Any]:
        """
        Analiza las entidades y genera valoraciones legales
        
        Args:
            entities: Diccionario con entidades extraídas
            doc_type: Tipo de documento
        
        Returns:
            Diccionario con análisis legal completo
        """
        # Obtener diagnósticos y métricas
        diagnoses = entities.get("DIAGNOSIS", [])
        metrics = entities.get("METRIC", [])
        
        # 1. Deduplicar diagnósticos
        unique_diagnoses = self._deduplicate_diagnoses(diagnoses)
        
        # 2. Agrupar patologías relacionadas
        grouped_diagnoses = self._group_related_pathologies(unique_diagnoses)
        
        # 3. Extraer métricas detectadas
        detected_metrics = self._extract_metrics(metrics)
        
        # 4. Generar valoraciones por capítulo
        chapter_valuations = []
        for diag in grouped_diagnoses:
            valuation = self._classify_diagnosis(diag, detected_metrics)
            if valuation:
                chapter_valuations.append(valuation)
        
        # 5. Calcular valoración final (GDA)
        final_valuation = self._calculate_final_valuation(chapter_valuations)
        
        # 6. Clasificación sugerida (para el frontend)
        suggested_classification = None
        if final_valuation:
            suggested_classification = {
                "class_number": final_valuation.get("final_class", "N/A"),
                "suggested_percentage": final_valuation.get("gda_percentage", 0),
                "description": final_valuation.get("description", "N/A"),
                "legal_basis": final_valuation.get("legal_basis", "RD 888/2022"),
                "confidence": final_valuation.get("confidence", 0.5)
            }
        
        return {
            "detected_diagnoses": grouped_diagnoses, # Devolver los diagnósticos ya agrupados
            "detected_metrics": detected_metrics,
            "chapter_valuations": chapter_valuations,
            "final_valuation": final_valuation,
            "suggested_classification": suggested_classification,
            "confidence": final_valuation.get("confidence", 0.5) if final_valuation else 0.0,
            "legal_basis": "RD 888/2022"
        }
    
    def _normalize_text(self, text: str) -> str:
        """Normaliza texto eliminando palabras comunes, puntuación y espacios extra"""
        if not text: return ""
        # Convertir a minúsculas
        text = text.lower().strip()
        # Eliminar puntuación
        text = re.sub(r'[^\w\s]', '', text)
        # Eliminar palabras comunes irrelevantes para la comparación semántica
        stop_words = ['de', 'del', 'la', 'el', 'los', 'las', 'un', 'una', 'unos', 'unas', 'y', 'o', 'a', 'en', 'por', 'para', 'con', 'sin', 'su', 'sus', 'al', 'crónico', 'crónica', 'bilateral', 'derecho', 'derecha', 'izquierdo', 'izquierda']
        words = text.split()
        significant_words = [w for w in words if w not in stop_words]
        # Unir y eliminar espacios múltiples
        normalized = ' '.join(significant_words)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized

    def _calculate_similarity(self, text1: str, text2: str) -> float:
        """Calcula la similitud entre dos textos normalizados usando el coeficiente de Jaccard"""
        set1 = set(text1.split())
        set2 = set(text2.split())
        if not set1 or not set2: return 0.0
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union > 0 else 0.0

    def _deduplicate_diagnoses(self, diagnoses: List[Dict]) -> List[Dict]:
        """
        Elimina diagnósticos duplicados y semánticamente muy similares.
        Utiliza normalización de texto y coeficiente de Jaccard.
        Mejorado para detectar sinónimos médicos (ej: "rotura" vs "lesión").
        """
        if not diagnoses: return []
        
        unique = []
        seen_normalized = []
        
        # Sinónimos médicos comunes (palabras que significan lo mismo en contexto médico)
        medical_synonyms = {
            "rotura": ["lesión", "ruptura", "desgarro"],
            "lesión": ["rotura", "ruptura", "desgarro"],
            "tendinopatía": ["tendinitis", "tendinosis"],
            "tendinitis": ["tendinopatía", "tendinosis"],
            "artrosis": ["osteoartritis", "artrosis degenerativa"],
            "hernia": ["protrusión", "prolapso"],
            "protrusión": ["hernia", "prolapso"]
        }
        
        def normalize_with_synonyms(text: str) -> str:
            """Normaliza texto reemplazando sinónimos por un término canónico"""
            normalized = self._normalize_text(text)
            words = normalized.split()
            # Reemplazar sinónimos por el término canónico (el primero de cada grupo)
            canonical_words = []
            for word in words:
                replaced = False
                for canonical, synonyms in medical_synonyms.items():
                    if word == canonical or word in synonyms:
                        canonical_words.append(canonical)
                        replaced = True
                        break
                if not replaced:
                    canonical_words.append(word)
            return ' '.join(canonical_words)
        
        # Ordenar por longitud de texto (preferir diagnósticos más largos/específicos)
        sorted_diagnoses = sorted(diagnoses, key=lambda x: len(x.get("text", "")), reverse=True)
        
        for diag in sorted_diagnoses:
            original_text = diag.get("text", "").strip()
            if not original_text: continue
            
            normalized_text = self._normalize_text(original_text)
            if not normalized_text: continue
            
            # Normalizar con sinónimos para comparación
            normalized_with_synonyms = normalize_with_synonyms(original_text)

            is_duplicate = False
            for seen_text in seen_normalized:
                # Si el texto normalizado es idéntico, es duplicado
                if normalized_text == seen_text:
                    is_duplicate = True
                    break
                
                # Comparar con sinónimos normalizados
                seen_normalized_with_synonyms = normalize_with_synonyms(seen_text)
                if normalized_with_synonyms == seen_normalized_with_synonyms:
                    is_duplicate = True
                    break
                
                # Si uno está contenido en el otro (ej: "lumbalgia" en "lumbalgia crónica")
                if normalized_text in seen_text or seen_text in normalized_text:
                     # Asegurar que no sea una coincidencia parcial de palabras cortas
                     if len(normalized_text.split()) > 1 and len(seen_text.split()) > 1:
                        is_duplicate = True
                        break

                # Calcular similitud de Jaccard para variaciones (ej: "hernia discal L5-S1" vs "hernia de disco lumbar")
                similarity = self._calculate_similarity(normalized_text, seen_text)
                if similarity >= 0.75: # Umbral de similitud alto
                    is_duplicate = True
                    break
                
                # Comparar también con sinónimos normalizados
                similarity_synonyms = self._calculate_similarity(normalized_with_synonyms, seen_normalized_with_synonyms)
                if similarity_synonyms >= 0.75:
                    is_duplicate = True
                    break
            
            if is_duplicate: continue
            
            seen_normalized.append(normalized_text)
            
            # Determinar información adicional
            body_part = self._extract_body_part(original_text)
            chapter = self._determine_chapter(original_text)
            
            unique.append({
                "text": original_text,
                "normalized_text": normalized_text, # Guardar para uso posterior
                "body_part": body_part,
                "chapter": chapter,
                "start": diag.get("start"),
                "end": diag.get("end"),
                "source": diag.get("source")
            })
            
        return unique
    
    def _group_related_pathologies(self, diagnoses: List[Dict]) -> List[Dict]:
        """
        Agrupa patologías relacionadas que deben valorarse conjuntamente
        según el RD 888/2022 para evitar doble valoración.
        Implementa una lógica de jerarquía: causa anatómica > consecuencia funcional.
        """
        if not diagnoses: return []
        
        grouped = []
        processed_indices = set()
        
        # Definición de grupos jerárquicos
        # 'primary_keywords' identifican la lesión anatómica principal (causa)
        # 'secondary_keywords' identifican las consecuencias funcionales que se deben subsumir
        hierarchical_groups = [
            # Grupo Hombro: Se unifican lesiones de partes blandas y óseas en una patología global.
            # Cualquiera de las "primary_keywords" puede iniciar el grupo.
            # Las "secondary_keywords" son síntomas funcionales que siempre se subsumen.
            {
                "name": "Patología traumática y/o degenerativa del hombro",
                "chapter": "8",
                "body_part": "hombro",
                # Añadimos "artrosis" y "omarthrosis" como palabras clave PRIMARIAS.
                "primary_keywords": ["rotura manguito", "lesión manguito", "tendinopatía manguito", "supraespinoso", "infraespinoso", "artrosis hombro", "artrosis acromioclavicular", "omarthrosis", "artrosis postraumática hombro"],
                "secondary_keywords": ["deficiencia funcional hombro", "limitación movilidad hombro", "omalgia", "dolor hombro", "discinesia", "amiotrofia"]
            },
            # Grupo Columna: Hernias/Espondilosis subsumen "dolor de espalda", "cervicalgia", etc.
            {
                "name": "Patología vertebral (columna)",
                "chapter": "8",
                "body_part": "columna",
                "primary_keywords": ["hernia discal", "protrusión discal", "espondilosis", "espondiloartrosis", "estenosis canal"],
                "secondary_keywords": ["deficiencia funcional columna", "cervicalgia", "dorsalgia", "lumbalgia", "lumbago", "ciática", "cervicobraquialgia", "lumbociatalgia", "dolor de espalda"]
            },
            # Grupo Tobillo/Pie: Síndrome del tarso/Tendinopatías subsumen "dolor de pie", "limitación", etc.
            {
                "name": "Patología de tobillo y pie",
                "chapter": "8",
                "body_part": "tobillo/pie",
                "primary_keywords": ["síndrome del tarso", "sindrome del tarso", "tendinopatía aquiles", "fascitis plantar", "espolón"],
                "secondary_keywords": ["deficiencia funcional tobillo", "limitación movilidad tobillo", "dolor de pie", "talalgia", "tendinopatía tobillo"]
            }
            # Se pueden añadir más grupos aquí (Rodilla, Cadera, etc.)
        ]
        
        # 1. Primera pasada: Buscar diagnósticos principales (causas anatómicas)
        for i, diag in enumerate(diagnoses):
            if i in processed_indices: continue
            
            normalized_text = diag.get("normalized_text", "")
            body_part = diag.get("body_part")
            
            matched_group_def = None
            
            # Intentar emparejar con un grupo jerárquico como diagnóstico PRINCIPAL
            for group_def in hierarchical_groups:
                # Verificar parte del cuerpo (si está definida en el diagnóstico)
                if body_part and body_part != "general" and group_def["body_part"] not in body_part:
                     continue

                # Verificar palabras clave primarias
                if any(kw in normalized_text for kw in group_def["primary_keywords"]):
                    matched_group_def = group_def
                    break
            
            if matched_group_def:
                # Hemos encontrado una causa anatómica principal. Iniciamos un grupo.
                group_diagnoses_texts = [diag.get("text", "")]
                processed_indices.add(i)
                
                # Buscar otros diagnósticos que sean consecuencias secundarias de este principal
                for j in range(i + 1, len(diagnoses)):
                    if j in processed_indices: continue
                    
                    other_diag = diagnoses[j]
                    other_normalized = other_diag.get("normalized_text", "")
                    other_body_part = other_diag.get("body_part")

                    # Verificar que coincida la parte del cuerpo
                    if other_body_part and other_body_part != "general" and matched_group_def["body_part"] not in other_body_part:
                         continue
                    
                    # Verificar si es una palabra clave SECUNDARIA (consecuencia funcional)
                    is_secondary = any(kw in other_normalized for kw in matched_group_def["secondary_keywords"])
                    # O si es otra palabra clave PRIMARIA del mismo grupo (ej. otra lesión de manguito)
                    is_primary = any(kw in other_normalized for kw in matched_group_def["primary_keywords"])

                    if is_secondary or is_primary:
                         group_diagnoses_texts.append(other_diag.get("text", ""))
                         processed_indices.add(j)
                
                # Crear el diagnóstico agrupado, usando el nombre del grupo principal
                grouped.append({
                    "text": diag.get("text"), # Mantener el nombre específico de la lesión principal
                    "normalized_text": normalized_text,
                    "related_diagnoses": group_diagnoses_texts, # Incluye el principal y los secundarios
                    "chapter": matched_group_def["chapter"],
                    "body_part": matched_group_def["body_part"],
                    "is_grouped": len(group_diagnoses_texts) > 1,
                    "group_name": matched_group_def["name"], # Nombre genérico del grupo
                    "start": diag.get("start"),
                    "end": diag.get("end")
                })

        # 2. Segunda pasada: Recoger los diagnósticos que no se agruparon
        for i, diag in enumerate(diagnoses):
            if i in processed_indices: continue
            
            # Verificar si este diagnóstico "huérfano" es una palabra clave SECUNDARIA de algún grupo
            # Si lo es, significa que no se encontró la causa principal, pero no debe valorarse solo si es muy genérico.
            is_orphan_secondary = False
            for group_def in hierarchical_groups:
                 normalized_text = diag.get("normalized_text", "")
                 body_part = diag.get("body_part")
                 if body_part and body_part != "general" and group_def["body_part"] not in body_part: continue

                 if any(kw in normalized_text for kw in group_def["secondary_keywords"]):
                      # Es una deficiencia funcional sin causa anatómica identificada.
                      # Se añade, pero marcándola para una valoración más conservadora.
                      diag["is_functional_only"] = True
                      is_orphan_secondary = True
                      break
            
            grouped.append(diag)
            processed_indices.add(i)
            
        return grouped
    
    def _extract_body_part(self, text: str) -> str:
        """Extrae la parte del cuerpo del diagnóstico (para sistema musculoesquelético)"""
        text_lower = text.lower()
        body_parts = ["hombro", "codo", "muñeca", "mano", "cadera", "rodilla", "tobillo", "pie", "tarso", 
                     "lumbar", "cervical", "dorsal", "columna"]
        
        for part in body_parts:
            if part in text_lower:
                # Normalizar partes compuestas
                if part in ["muñeca", "mano"]: return "muñeca/mano"
                if part in ["tobillo", "pie", "tarso"]: return "tobillo/pie"
                if part in ["lumbar", "cervical", "dorsal", "columna"]: return "columna"
                return part
        
        return "general"
    
    def _determine_chapter(self, text: str) -> str:
        """
        Determina el capítulo del RD 888/2022 según el sistema corporal afectado.
        Utiliza el mapeo system_patterns.
        """
        text_lower = text.lower()
        
        # Priorizar sistemas más específicos para evitar asignaciones genéricas incorrectas
        priority_chapters = ["15", "9", "10", "4", "5", "6", "7", "2", "8"]
        
        for chapter in priority_chapters:
            if chapter not in self.system_patterns: continue
            system_data = self.system_patterns[chapter]
            
            # 1. Buscar por patrones regex (más específicos)
            for pattern in system_data.get("patterns", []):
                if re.search(pattern, text_lower, re.IGNORECASE):
                    return chapter
            
            # 2. Buscar por palabras clave
            for keyword in system_data.get("keywords", []):
                 # Usar búsqueda de palabra completa para evitar falsos positivos (ej: "renal" en "adrenalina")
                 if re.search(r'\b' + re.escape(keyword) + r'\b', text_lower):
                    return chapter
        
        # Si no se detectó ningún sistema específico
        
        # Verificar si es claramente musculoesquelético por términos anatómicos o patológicos
        musculo_terms = ["hombro", "codo", "muñeca", "mano", "cadera", "rodilla", "tobillo", "pie", "tarso",
                         "columna", "cervical", "dorsal", "lumbar", "artrosis", "artritis", "tendinitis",
                         "tendinopatía", "esguince", "fractura", "luxación", "contractura", "dolor articular"]
        if any(re.search(r'\b' + re.escape(term) + r'\b', text_lower) for term in musculo_terms):
            return "8"

        # Último recurso: Capítulo 1 (General) - solo si hay evidencia de que es una enfermedad
        general_terms = ["síndrome", "sindrome", "enfermedad", "trastorno", "patología", "lesión"]
        if any(re.search(r'\b' + re.escape(term) + r'\b', text_lower) for term in general_terms):
             return "1"

        # Si no parece un diagnóstico médico, podría devolverse None o un capítulo especial de error
        return "unknown"

    def _extract_metrics(self, metrics: List[Dict]) -> Dict[str, float]:
        """Extrae y consolida las métricas funcionales más relevantes"""
        detected = {}
        
        for metric in metrics:
            metric_type = metric.get("type")
            value = metric.get("value")
            
            if metric_type and value is not None:
                try:
                    value_float = float(value)
                    # Para ROM (abducción, flexión, etc.), nos interesa el PEOR valor (el más bajo)
                    if metric_type in ["abduccion", "flexion", "extension", "rotacion", "rom_global"]:
                         # Si el valor es > 180, probablemente sea un error de OCR o no sea grados
                         if value_float > 180: continue
                         
                         if metric_type not in detected or value_float < detected[metric_type]:
                            detected[metric_type] = value_float
                    
                    # Para balance muscular (fuerza), nos interesa el PEOR valor (el más bajo)
                    elif metric_type == "fuerza":
                         # Fuerza suele ser 0-5
                         if value_float > 5: continue
                         if metric_type not in detected or value_float < detected[metric_type]:
                             detected[metric_type] = value_float
                    
                    # Para pérdida funcional (%), nos interesa el MAYOR valor
                    elif metric_type == "perdida_funcional":
                         if value_float > 100: continue
                         if metric_type not in detected or value_float > detected[metric_type]:
                             detected[metric_type] = value_float

                except ValueError:
                    continue
        
        return detected

    def _get_class_from_rom(self, body_part: str, metrics: Dict[str, float]) -> str:
        """Determina la clase de deficiencia basada en rangos de movilidad (ROM)"""
        if body_part not in self.rom_thresholds:
            return "1" # Por defecto si no hay umbrales definidos
        
        thresholds = self.rom_thresholds[body_part]
        worst_class = "0"
        
        # Revisar cada tipo de movimiento definido para esa parte del cuerpo
        for move_type, ranges in thresholds.items():
            # Buscar si tenemos una métrica para ese tipo de movimiento
            metric_value = None
            if move_type == "flexion_abduccion":
                # Usar el peor entre flexión y abducción si existen
                vals = [metrics.get(m) for m in ["flexion", "abduccion"] if metrics.get(m) is not None]
                if vals: metric_value = min(vals)
            elif move_type == "flexion_extension":
                 vals = [metrics.get(m) for m in ["flexion", "extension"] if metrics.get(m) is not None]
                 if vals: metric_value = min(vals)
            elif move_type == "flexion":
                metric_value = metrics.get("flexion")
            
            if metric_value is not None:
                # Comparar con los rangos para determinar la clase
                current_class = "0"
                if ranges["muy_grave"][0] <= metric_value <= ranges["muy_grave"][1]:
                    current_class = "4"
                elif ranges["grave"][0] <= metric_value <= ranges["grave"][1]:
                    current_class = "3"
                elif ranges["moderado"][0] <= metric_value <= ranges["moderado"][1]:
                    current_class = "2"
                elif ranges["leve"][0] <= metric_value <= ranges["leve"][1]:
                    current_class = "1"
                
                # Quedarse con la peor clase detectada
                if current_class > worst_class:
                    worst_class = current_class
                    
        return worst_class if worst_class != "0" else "1"

    def _classify_diagnosis(self, diagnosis: Dict, metrics: Dict[str, float]) -> Optional[Dict]:
        """
        Clasifica un diagnóstico según RD 888/2022 y asigna un porcentaje (VIA).
        Actualizado para manejar la agrupación jerárquica.
        """
        text = diagnosis.get("text", "")
        normalized_text = diagnosis.get("normalized_text", self._normalize_text(text))
        chapter = diagnosis.get("chapter")
        body_part = diagnosis.get("body_part")
        is_grouped = diagnosis.get("is_grouped", False)
        is_functional_only = diagnosis.get("is_functional_only", False) # Nueva bandera
        group_name = diagnosis.get("group_name", None)
        
        if not chapter or chapter == "unknown":
            return None 
            
        # Valores por defecto (Clase 1)
        class_num = "1"
        confidence = 0.5
        
        # --- Lógica de Clasificación por Capítulo ---
        
        if chapter == "8": # Sistema Musculoesquelético
            # 1. Clasificación basada en métricas (ROM), si existen
            rom_class = self._get_class_from_rom(body_part, metrics)
            if rom_class != "1": 
                class_num = rom_class
                confidence = 0.8 
            
            # 2. Considerar fuerza muscular
            fuerza = metrics.get("fuerza")
            if fuerza is not None and fuerza <= 3: 
                 if class_num < "2": class_num = "2"
                 confidence = max(confidence, 0.7)

            # 3. Valoración basada en la naturaleza de la patología (si no hay métricas determinantes)
            if class_num == "1":
                # Obtener todos los textos relacionados normalizados
                related_diagnoses = diagnosis.get("related_diagnoses", [])
                related_texts_normalized = [self._normalize_text(d) if isinstance(d, str) else self._normalize_text(d.get("text", "")) for d in related_diagnoses]
                all_texts = [normalized_text] + related_texts_normalized
                
                # Definir palabras clave de patologías que justifican al menos Clase 2
                severe_pathology_keywords = ["rotura manguito", "rotura del manguito", "lesión manguito", "hernia discal", "estenosis canal", "artrosis severa", "artrosis avanzada", "prótesis", "artroplastia"]
                
                # Comprobar si alguna de estas patologías está presente en el grupo
                is_severe = False
                for text in all_texts:
                    if any(kw in text for kw in severe_pathology_keywords):
                        is_severe = True
                        break
                
                if is_severe:
                     class_num = "2"
                     confidence = 0.6
                     if is_grouped: # Si es un grupo de lesiones graves, la confianza aumenta
                         confidence = 0.7

                # Deficiencias funcionales "huérfanas" (sin causa anatómica identificada)
                elif is_functional_only:
                     # Se mantienen en Clase 1 (leve) por defecto, salvo que haya métricas
                     class_num = "1"
                     confidence = 0.5 # Confianza media-baja
                     if any(kw in normalized_text for kw in ["severa", "grave", "importante"]):
                          class_num = "2"
                          confidence = 0.4 # Baja confianza, basado solo en adjetivos

                # Factores agravantes generales
                elif any(kw in normalized_text for kw in ["crónico", "persistente", "limitante"]):
                     confidence = 0.4

        # ... (El resto de capítulos 15, 4, etc., permanece igual que en la versión anterior) ...
        elif chapter == "15":
             if any(kw in normalized_text for kw in ["grave", "mayor", "severo", "crónico", "resistente", "esquizofrenia", "bipolar", "psicosis"]):
                class_num = "2"
                confidence = 0.6
             else:
                class_num = "1"
                confidence = 0.5
        elif chapter == "4":
            if "hipertensión" in normalized_text or "hta" in normalized_text:
                class_num = "0" if not any(kw in normalized_text for kw in ["resistente", "mal controlada"]) else "1"
                confidence = 0.7
            elif any(kw in normalized_text for kw in ["insuficiencia cardíaca", "infarto", "angina", "arritmia", "valvulopatía"]):
                class_num = "2"
                confidence = 0.6
            else:
                class_num = "1"
                confidence = 0.6
        elif chapter in ["5", "6", "7", "9", "10"]:
             if any(kw in normalized_text for kw in ["crónico", "severo", "insuficiencia", "grave"]):
                  class_num = "2"
                  confidence = 0.5
             else:
                  class_num = "1"
                  confidence = 0.6
        
        # --- Asignación del Porcentaje (VIA) ---
        class_data = self.classes_via.get(class_num, self.classes_via["1"])
        percentage = class_data["via"]
        description = class_data["description"]
        
        if class_num == "1" and percentage == 15 and confidence == 0.5:
             confidence = 0.4 

        # Construir la base legal / justificación
        legal_basis = f"RD 888/2022, Anexo III, Cap. {chapter}, {description} (VIA)"
        if is_grouped:
             legal_basis += ". Incluye valoración integral de síntomas y limitaciones funcionales asociadas."
        elif is_functional_only:
             legal_basis += ". Valoración funcional sin causa anatómica específica identificada en el texto."

        return {
            "diagnosis": text, # Usar el texto de la lesión principal
            "normalized_text": normalized_text,
            "chapter": chapter,
            "body_part": body_part,
            "class": class_num,
            "percentage": percentage,
            "description": description,
            "confidence": confidence,
            "legal_basis": legal_basis,
            "is_grouped": is_grouped,
            "group_name": group_name,
            "related_diagnoses": diagnosis.get("related_diagnoses", [])
        }
    
    def _calculate_final_valuation(self, chapter_valuations: List[Dict]) -> Optional[Dict]:
        """
        Calcula la valoración final (GDA) aplicando la fórmula de combinación.
        Calcula una confianza global basada en las confianzas individuales.
        """
        if not chapter_valuations: return None
        
        # Obtener porcentajes y confianzas
        percentages = [v.get("percentage", 0) for v in chapter_valuations]
        confidences = [v.get("confidence", 0) for v in chapter_valuations]
        
        # Ordenar de mayor a menor porcentaje
        percentages.sort(reverse=True)
        
        # Aplicar fórmula de combinación: A + B(1 - A/100)
        combined_percentage = percentages[0] if percentages else 0
        for next_p in percentages[1:]:
            combined_percentage = combined_percentage + (next_p * (100 - combined_percentage) / 100)
        
        # Redondear y limitar
        bdgp_percentage = min(round(combined_percentage, 2), 99.0) # Máximo 99% según RD
        
        # Determinar clase final
        final_class = "0"
        for c_num, c_data in self.classes_via.items():
            min_p, max_p = c_data["range"]
            if min_p <= bdgp_percentage <= max_p:
                final_class = c_num
                break
        
        # Calcular confianza global (promedio ponderado por porcentaje, simplificado)
        avg_confidence = statistics.mean(confidences) if confidences else 0.0
        # Penalizar si hay muchas deficiencias pequeñas combinadas (mayor incertidumbre)
        if len(percentages) > 3:
             avg_confidence *= 0.9
        
        # GDA preliminar (sin BLA/BRP/BFCA)
        gda_percentage = bdgp_percentage
        
        # Fórmula para mostrar
        if len(percentages) > 1:
            formula_parts = [f"{p}%" for p in percentages[:3]]
            if len(percentages) > 3: formula_parts.append("...")
            formula = f"Combinación (Art. 4.2): {' + '.join(formula_parts)} = {bdgp_percentage}%"
        else:
            formula = f"BDGP (Capítulo único): {bdgp_percentage}%"

        return {
            "bdgp_percentage": bdgp_percentage,
            "gda_percentage": gda_percentage,
            "final_class": final_class,
            "description": self.classes_via.get(final_class, {}).get("description", "N/A"),
            "components_count": len(chapter_valuations),
            "formula": formula,
            "confidence": round(avg_confidence, 2),
            "legal_basis": "RD 888/2022, Art. 4.2 (Fórmula de combinación de deficiencias)"
        }
