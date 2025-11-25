"""
Wrapper para FastAPI en Vercel Serverless Functions
Usa Mangum como adaptador ASGI para Vercel
"""
import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent / "backend"
sys.path.insert(0, str(backend_path))

# Cambiar al directorio backend para imports relativos
os.chdir(backend_path)

try:
    from mangum import Mangum
    from main import app
    
    # Crear handler para Vercel usando Mangum
    handler = Mangum(app, lifespan="off")
except ImportError:
    # Fallback si mangum no está disponible
    from main import app
    handler = app

