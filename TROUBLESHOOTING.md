# Solución de Problemas - JurisMed AI

## Error: ERR_CONNECTION_RESET

Este error indica que la conexión con el backend se interrumpió. Sigue estos pasos:

### 1. Verificar que el backend esté ejecutándose

```bash
# En una terminal, ejecuta:
cd backend
python test_connection.py
```

Si no está funcionando, inicia el backend:

```bash
cd backend
python run.py
# O alternativamente:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2. Verificar que el puerto 8000 esté libre

En Windows (PowerShell):
```powershell
netstat -ano | findstr :8000
```

En Linux/Mac:
```bash
lsof -i :8000
```

Si hay otro proceso usando el puerto, detén ese proceso o cambia el puerto en `backend/run.py`.

### 3. Verificar CORS

Asegúrate de que en `backend/main.py` esté configurado:

```python
allow_origins=["http://localhost:3000", "http://localhost:5173"],
```

### 4. Verificar el tamaño del archivo

El backend acepta archivos hasta 50MB. Si tu PDF es más grande:
- Comprime el PDF
- Divide el documento en partes más pequeñas
- Aumenta el límite en `backend/main.py` (línea donde se verifica `file_size`)

### 5. Verificar logs del backend

Cuando cargas un archivo, el backend debería mostrar logs como:
```
Procesando archivo: sentencia.pdf, tamaño: 2.45MB
```

Si ves errores en los logs, compártelos para diagnosticar el problema.

### 6. Probar el endpoint directamente

Puedes probar el endpoint con curl:

```bash
curl -X POST "http://localhost:8000/api/analyze/document" \
  -F "file=@ruta/a/tu/archivo.pdf" \
  -F "document_type=judicial"
```

### 7. Verificar dependencias

Asegúrate de que todas las dependencias estén instaladas:

```bash
cd backend
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

## Error: "No se pudo extraer texto del documento"

- El PDF puede estar escaneado y requerir OCR más avanzado
- El PDF puede estar corrupto
- El PDF puede estar protegido con contraseña

Solución: Verifica que el PDF sea válido y no esté protegido.

## Error: Timeout

Si el análisis tarda demasiado:
- El archivo puede ser muy grande
- El modelo NLP puede estar cargándose por primera vez
- El OCR puede estar procesando muchas páginas

Solución: Espera un poco más o verifica los logs del backend.

## Error: "Modelo spaCy no encontrado"

```bash
python -m spacy download es_core_news_sm
```

O para mejor calidad:
```bash
python -m spacy download es_core_news_lg
```

## Verificar que todo funciona

1. Backend corriendo: http://localhost:8000/docs
2. Frontend corriendo: http://localhost:3000
3. Backend responde: http://localhost:8000/health

Si todos estos pasos funcionan pero aún tienes problemas, revisa la consola del navegador (F12) para ver errores específicos.




