# Guía de Depuración - Errores 500

## Cómo ver los errores del backend

Cuando recibes un error 500, el backend muestra el error completo en la terminal donde está ejecutándose.

### Pasos para depurar:

1. **Mira la terminal del backend** donde ejecutaste `python run.py`
2. **Busca el traceback completo** - debería mostrar algo como:
   ```
   Traceback (most recent call last):
     File "...", line X, in ...
   Error: ...
   ```
3. **Copia el error completo** y compártelo

### Errores comunes:

#### 1. "No module named 'docx'"
**Solución:**
```bash
pip install python-docx
```

#### 2. "not a zip file" o "bad zipfile"
**Causa:** El archivo .docx está corrupto o no es realmente un .docx
**Solución:** Abre el archivo en Word y guárdalo de nuevo como .docx

#### 3. "Error al leer el PDF"
**Causa:** PDF corrupto o protegido con contraseña
**Solución:** Verifica que el PDF se pueda abrir normalmente

#### 4. "Modelo spaCy no encontrado"
**Solución:**
```bash
python -m spacy download es_core_news_sm
```

#### 5. Error al importar fitz (PyMuPDF)
**Solución:**
```bash
pip install PyMuPDF
```

### Ver logs detallados

El backend imprime información útil:
- `Procesando archivo: nombre.pdf, tamaño: X.XXMB, tipo: pdf`
- Si hay un error, muestra el traceback completo

### Mejorar el logging

Si quieres más información, puedes agregar más `print()` en el código o usar el logging de Python.




