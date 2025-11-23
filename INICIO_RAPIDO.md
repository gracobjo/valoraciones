# 🚀 Inicio Rápido - JurisMed AI

## Paso 1: Arrancar el Backend

Abre una **terminal** (PowerShell, CMD, o terminal de tu editor) y ejecuta:

```bash
cd backend
python run.py
```

**O alternativamente:**

```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### ✅ Verificación

Deberías ver algo como:

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 🌐 Probar que funciona

Abre en tu navegador: **http://localhost:8000/docs**

Deberías ver la documentación interactiva de la API (Swagger UI).

---

## Paso 2: Arrancar el Frontend

Abre **otra terminal** (deja la del backend abierta) y ejecuta:

```bash
cd frontend
npm run dev
```

### ✅ Verificación

Deberías ver algo como:

```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:3000/
  ➜  Network: use --host to expose
```

### 🌐 Abrir la aplicación

Abre en tu navegador: **http://localhost:3000**

---

## ⚠️ Si tienes problemas

### Error: "No module named 'fastapi'"

Instala las dependencias:

```bash
cd backend
pip install -r requirements.txt
python -m spacy download es_core_news_sm
```

### Error: "npm: command not found"

Instala Node.js desde: https://nodejs.org/

### Error: Puerto 8000 ya en uso

Cierra el proceso que está usando el puerto o cambia el puerto en `backend/run.py`.

### Error: "Modelo spaCy no encontrado"

```bash
python -m spacy download es_core_news_sm
```

---

## 📋 Resumen

1. **Terminal 1**: `cd backend && python run.py` → Backend en http://localhost:8000
2. **Terminal 2**: `cd frontend && npm run dev` → Frontend en http://localhost:3000
3. **Navegador**: Abre http://localhost:3000

¡Listo! Ya puedes cargar tus documentos PDF.




