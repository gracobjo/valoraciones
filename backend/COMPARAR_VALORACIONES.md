# Guía para Comprobar Cómo Valora la Administración

## Métodos para Verificar la Valoración Administrativa

### 1. **Análisis del Documento de Resolución**

La resolución administrativa debe contener las siguientes secciones:

#### A. Sección "FUNDAMENTOS" o "MOTIVACIÓN"
- **Qué buscar:**
  - Diagnóstico reconocido (código CIE-10)
  - Justificación de la clase asignada
  - Referencia a los anexos del RD 888/2022 aplicados
  - Explicación de por qué se asigna ese porcentaje

- **Ejemplo de lo que debería decir:**
  ```
  "Atendiendo al diagnóstico de [código], y aplicando el Anexo III 
  del RD 888/2022, Capítulo 15 (Extremidades Superiores), se asigna 
  Clase 1 (Deficiencia leve), correspondiente a un porcentaje del 10%."
  ```

#### B. Sección "DISPOSITIVO" o "RESUELVE"
- **Qué buscar:**
  - Porcentaje final reconocido
  - Clase de deficiencia asignada
  - Referencia legal completa

### 2. **Verificación de Criterios según RD 888/2022**

#### ✅ Checklist de Verificación:

**A. Diagnóstico:**
- [ ] ¿Se mencionan TODOS los diagnósticos del informe pericial?
- [ ] ¿O solo se usa un código genérico (ej: M75.91)?
- [ ] ¿Se especifican las patologías concretas (rotura manguito, discinesia, etc.)?

**B. Metodología de Cálculo:**
- [ ] ¿Se aplica la fórmula de combinación para múltiples deficiencias?
- [ ] ¿O se valora solo una deficiencia aislada?
- [ ] ¿Se suman las deficiencias o se combinan según el RD 888/2022?

**C. Baremos Aplicados:**
- [ ] ¿Solo se aplica el Anexo III (BDGP)?
- [ ] ¿O también se consideran Anexo IV (BLA), V (BRP) y VI (BFCA)?
- [ ] ¿Se menciona el Art. 4.2 del RD 888/2022?

**D. Clasificación:**
- [ ] ¿La clase asignada corresponde al porcentaje según las tablas del RD 888/2022?
  - Clase 0: 0-9%
  - Clase 1: 10-24%
  - Clase 2: 25-49%
  - Clase 3: 50-74%
  - Clase 4: 75-100%

### 3. **Comparación con el Análisis del Sistema**

Nuestro sistema analiza:

1. **Extracción de Diagnósticos:**
   - Detecta todas las patologías mencionadas en el documento
   - Deduplica diagnósticos similares
   - Agrupa por sistema/capítulo

2. **Aplicación de Baremos:**
   - **BDGP (Anexo III):** Valoración de deficiencias
   - **BLA (Anexo IV):** Limitaciones en actividad
   - **BRP (Anexo V):** Restricciones en participación
   - **BFCA (Anexo VI):** Factores contextuales

3. **Cálculo del GDA:**
   - Fórmula de combinación para múltiples deficiencias
   - Suma de ajustes según Art. 4.2
   - Determinación de clase según BDGP

### 4. **Preguntas Clave para la Reclamación**

Si la resolución administrativa:

- ❌ **Solo menciona un diagnóstico genérico** → Error: debe valorar todas las deficiencias
- ❌ **No aplica fórmula de combinación** → Error: debe combinar múltiples deficiencias
- ❌ **No menciona BLA, BRP, BFCA** → Error: debe aplicar todos los baremos según Art. 4.2
- ❌ **Asigna clase incorrecta para el porcentaje** → Error: la clase debe corresponder al rango

### 5. **Cómo Usar Esta Información**

1. **Revisa la resolución administrativa** usando el checklist anterior
2. **Compara con el análisis de nuestro sistema** (que aparece en la interfaz)
3. **Genera el informe de inconsistencia** usando el botón en la aplicación
4. **Usa el informe generado** como fundamento para la reclamación

### 6. **Ejemplo de Análisis**

**Resolución Administrativa:**
- Diagnóstico: M75.91 (Lesión no especificada de hombro)
- Metodología: Valoración única
- Baremo: Solo Anexo III
- Resultado: 10% (Clase 1)

**Análisis del Sistema:**
- Diagnósticos: 7 deficiencias específicas detectadas
- Metodología: Fórmula de combinación RD 888/2022
- Baremos: BDGP (60.7%) + BLA + BRP + BFCA
- Resultado: 67.4% (Clase 3)

**Diferencia:** 57.4 puntos porcentuales

**Justificación de la diferencia:**
1. La administración usa diagnóstico genérico vs. 7 deficiencias específicas
2. No aplica fórmula de combinación para múltiples deficiencias
3. No considera baremos secundarios (BLA, BRP, BFCA)
4. Clasificación incorrecta según las tablas del RD 888/2022

---

**Nota:** Si el PDF de la resolución está escaneado y no se puede extraer el texto automáticamente, puedes:
1. Revisar manualmente el documento PDF
2. Usar la herramienta de comparación en la interfaz web
3. Generar el informe de inconsistencia que compara ambas metodologías




