"""
Wrapper para FastAPI en Vercel Serverless Functions
Usa Mangum como adaptador ASGI para Vercel
"""
import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_path = Path(__file__).parent.parent / "backend"
backend_path_str = str(backend_path.resolve())
if backend_path_str not in sys.path:
    sys.path.insert(0, backend_path_str)

# Cambiar al directorio backend para imports relativos
if os.path.exists(backend_path):
    os.chdir(backend_path)

try:
    from mangum import Mangum
    from main import app
    
    # Crear handler para Vercel usando Mangum
    handler = Mangum(app, lifespan="off")
except ImportError as e:
    # Log del error para debugging
    print(f"Error importando módulos: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    # Fallback si mangum no está disponible
    try:
        from main import app
        handler = app
    except Exception as e2:
        print(f"Error crítico: {e2}", file=sys.stderr)
        traceback.print_exc()
        raise
except Exception as e:
    print(f"Error inicializando handler: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

