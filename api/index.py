"""
Wrapper para FastAPI en Vercel Serverless Functions
Usa Mangum como adaptador ASGI para Vercel
Versión mejorada con mejor manejo de errores
"""
import sys
import os
from pathlib import Path

# Log inicial para debugging
print("Inicializando función serverless...", file=sys.stderr)

try:
    # Agregar el directorio backend al path
    backend_path = Path(__file__).parent.parent / "backend"
    backend_path_str = str(backend_path.resolve())
    
    print(f"Backend path: {backend_path_str}", file=sys.stderr)
    print(f"Backend path exists: {os.path.exists(backend_path)}", file=sys.stderr)
    
    if backend_path_str not in sys.path:
        sys.path.insert(0, backend_path_str)
        print(f"Agregado al path: {backend_path_str}", file=sys.stderr)
    
    # Cambiar al directorio backend para imports relativos
    if os.path.exists(backend_path):
        original_cwd = os.getcwd()
        os.chdir(backend_path)
        print(f"Cambiado directorio a: {backend_path}", file=sys.stderr)
    else:
        print(f"ERROR: Backend path no existe: {backend_path}", file=sys.stderr)
        raise FileNotFoundError(f"Backend directory not found: {backend_path}")
    
    # Intentar importar mangum
    print("Importando mangum...", file=sys.stderr)
    try:
        from mangum import Mangum
        print("Mangum importado correctamente", file=sys.stderr)
    except ImportError as e:
        print(f"ERROR importando mangum: {e}", file=sys.stderr)
        raise
    
    # Intentar importar la app
    print("Importando main.app...", file=sys.stderr)
    try:
        from main import app
        print("App importada correctamente", file=sys.stderr)
    except ImportError as e:
        print(f"ERROR importando app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    
    # Crear handler para Vercel usando Mangum
    print("Creando handler Mangum...", file=sys.stderr)
    try:
        handler = Mangum(app, lifespan="off")
        print("Handler creado correctamente", file=sys.stderr)
    except Exception as e:
        print(f"ERROR creando handler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    
    print("Función serverless inicializada correctamente", file=sys.stderr)
    
except Exception as e:
    print(f"ERROR CRÍTICO en inicialización: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    
    # Crear una app de fallback que muestre el error
    from fastapi import FastAPI
    from fastapi.responses import JSONResponse
    
    error_app = FastAPI()
    
    @error_app.get("/{path:path}")
    @error_app.post("/{path:path}")
    async def error_handler(path: str):
        return JSONResponse(
            status_code=500,
            content={
                "error": "Error inicializando la aplicación",
                "message": str(e),
                "path": path
            }
        )
    
    handler = Mangum(error_app, lifespan="off") if 'Mangum' in globals() else error_app
