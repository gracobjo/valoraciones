# Solución: Error al leer documentos Word

## Error: "Error al leer el documento Word. Verifica que sea un archivo .docx válido."

Este error ocurre cuando intentas subir un archivo Word que no es compatible.

### Causas comunes:

1. **Archivo .doc (formato antiguo)**: Los archivos `.doc` (Word 97-2003) no están soportados directamente
2. **Archivo .docx corrupto**: El archivo puede estar dañado
3. **Archivo no es realmente Word**: Puede ser otro formato con extensión .docx

## Soluciones:

### Opción 1: Convertir .doc a .docx (Recomendado)

1. Abre el archivo en Microsoft Word
2. Ve a **Archivo** → **Guardar como**
3. En el menú desplegable de formato, selecciona **"Documento de Word (.docx)"**
4. Guarda el archivo
5. Sube el nuevo archivo .docx

### Opción 2: Convertir a PDF

1. Abre el archivo en Microsoft Word
2. Ve a **Archivo** → **Guardar como**
3. Selecciona formato **PDF**
4. Guarda el archivo
5. Sube el archivo PDF

### Opción 3: Usar conversor online

Si no tienes Word instalado:
- [CloudConvert](https://cloudconvert.com/doc-to-docx)
- [Zamzar](https://www.zamzar.com/convert/doc-to-docx/)
- [Online-Convert](https://www.online-convert.com/)

### Verificar que el archivo sea válido

Antes de subir:
1. Abre el archivo en Word o en un visor
2. Verifica que se abra correctamente
3. Si muestra errores, el archivo está corrupto

## Formatos soportados:

✅ **PDF** - Totalmente soportado (nativos y escaneados)
✅ **DOCX** - Soportado (formato moderno de Word 2007+)
❌ **DOC** - No soportado (formato antiguo Word 97-2003 - debe convertirse)

### ⚠️ Importante sobre archivos .doc

Los archivos `.doc` (formato binario antiguo de Word) **NO están soportados** porque:
- Usan un formato binario propietario diferente
- La librería `python-docx` solo puede leer `.docx` (formato XML comprimido)
- Requeriría librerías adicionales complejas

**Solución obligatoria:** Convertir a `.docx` o `PDF` antes de subir.

## Nota técnica:

Los archivos `.doc` usan un formato binario propietario diferente a `.docx` (que es XML comprimido). 
La librería `python-docx` solo puede leer `.docx`, por eso necesitas convertir los archivos `.doc` antiguos.

