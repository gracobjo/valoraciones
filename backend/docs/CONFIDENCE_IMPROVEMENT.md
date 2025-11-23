# Mejora de la Confianza en el Análisis Legal-Médico

## Cómo se Calcula Actualmente la Confianza

### 1. Confianza por Diagnóstico Individual

La confianza se calcula en `_classify_diagnosis()` basándose en varios factores:

#### Factores que AUMENTAN la confianza (0.7-0.8):
- **Métricas ROM objetivas detectadas**: Si hay valores de rango de movimiento (flexión, abducción, etc.), confianza = 0.8
- **Fuerza muscular medida**: Si hay balance muscular (0-5), confianza = 0.7
- **Patologías anatómicas específicas**: Rotura de manguito, hernia discal, etc., confianza = 0.6-0.7
- **Agrupación de diagnósticos**: Si se agrupan síntomas relacionados, confianza aumenta

#### Factores que DISMINUYEN la confianza (0.4-0.5):
- **Solo adjetivos descriptivos**: "grave", "severa" sin métricas objetivas, confianza = 0.4
- **Deficiencias funcionales sin causa anatómica**: confianza = 0.5
- **Sin métricas ni patología específica**: confianza = 0.4-0.5

### 2. Confianza Global

La confianza global se calcula como:
```python
avg_confidence = statistics.mean(confidences)  # Promedio simple
# Penalización si hay muchas deficiencias pequeñas
if len(percentages) > 3:
    avg_confidence *= 0.9
```

## Estrategias para Mejorar la Confianza

### 1. Mejoras Inmediatas (Sin Modelos de IA)

#### A. Extracción Mejorada de Métricas
- **Problema actual**: Las métricas ROM pueden no detectarse correctamente
- **Solución**: Mejorar patrones regex para capturar más variaciones:
  - "Flexión: 90°" vs "90 grados de flexión" vs "flexión de 90°"
  - Capturar valores en tablas estructuradas
  - Detectar rangos de movimiento combinados

#### B. Validación Cruzada de Diagnósticos
- Comparar diagnósticos extraídos con:
  - Códigos CIE-10 detectados
  - Valoraciones previas mencionadas en el documento
  - Consistencia entre diferentes secciones del documento

#### C. Análisis de Contexto
- Detectar si el diagnóstico está en:
  - Sección de "Diagnóstico" (alta confianza)
  - Sección de "Antecedentes" (media confianza)
  - Sección de "Exploración" (alta confianza si hay métricas)
  - Sección de "Conclusiones" (alta confianza)

### 2. Modelos de IA Especializados

#### Opción A: Modelos de Lenguaje Especializados en Medicina

**Modelos Recomendados:**

1. **BioBERT / ClinicalBERT**
   - Pre-entrenado en textos médicos
   - Mejor comprensión de terminología médica
   - Puede identificar relaciones causa-efecto

2. **SpaCy + Modelo Médico**
   - `en_core_sci_md` o `es_core_sci_md` (si existe)
   - NER (Named Entity Recognition) especializado
   - Mejor extracción de entidades médicas

3. **MedBERT / PubMedBERT**
   - Entrenados en literatura médica
   - Excelente para clasificación de diagnósticos

#### Opción B: Modelos de Clasificación Fine-Tuned

**Enfoque:**
1. Recopilar dataset de casos reales de RD 888/2022
2. Etiquetar: diagnóstico → capítulo → clase → porcentaje
3. Fine-tune de un modelo base (BERT, RoBERTa) en español
4. Entrenar específicamente para valoración legal-médica

**Ventajas:**
- Alta precisión en casos similares a los entrenados
- Aprende patrones específicos del baremo
- Puede generalizar a casos nuevos

**Desafíos:**
- Requiere dataset grande y etiquetado
- Necesita expertos médicos-legales para etiquetar
- Coste computacional

#### Opción C: Modelos de Embeddings + Similaridad Semántica

**Enfoque:**
1. Usar embeddings de modelos médicos (BioBERT, etc.)
2. Crear base de conocimiento de casos de referencia
3. Comparar similitud semántica con casos conocidos
4. Asignar confianza basada en similitud

**Ventajas:**
- No requiere entrenamiento
- Puede usar casos de referencia del baremo
- Interpretable (muestra casos similares)

### 3. Sistema Híbrido (Recomendado)

Combinar reglas basadas en conocimiento + IA:

```
1. Extracción con NLP mejorado (SpaCy + modelo médico)
   ↓
2. Clasificación con reglas (actual) + modelo fine-tuned
   ↓
3. Validación cruzada con casos de referencia
   ↓
4. Cálculo de confianza ponderado:
   - Confianza de extracción: 30%
   - Confianza de clasificación: 40%
   - Confianza de validación: 30%
```

## Implementación Práctica

### Fase 1: Mejoras Inmediatas (1-2 semanas)
1. ✅ Mejorar extracción de métricas ROM
2. ✅ Añadir detección de secciones del documento
3. ✅ Validación cruzada con códigos CIE-10
4. ✅ Mejorar cálculo de confianza (ponderado)

### Fase 2: Integración de Modelos Médicos (1 mes)
1. Integrar SpaCy con modelo médico (si disponible en español)
2. Usar embeddings de BioBERT/ClinicalBERT para similitud
3. Crear base de conocimiento de casos de referencia

### Fase 3: Fine-Tuning (2-3 meses)
1. Recopilar dataset de casos reales
2. Etiquetar con expertos
3. Fine-tune modelo BERT en español
4. Validar con casos de prueba

## Código de Ejemplo: Mejora de Confianza

```python
def calculate_enhanced_confidence(self, diagnosis, metrics, context):
    """
    Calcula confianza mejorada considerando múltiples factores
    """
    confidence_factors = {
        'extraction': 0.0,  # Calidad de extracción
        'metrics': 0.0,     # Presencia de métricas objetivas
        'classification': 0.0,  # Calidad de clasificación
        'validation': 0.0   # Validación cruzada
    }
    
    # 1. Confianza de extracción (30%)
    if diagnosis.get('source') == 'whitelist':
        confidence_factors['extraction'] = 0.9
    elif diagnosis.get('source') == 'pattern':
        confidence_factors['extraction'] = 0.7
    else:
        confidence_factors['extraction'] = 0.5
    
    # 2. Confianza por métricas (30%)
    if metrics:
        if any(m in metrics for m in ['abduccion', 'flexion', 'extension']):
            confidence_factors['metrics'] = 0.9
        elif 'fuerza' in metrics:
            confidence_factors['metrics'] = 0.8
        else:
            confidence_factors['metrics'] = 0.6
    else:
        confidence_factors['metrics'] = 0.4
    
    # 3. Confianza de clasificación (25%)
    # Basada en patología específica vs genérica
    if any(kw in diagnosis.get('normalized_text', '') 
           for kw in ['rotura manguito', 'hernia discal']):
        confidence_factors['classification'] = 0.8
    else:
        confidence_factors['classification'] = 0.6
    
    # 4. Confianza de validación (15%)
    # Validación cruzada con códigos CIE-10, valoraciones previas, etc.
    if context.get('cie_code'):
        confidence_factors['validation'] = 0.8
    elif context.get('previous_valuation'):
        confidence_factors['validation'] = 0.7
    else:
        confidence_factors['validation'] = 0.5
    
    # Cálculo ponderado
    weights = {
        'extraction': 0.30,
        'metrics': 0.30,
        'classification': 0.25,
        'validation': 0.15
    }
    
    final_confidence = sum(
        confidence_factors[factor] * weights[factor]
        for factor in confidence_factors
    )
    
    return min(final_confidence, 0.95)  # Máximo 95%
```

## Recursos y Herramientas

### Modelos Pre-entrenados Disponibles:
1. **Hugging Face Models:**
   - `dccuchile/bert-base-spanish-wwm-uncased` (BERT en español)
   - `PlanTL-GOB-ES/roberta-base-bne` (RoBERTa en español)
   - `microsoft/BiomedNLP-PubMedBERT-base-uncased-abstract-fulltext` (médico, inglés)

2. **SpaCy Models:**
   - `es_core_news_md` (español general)
   - Buscar modelos médicos en español

3. **Bibliotecas:**
   - `transformers` (Hugging Face)
   - `spacy` (NLP)
   - `scikit-learn` (clasificación)
   - `sentence-transformers` (embeddings)

### Datasets de Referencia:
- Casos reales de RD 888/2022 (anónimos)
- Baremo oficial con ejemplos
- Jurisprudencia relacionada

## Conclusión

La confianza actual (55% en tu ejemplo) puede mejorarse significativamente mediante:

1. **Corto plazo**: Mejoras en extracción y validación → **+15-20% confianza**
2. **Medio plazo**: Integración de modelos médicos → **+20-30% confianza**
3. **Largo plazo**: Fine-tuning específico → **+30-40% confianza**

**Objetivo realista**: Llegar a 75-85% de confianza con mejoras incrementales.

