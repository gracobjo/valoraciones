"""
Generador de informes legales comparativos mejorado
Compara valoraciones entre múltiples documentos y destaca discrepancias
Versión refactorizada con métodos modulares para mejor mantenibilidad
"""
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
import re


class ReportGenerator:
    """Genera informes legales completos con comparación de documentos"""
    
    def generate_comparative_report(self, clinical_data: Optional[Dict], 
                                   judicial_data: Optional[Dict], 
                                   administrative_data: Optional[Dict]) -> str:
        """
        Orquesta la generación del informe comparativo completo
        
        Args:
            clinical_data: Análisis del informe médico/pericial
            judicial_data: Análisis de la sentencia judicial
            administrative_data: Análisis de la resolución administrativa
        
        Returns:
            Reporte en formato texto
        """
        report_lines = []
        
        # Encabezado
        report_lines.extend(self._generate_header())
        
        # Información de documentos
        report_lines.extend(self._generate_documents_info(clinical_data, judicial_data, administrative_data))
        
        # Análisis individuales detallados
        all_valuations = {}
        
        if clinical_data:
            report_lines.extend(self._format_individual_analysis("INFORME MÉDICO/PERICIAL", clinical_data, "pericial"))
            all_valuations['pericial'] = self._extract_valuation_data(clinical_data)
        
        if judicial_data:
            report_lines.extend(self._format_individual_analysis("SENTENCIA JUDICIAL", judicial_data, "judicial"))
            all_valuations['judicial'] = self._extract_valuation_data(judicial_data)
        
        if administrative_data:
            report_lines.extend(self._format_individual_analysis("RESOLUCIÓN ADMINISTRATIVA", administrative_data, "administrativa"))
            all_valuations['administrativa'] = self._extract_valuation_data(administrative_data)
        
        # Comparación estratégica (patología por patología)
        report_lines.extend(self._generate_strategic_comparison(clinical_data, judicial_data, administrative_data, all_valuations))
        
        # Recomendaciones concretas
        report_lines.extend(self._generate_concrete_recommendations(clinical_data, judicial_data, administrative_data, all_valuations))
        
        # Pie de página
        report_lines.extend(self._generate_footer())
        
        return "\n".join(report_lines)
    
    def _generate_header(self) -> List[str]:
        """Genera el encabezado del informe"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return [
            "=" * 80,
            "INFORME LEGAL COMPLETO - RD 888/2022",
            "Análisis Comparativo de Valoración de Deficiencias",
            "=" * 80,
            "",
            f"Fecha de generación: {fecha_actual}",
            ""
        ]
    
    def _generate_documents_info(self, clinical_data: Optional[Dict], 
                                 judicial_data: Optional[Dict], 
                                 administrative_data: Optional[Dict]) -> List[str]:
        """Genera la sección de información de documentos analizados"""
        lines = [
            "DOCUMENTOS ANALIZADOS",
            "-" * 80,
            ""
        ]
        
        doc_count = 0
        if clinical_data:
            doc_count += 1
            filename = clinical_data.get('filename', 'Documento médico')
            lines.append(f"{doc_count}. Informe Médico/Pericial: {filename}")
        if judicial_data:
            doc_count += 1
            filename = judicial_data.get('filename', 'Documento judicial')
            lines.append(f"{doc_count}. Sentencia Judicial: {filename}")
        if administrative_data:
            doc_count += 1
            filename = administrative_data.get('filename', 'Documento administrativo')
            lines.append(f"{doc_count}. Resolución Administrativa: {filename}")
        
        if doc_count == 0:
            lines.append("No hay documentos analizados.")
            return lines
        
        lines.append("")
        return lines
    
    def _format_individual_analysis(self, title: str, data: Dict, doc_type: str) -> List[str]:
        """
        Genera una sección de análisis detallado para un documento.
        Muestra el desglose patología por patología y la fórmula.
        
        Args:
            title: Título de la sección
            data: Datos del análisis del documento
            doc_type: Tipo de documento ('pericial', 'judicial', 'administrativa')
        """
        lines = [
            "=" * 80,
            f"ANÁLISIS DETALLADO: {title}",
            "=" * 80,
            ""
        ]
        
        filename = data.get('filename', 'Documento')
        lines.append(f"Archivo: {filename}")
        lines.append("")
        
        legal_analysis = data.get('legal_analysis', {})
        chapter_valuations = legal_analysis.get('chapter_valuations', [])
        
        # Desglose de deficiencias reconocidas
        if chapter_valuations:
            lines.append("DESGLOSE DE DEFICIENCIAS RECONOCIDAS:")
            lines.append("-" * 80)
            lines.append("")
            
            for i, valuation in enumerate(chapter_valuations, 1):
                diag = valuation.get('diagnosis', 'N/A')
                pct = valuation.get('percentage', 0)
                cls = valuation.get('class', 'N/A')
                desc = valuation.get('description', 'N/A')
                chapter = valuation.get('chapter', 'N/A')
                body_part = valuation.get('body_part', 'N/A')
                legal_basis = valuation.get('legal_basis', 'RD 888/2022')
                is_grouped = valuation.get('is_grouped', False)
                confidence = valuation.get('confidence', 0)
                
                lines.append(f"  {i}. {diag}")
                lines.append(f"     • Capítulo RD 888/2022: {chapter}")
                if body_part != 'N/A' and body_part != 'general':
                    lines.append(f"     • Región anatómica: {body_part}")
                lines.append(f"     • Clase: {cls} ({desc})")
                lines.append(f"     • Porcentaje (VIA): {pct}%")
                lines.append(f"     • Base legal: {legal_basis}")
                if is_grouped:
                    related = valuation.get('related_diagnoses', [])
                    if related:
                        lines.append(f"     • Patologías agrupadas: {', '.join(related[:3])}")
                        if len(related) > 3:
                            lines.append(f"       ... y {len(related) - 3} más")
                lines.append(f"     • Confianza: {confidence * 100:.0f}%")
                lines.append("")
        else:
            # Si no hay valoraciones detalladas, mostrar diagnósticos detectados
            diagnoses = legal_analysis.get('detected_diagnoses', [])
            if diagnoses:
                lines.append("Diagnósticos detectados (sin valoración detallada):")
                for i, diag in enumerate(diagnoses[:10], 1):
                    diag_text = diag.get('text', diag) if isinstance(diag, dict) else str(diag)
                    lines.append(f"  {i}. {diag_text}")
                if len(diagnoses) > 10:
                    lines.append(f"  ... y {len(diagnoses) - 10} más")
                lines.append("")
        
        # Cálculo del grado final con fórmula paso a paso
        final_val = legal_analysis.get('final_valuation', {})
        if final_val:
            lines.extend(self._format_final_valuation_calculation(final_val, doc_type))
        else:
            suggested = legal_analysis.get('suggested_classification', {})
            if suggested:
                perc = suggested.get('suggested_percentage', 0)
                cls = suggested.get('class_number', 'N/A')
                lines.append(f"Valoración sugerida: {perc}% (Clase {cls})")
                lines.append("")
        
        # Para resolución administrativa, extraer fundamentos médicos
        if doc_type == 'administrativa':
            lines.extend(self._extract_administrative_foundations(data))
        
        lines.append("")
        return lines
    
    def _format_final_valuation_calculation(self, final_val: Dict, doc_type: str) -> List[str]:
        """
        Formatea el cálculo del grado final mostrando la fórmula paso a paso
        
        Args:
            final_val: Diccionario con la valoración final
            doc_type: Tipo de documento
        """
        lines = [
            "CÁLCULO DEL GRADO FINAL (BDGP):",
            "-" * 80,
            ""
        ]
        
        bdgp = final_val.get('bdgp_percentage', 0)
        final_class = final_val.get('final_class', 'N/A')
        description = final_val.get('description', 'N/A')
        formula = final_val.get('formula', 'N/A')
        components_count = final_val.get('components_count', 0)
        
        lines.append(f"RESULTADO FINAL BDGP: {bdgp}% (Clase {final_class} - {description})")
        lines.append(f"Número de deficiencias combinadas: {components_count}")
        lines.append("")
        
        if formula and formula != 'N/A':
            lines.append("Fórmula de combinación aplicada:")
            lines.append(f"  {formula}")
            lines.append("")
        
        # Mostrar fórmula paso a paso si tenemos los componentes
        chapter_valuations = final_val.get('chapter_valuations', [])
        if not chapter_valuations:
            # Intentar extraer de la fórmula si está disponible
            if 'Combinación' in str(formula):
                lines.append("Justificación: La valoración final se obtiene mediante la aplicación")
                lines.append("del Art. 4.2 del RD 888/2022, combinando las deficiencias individuales")
                lines.append("según la fórmula: A + B(1 - A/100) + C(1 - resultado anterior/100)...")
                lines.append("")
        else:
            # Mostrar cálculo paso a paso
            lines.append("Cálculo paso a paso:")
            percentages = [v.get('percentage', 0) for v in chapter_valuations if v.get('percentage', 0) > 0]
            percentages.sort(reverse=True)
            
            if len(percentages) > 1:
                lines.append(f"  Paso 1: {percentages[0]}%")
                current_result = percentages[0]
                for i, next_p in enumerate(percentages[1:], 2):
                    prev_result = current_result
                    current_result = prev_result + (next_p * (100 - prev_result) / 100)
                    lines.append(f"  Paso {i}: {prev_result:.2f}% + {next_p}% × (1 - {prev_result:.2f}/100) = {current_result:.2f}%")
                lines.append(f"  RESULTADO FINAL: {current_result:.2f}%")
            elif len(percentages) == 1:
                lines.append(f"  Valoración única: {percentages[0]}%")
            lines.append("")
        
        # Nota sobre baremos complementarios
        if doc_type in ['pericial', 'judicial']:
            lines.append("NOTA: Esta valoración corresponde al BDGP (Baremo de Deficiencia Global de la Persona).")
            lines.append("El Grado Final de Discapacidad puede requerir ajustes según:")
            lines.append("  • Baremo de Limitaciones en la Actividad (BLA) - Anexo IV")
            lines.append("  • Baremo de Restricciones en la Participación (BRP) - Anexo V")
            lines.append("  • Baremo de Factores Contextuales y Barreras Ambientales (BFCA) - Anexo VI")
            lines.append("")
        
        return lines
    
    def _extract_administrative_foundations(self, admin_data: Dict) -> List[str]:
        """
        Extrae los fundamentos médicos de la resolución administrativa
        
        Args:
            admin_data: Datos de la resolución administrativa
        """
        lines = []
        extracted_text = admin_data.get('extracted_text', '') or admin_data.get('full_extracted_text', '')
        
        if not extracted_text:
            return lines
        
        text_lower = extracted_text.lower()
        lines.append("FUNDAMENTOS MÉDICOS DETECTADOS EN LA RESOLUCIÓN:")
        lines.append("-" * 80)
        
        # Buscar menciones de patologías reconocidas
        admin_analysis = admin_data.get('legal_analysis', {})
        chapter_valuations = admin_analysis.get('chapter_valuations', [])
        
        if chapter_valuations:
            lines.append("Patologías reconocidas en la resolución:")
            for i, val in enumerate(chapter_valuations, 1):
                diagnosis = val.get('diagnosis', 'N/A')
                percentage = val.get('percentage', 0)
                class_num = val.get('class', 'N/A')
                lines.append(f"  {i}. {diagnosis}: {percentage}% (Clase {class_num})")
            lines.append("")
        else:
            lines.append("No se detectaron patologías específicas valoradas en la resolución.")
            lines.append("")
        
        # Buscar si se menciona la fórmula de combinación
        if 'combinación' in text_lower or 'fórmula' in text_lower:
            lines.append("✓ La resolución menciona la aplicación de la fórmula de combinación")
            lines.append("  de deficiencias según el Art. 4.2 del RD 888/2022.")
        else:
            lines.append("⚠️  OBSERVACIÓN: La resolución no menciona explícitamente la aplicación")
            lines.append("   de la fórmula de combinación, lo que sugiere que puede haber reconocido")
            lines.append("   una única deficiencia o no haber aplicado correctamente el baremo.")
        
        lines.append("")
        
        # Verificar baremos complementarios
        has_bla = 'bla' in text_lower or 'limitaciones en la actividad' in text_lower
        has_brp = 'brp' in text_lower or 'restricciones en la participación' in text_lower
        has_bfca = 'bfca' in text_lower or 'factores contextuales' in text_lower
        
        if has_bla or has_brp or has_bfca:
            lines.append("Baremos complementarios mencionados:")
            if has_bla:
                lines.append("  ✓ Baremo de Limitaciones en la Actividad (BLA) - Anexo IV")
            if has_brp:
                lines.append("  ✓ Baremo de Restricciones en la Participación (BRP) - Anexo V")
            if has_bfca:
                lines.append("  ✓ Baremo de Factores Contextuales (BFCA) - Anexo VI")
        else:
            lines.append("⚠️  No se detectan menciones a baremos complementarios (BLA, BRP, BFCA)")
            lines.append("   en la resolución. Esto puede indicar que no se han valorado estos aspectos.")
        
        lines.append("")
        return lines
    
    def _extract_valuation_data(self, data: Dict) -> Optional[Dict]:
        """Extrae los datos de valoración de un documento"""
        legal_analysis = data.get('legal_analysis', {})
        final_val = legal_analysis.get('final_valuation', {})
        suggested = legal_analysis.get('suggested_classification', {})
        chapter_valuations = legal_analysis.get('chapter_valuations', [])
        
        if final_val:
            return {
                'percentage': final_val.get('bdgp_percentage', 0),
                'class': final_val.get('final_class', 'N/A'),
                'description': final_val.get('description', 'N/A'),
                'components': final_val.get('components_count', 0),
                'chapter_valuations': chapter_valuations,
                'formula': final_val.get('formula', 'N/A')
            }
        elif suggested:
            return {
                'percentage': suggested.get('suggested_percentage', 0),
                'class': suggested.get('class_number', 'N/A'),
                'description': suggested.get('description', 'N/A'),
                'components': 0,
                'chapter_valuations': chapter_valuations,
                'formula': None
            }
        return None
    
    def _generate_strategic_comparison(self, clinical_data: Optional[Dict],
                                     judicial_data: Optional[Dict],
                                     administrative_data: Optional[Dict],
                                     all_valuations: Dict) -> List[str]:
        """
        Genera la tabla comparativa por patología y analiza discrepancias
        
        Args:
            clinical_data: Datos del informe pericial
            judicial_data: Datos de la sentencia judicial
            administrative_data: Datos de la resolución administrativa
            all_valuations: Diccionario con todas las valoraciones extraídas
        """
        lines = [
            "=" * 80,
            "COMPARACIÓN ESTRATÉGICA: PATOLOGÍA POR PATOLOGÍA",
            "=" * 80,
            ""
        ]
        
        # 1. Crear lista maestra de todos los diagnósticos únicos
        master_diagnoses = {}
        
        # Recopilar diagnósticos del informe pericial
        if clinical_data:
            clinical_analysis = clinical_data.get('legal_analysis', {})
            chapter_valuations = clinical_analysis.get('chapter_valuations', [])
            for val in chapter_valuations:
                diag = val.get('diagnosis', '')
                if diag:
                    normalized = self._normalize_diagnosis_text(diag)
                    if normalized not in master_diagnoses:
                        master_diagnoses[normalized] = {
                            'original': diag,
                            'pericial': None,
                            'judicial': None,
                            'administrativa': None,
                            'chapter': val.get('chapter', 'N/A'),
                            'body_part': val.get('body_part', 'N/A')
                        }
                    master_diagnoses[normalized]['pericial'] = {
                        'percentage': val.get('percentage', 0),
                        'class': val.get('class', 'N/A'),
                        'description': val.get('description', 'N/A')
                    }
        
        # Recopilar diagnósticos de la sentencia judicial
        if judicial_data:
            judicial_analysis = judicial_data.get('legal_analysis', {})
            chapter_valuations = judicial_analysis.get('chapter_valuations', [])
            for val in chapter_valuations:
                diag = val.get('diagnosis', '')
                if diag:
                    normalized = self._normalize_diagnosis_text(diag)
                    if normalized not in master_diagnoses:
                        master_diagnoses[normalized] = {
                            'original': diag,
                            'pericial': None,
                            'judicial': None,
                            'administrativa': None,
                            'chapter': val.get('chapter', 'N/A'),
                            'body_part': val.get('body_part', 'N/A')
                        }
                    master_diagnoses[normalized]['judicial'] = {
                        'percentage': val.get('percentage', 0),
                        'class': val.get('class', 'N/A'),
                        'description': val.get('description', 'N/A')
                    }
        
        # Recopilar diagnósticos de la resolución administrativa
        if administrative_data:
            admin_analysis = administrative_data.get('legal_analysis', {})
            chapter_valuations = admin_analysis.get('chapter_valuations', [])
            for val in chapter_valuations:
                diag = val.get('diagnosis', '')
                if diag:
                    normalized = self._normalize_diagnosis_text(diag)
                    if normalized not in master_diagnoses:
                        master_diagnoses[normalized] = {
                            'original': diag,
                            'pericial': None,
                            'judicial': None,
                            'administrativa': None,
                            'chapter': val.get('chapter', 'N/A'),
                            'body_part': val.get('body_part', 'N/A')
                        }
                    master_diagnoses[normalized]['administrativa'] = {
                        'percentage': val.get('percentage', 0),
                        'class': val.get('class', 'N/A'),
                        'description': val.get('description', 'N/A')
                    }
        
        if not master_diagnoses:
            lines.append("No se detectaron patologías específicas para comparar.")
            lines.append("")
            return lines
        
        # 2. Crear tabla comparativa
        lines.append("TABLA COMPARATIVA DE VALORACIONES POR PATOLOGÍA:")
        lines.append("-" * 80)
        lines.append("")
        
        # Encabezado de la tabla
        col_lesion_width = 45
        col_pct_width = 12
        col_class_width = 8
        
        header = f"{'PATOLOGÍA':<{col_lesion_width}} | {'PERICIAL':<{col_pct_width}} | {'JUDICIAL':<{col_pct_width}} | {'ADMIN.':<{col_pct_width}}"
        lines.append(header)
        lines.append("-" * len(header))
        
        # Filas de la tabla
        for normalized, diag_data in sorted(master_diagnoses.items()):
            original = diag_data['original']
            lesion_display = original[:col_lesion_width] if len(original) <= col_lesion_width else original[:col_lesion_width-3] + "..."
            
            # Obtener valoraciones
            perc_pericial = self._find_percentage_for_diagnosis(clinical_data, normalized, diag_data['pericial'])
            perc_judicial = self._find_percentage_for_diagnosis(judicial_data, normalized, diag_data['judicial'])
            perc_admin = self._find_percentage_for_diagnosis(administrative_data, normalized, diag_data['administrativa'])
            
            row = f"{lesion_display:<{col_lesion_width}} | {perc_pericial:<{col_pct_width}} | {perc_judicial:<{col_pct_width}} | {perc_admin:<{col_pct_width}}"
            lines.append(row)
        
        lines.append("")
        lines.append("Leyenda: X% (Clase Y) = Porcentaje y clase reconocidos; 'NO RECON.' = No reconocida")
        lines.append("")
        
        # 3. Análisis detallado de discrepancias por patología
        lines.append("ANÁLISIS DETALLADO DE DISCREPANCIAS POR PATOLOGÍA:")
        lines.append("-" * 80)
        lines.append("")
        
        for normalized, diag_data in sorted(master_diagnoses.items()):
            original = diag_data['original']
            chapter = diag_data['chapter']
            body_part = diag_data['body_part']
            
            lines.append(f"Patología: {original}")
            lines.append(f"  Capítulo RD 888/2022: {chapter}")
            if body_part != 'N/A' and body_part != 'general':
                lines.append(f"  Región anatómica: {body_part}")
            lines.append("")
            
            # Mostrar valoraciones
            if diag_data['pericial']:
                pct_p = diag_data['pericial']['percentage']
                cls_p = diag_data['pericial']['class']
                lines.append(f"  • Informe Pericial: {pct_p}% (Clase {cls_p})")
            else:
                lines.append(f"  • Informe Pericial: No valorada")
            
            if diag_data['judicial']:
                pct_j = diag_data['judicial']['percentage']
                cls_j = diag_data['judicial']['class']
                lines.append(f"  • Sentencia Judicial: {pct_j}% (Clase {cls_j})")
            else:
                lines.append(f"  • Sentencia Judicial: No valorada")
            
            if diag_data['administrativa']:
                pct_a = diag_data['administrativa']['percentage']
                cls_a = diag_data['administrativa']['class']
                lines.append(f"  • Resolución Administrativa: {pct_a}% (Clase {cls_a})")
            else:
                lines.append(f"  • Resolución Administrativa: No valorada")
            
            lines.append("")
            
            # Análisis de discrepancia
            if diag_data['pericial'] and diag_data['administrativa']:
                pct_p = diag_data['pericial']['percentage']
                pct_a = diag_data['administrativa']['percentage']
                diff = pct_p - pct_a
                
                if abs(diff) >= 5:
                    lines.append(f"  ⚠️  DISCREPANCIA DETECTADA: Diferencia de {diff:+.1f} puntos porcentuales")
                    lines.append(f"     El informe pericial valora esta patología con {pct_p}% (Clase {diag_data['pericial']['class']}),")
                    lines.append(f"     mientras que la resolución administrativa la valora solo con {pct_a}% (Clase {diag_data['administrativa']['class']}).")
                    lines.append(f"     Esta diferencia indica una posible infravaloración de la limitación funcional")
                    lines.append(f"     según los criterios del Capítulo {chapter} del RD 888/2022.")
                    lines.append("")
            elif diag_data['pericial'] and not diag_data['administrativa']:
                lines.append(f"  ⚠️  OMISIÓN DETECTADA: La resolución administrativa no reconoce esta patología,")
                lines.append(f"     que está valorada en {diag_data['pericial']['percentage']}% (Clase {diag_data['pericial']['class']})")
                lines.append(f"     en el informe pericial. Esta omisión puede constituir un error de valoración.")
                lines.append("")
            
            lines.append("")
        
        # 4. Análisis de discrepancia global
        pericial_val = all_valuations.get('pericial') or all_valuations.get('judicial')
        admin_val = all_valuations.get('administrativa')
        
        if pericial_val and admin_val:
            lines.extend(self._analyze_global_discrepancy(pericial_val, admin_val, all_valuations.get('judicial')))
        
        return lines
    
    def _normalize_diagnosis_text(self, text: str) -> str:
        """Normaliza el texto de un diagnóstico para comparación"""
        if not text:
            return ""
        # Convertir a minúsculas y eliminar espacios extra
        normalized = text.lower().strip()
        normalized = re.sub(r'\s+', ' ', normalized)
        # Eliminar artículos y palabras comunes
        normalized = re.sub(r'\b(el|la|los|las|de|del|de la|del|un|una)\b', '', normalized)
        normalized = re.sub(r'\s+', ' ', normalized).strip()
        return normalized
    
    def _find_percentage_for_diagnosis(self, doc_data: Optional[Dict], normalized_diag: str, direct_val: Optional[Dict]) -> str:
        """
        Busca el porcentaje de un diagnóstico en un documento
        
        Args:
            doc_data: Datos del documento
            normalized_diag: Diagnóstico normalizado a buscar
            direct_val: Valoración directa si ya se conoce
        
        Returns:
            String con el porcentaje y clase, o "NO RECON."
        """
        if direct_val:
            pct = direct_val.get('percentage', 0)
            cls = direct_val.get('class', 'N/A')
            return f"{pct}% (Clase {cls})"
        
        if not doc_data:
            return "NO RECON."
        
        legal_analysis = doc_data.get('legal_analysis', {})
        chapter_valuations = legal_analysis.get('chapter_valuations', [])
        
        for val in chapter_valuations:
            diag = val.get('diagnosis', '')
            if diag:
                normalized = self._normalize_diagnosis_text(diag)
                # Comparación simple (podría mejorarse con Jaccard)
                if normalized == normalized_diag or normalized_diag in normalized or normalized in normalized_diag:
                    pct = val.get('percentage', 0)
                    cls = val.get('class', 'N/A')
                    return f"{pct}% (Clase {cls})"
        
        return "NO RECON."
    
    def _analyze_global_discrepancy(self, pericial_val: Dict, admin_val: Dict, judicial_val: Optional[Dict]) -> List[str]:
        """
        Analiza la discrepancia global entre valoraciones
        
        Args:
            pericial_val: Valoración del informe pericial
            admin_val: Valoración administrativa
            judicial_val: Valoración judicial (opcional)
        """
        lines = [
            "ANÁLISIS DE LA DISCREPANCIA GLOBAL:",
            "-" * 80,
            ""
        ]
        
        pericial_pct = pericial_val['percentage']
        admin_pct = admin_val['percentage']
        diferencia = pericial_pct - admin_pct
        pericial_class = pericial_val['class']
        admin_class = admin_val['class']
        
        lines.append(f"Se ha detectado una discrepancia sustancial entre la valoración del")
        lines.append(f"informe pericial y la resolución administrativa previa:")
        lines.append("")
        lines.append(f"  • Valoración Pericial:        {pericial_pct}% (Clase {pericial_class})")
        lines.append(f"  • Valoración Administrativa:  {admin_pct}% (Clase {admin_class})")
        lines.append(f"  • Diferencia:                 {diferencia:+.1f} puntos porcentuales")
        lines.append("")
        
        if abs(diferencia) >= 10:
            lines.append("⚠️  DISCREPANCIA CRÍTICA DETECTADA")
            lines.append("-" * 80)
            lines.append(f"La diferencia de {abs(diferencia):.1f} puntos porcentuales representa una")
            lines.append(f"discrepancia crítica que indica una posible infravaloración significativa")
            lines.append(f"en la resolución administrativa inicial.")
            lines.append("")
            
            # Análisis del cambio de clase
            if pericial_class != admin_class:
                lines.append("CAMBIO DE CLASIFICACIÓN:")
                lines.append("-" * 80)
                lines.append(f"La valoración pericial ({pericial_pct}%) clasifica la deficiencia como")
                lines.append(f"Clase {pericial_class} ({pericial_val.get('description', 'N/A')}),")
                lines.append(f"mientras que la resolución administrativa ({admin_pct}%) la clasificó como")
                lines.append(f"Clase {admin_class} ({admin_val.get('description', 'N/A')}).")
                lines.append("")
                lines.append("Este cambio de clasificación refleja una diferencia sustancial en la")
                lines.append("interpretación de la gravedad de las deficiencias según el RD 888/2022.")
                lines.append("")
        
        # Consideración de la sentencia judicial
        if judicial_val:
            judicial_pct = judicial_val['percentage']
            judicial_class = judicial_val['class']
            diferencia_judicial = judicial_pct - admin_pct
            
            lines.append("CONSIDERACIÓN DE LA SENTENCIA JUDICIAL:")
            lines.append("-" * 80)
            lines.append("")
            lines.append(f"La sentencia judicial reconoce una valoración de {judicial_pct}%")
            lines.append(f"(Clase {judicial_class}), lo cual es significativamente superior a la")
            lines.append(f"valoración administrativa previa de {admin_pct}%.")
            lines.append("")
            lines.append(f"Esta diferencia de {diferencia_judicial:+.1f} puntos porcentuales entre")
            lines.append("la sentencia judicial y la resolución administrativa previa indica una")
            lines.append("posible infravaloración inicial en la resolución administrativa.")
            lines.append("")
            lines.append("La sentencia judicial, al reconocer una valoración superior, refuerza")
            lines.append("la necesidad de revisar la valoración administrativa inicial y puede")
            lines.append("constituir base para reclamación o recurso.")
            lines.append("")
        
        return lines
    
    def _generate_concrete_recommendations(self, clinical_data: Optional[Dict],
                                          judicial_data: Optional[Dict],
                                          administrative_data: Optional[Dict],
                                          all_valuations: Dict) -> List[str]:
        """
        Genera recomendaciones legales específicas basadas en las discrepancias detectadas
        
        Args:
            clinical_data: Datos del informe pericial
            judicial_data: Datos de la sentencia judicial
            administrative_data: Datos de la resolución administrativa
            all_valuations: Diccionario con todas las valoraciones
        """
        lines = [
            "=" * 80,
            "RECOMENDACIONES LEGALES ESPECÍFICAS Y FUNDAMENTADAS",
            "=" * 80,
            ""
        ]
        
        pericial_val = all_valuations.get('pericial')
        judicial_val = all_valuations.get('judicial')
        admin_val = all_valuations.get('administrativa')
        
        if not pericial_val or not admin_val:
            lines.append("No hay suficientes datos para generar recomendaciones específicas.")
            lines.append("")
            return lines
        
        pericial_pct = pericial_val['percentage']
        admin_pct = admin_val['percentage']
        diferencia = pericial_pct - admin_pct
        
        if diferencia > 10:  # Discrepancia significativa
            lines.append("RECOMENDACIÓN PRINCIPAL: RECLAMACIÓN POR INFRAVALORACIÓN")
            lines.append("-" * 80)
            lines.append("")
            lines.append("Se recomienda interponer RECLAMACIÓN PREVIA (o RECURSO ADMINISTRATIVO")
            lines.append("si ya se agotó la vía previa) solicitando la revisión del grado de discapacidad")
            lines.append("por infravaloración, fundamentada en las siguientes razones:")
            lines.append("")
            
            # 1. Discrepancia sustancial
            lines.append("1. DISCREPANCIA SUSTANCIAL EN LA VALORACIÓN GLOBAL:")
            lines.append(f"   • Valoración pericial/judicial: {pericial_pct}% (Clase {pericial_val['class']})")
            lines.append(f"   • Valoración administrativa: {admin_pct}% (Clase {admin_val['class']})")
            lines.append(f"   • Diferencia: {diferencia:.1f} puntos porcentuales")
            lines.append("")
            
            # 2. Patologías específicas infravaloradas
            lines.append("2. PATOLOGÍAS ESPECÍFICAS INFRAVALORADAS:")
            lines.append("")
            
            pericial_chapters = pericial_val.get('chapter_valuations', [])
            admin_chapters = admin_val.get('chapter_valuations', [])
            
            # Crear diccionario de patologías administrativas para búsqueda rápida
            admin_pathologies = {}
            for admin_val_item in admin_chapters:
                diag = admin_val_item.get('diagnosis', '')
                if diag:
                    normalized = self._normalize_diagnosis_text(diag)
                    admin_pathologies[normalized] = admin_val_item
            
            for val in pericial_chapters:
                diag = val.get('diagnosis', '')
                if not diag:
                    continue
                
                normalized = self._normalize_diagnosis_text(diag)
                pct_p = val.get('percentage', 0)
                cls_p = val.get('class', 'N/A')
                chapter = val.get('chapter', 'N/A')
                
                # Buscar en administrativa
                found_in_admin = None
                for norm_key, admin_item in admin_pathologies.items():
                    if normalized == norm_key or normalized in norm_key or norm_key in normalized:
                        found_in_admin = admin_item
                        break
                
                if found_in_admin:
                    pct_a = found_in_admin.get('percentage', 0)
                    cls_a = found_in_admin.get('class', 'N/A')
                    if pct_p > pct_a:
                        lines.append(f"   • {diag}:")
                        lines.append(f"     - Valoración pericial: {pct_p}% (Clase {cls_p})")
                        lines.append(f"     - Valoración administrativa: {pct_a}% (Clase {cls_a})")
                        lines.append(f"     - Diferencia: {pct_p - pct_a:+.1f} puntos porcentuales")
                        lines.append(f"     - Se recomienda solicitar la aplicación de los criterios")
                        lines.append(f"       de la Clase {cls_p} según el Capítulo {chapter} del RD 888/2022")
                        lines.append("")
                else:
                    lines.append(f"   • {diag}:")
                    lines.append(f"     - Valoración pericial: {pct_p}% (Clase {cls_p})")
                    lines.append(f"     - NO RECONOCIDA en la resolución administrativa")
                    lines.append(f"     - Se recomienda solicitar su reconocimiento y valoración")
                    lines.append(f"       según el Capítulo {chapter} del RD 888/2022")
                    lines.append("")
            
            # 3. Documentación a aportar
            lines.append("3. DOCUMENTACIÓN A APORTAR:")
            lines.append("   • Informe médico/pericial completo")
            if judicial_val:
                lines.append("   • Sentencia judicial que reconoce valoración superior")
            lines.append("   • Resolución administrativa impugnada")
            lines.append("   • Cualquier informe médico complementario")
            lines.append("")
            
            # 4. Solicitudes específicas
            lines.append("4. SOLICITUDES ESPECÍFICAS A INCLUIR EN LA RECLAMACIÓN:")
            lines.append("   • Revisión del grado de discapacidad por infravaloración")
            lines.append("   • Aplicación correcta de los criterios del RD 888/2022")
            lines.append("   • Reconocimiento de todas las patologías detectadas en el informe pericial")
            lines.append("   • Valoración de los Factores Contextuales (BFCA) del Anexo VI,")
            lines.append("     si no fueron considerados en la resolución inicial")
            lines.append("   • Aplicación de la fórmula de combinación de deficiencias")
            lines.append("     según el Art. 4.2 del RD 888/2022")
            lines.append("")
            
            # 5. Argumentación jurídica
            if judicial_val:
                judicial_pct = judicial_val['percentage']
                lines.append("5. ARGUMENTACIÓN JURÍDICA:")
                lines.append(f"   La sentencia judicial reconoce una valoración de {judicial_pct}%,")
                lines.append(f"   que es significativamente superior a la valoración administrativa")
                lines.append(f"   de {admin_pct}%. Esta sentencia constituye prueba de la infravaloración")
                lines.append(f"   inicial y debe ser aportada como nueva prueba en la reclamación.")
                lines.append("")
            
            # 6. Plazo y procedimiento
            lines.append("6. PLAZO Y PROCEDIMIENTO:")
            lines.append("   • Reclamación Previa: 1 mes desde la notificación de la resolución")
            lines.append("   • Recurso Administrativo: 1 mes desde la resolución de la reclamación")
            lines.append("   • Se recomienda asesoramiento jurídico especializado")
            lines.append("")
        
        # Observaciones generales
        lines.append("OBSERVACIONES GENERALES:")
        lines.append("-" * 80)
        lines.append("")
        lines.append("NOTA IMPORTANTE:")
        lines.append("Este informe ha sido generado automáticamente mediante análisis de IA.")
        lines.append("Los porcentajes y clasificaciones son estimaciones basadas en los datos")
        lines.append("extraídos de los documentos y deben ser revisados por un profesional")
        lines.append("médico-legal calificado antes de su uso en procedimientos.")
        lines.append("")
        lines.append("Las valoraciones pueden requerir ajustes según:")
        lines.append("  • Baremo de Limitaciones en la Actividad (BLA) - Anexo IV")
        lines.append("  • Baremo de Restricciones en la Participación (BRP) - Anexo V")
        lines.append("  • Baremo de Factores Contextuales y Barreras Ambientales (BFCA) - Anexo VI")
        lines.append("")
        lines.append("Se recomienda consultar la jurisprudencia aplicable y los criterios")
        lines.append("específicos del RD 888/2022 para cada patología valorada.")
        lines.append("")
        
        return lines
    
    def _generate_footer(self) -> List[str]:
        """Genera el pie de página del informe"""
        fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        return [
            "=" * 80,
            f"Informe generado el {fecha_actual}",
            "JurisMed AI - Sistema de Análisis Legal-Médico basado en RD 888/2022",
            "=" * 80
        ]
