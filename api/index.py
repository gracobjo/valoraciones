"""
Wrapper para FastAPI en Vercel Serverless Functions
Usa Mangum como adaptador ASGI para Vercel
Versión mejorada con mejor manejo de errores y paths
"""
import sys
import os
from pathlib import Path

# Log inicial para debugging
print("=" * 80, file=sys.stderr)
print("INICIALIZANDO FUNCIÓN SERVERLESS", file=sys.stderr)
print("=" * 80, file=sys.stderr)

try:
    # Obtener el directorio actual de la función
    current_dir = Path(__file__).parent.resolve()
    project_root = current_dir.parent.resolve()
    backend_path = project_root / "backend"
    
    print(f"Current dir (api/): {current_dir}", file=sys.stderr)
    print(f"Project root: {project_root}", file=sys.stderr)
    print(f"Backend path: {backend_path}", file=sys.stderr)
    print(f"Backend exists: {os.path.exists(backend_path)}", file=sys.stderr)
    
    # Listar contenido del proyecto root para debugging
    if os.path.exists(project_root):
        print(f"Contenido de project root:", file=sys.stderr)
        for item in sorted(os.listdir(project_root))[:20]:  # Primeros 20
            item_path = project_root / item
            item_type = "DIR" if os.path.isdir(item_path) else "FILE"
            print(f"  {item_type}: {item}", file=sys.stderr)
    
    # Agregar backend al path
    if os.path.exists(backend_path):
        backend_path_str = str(backend_path.resolve())
        if backend_path_str not in sys.path:
            sys.path.insert(0, backend_path_str)
            print(f"✓ Backend agregado al path: {backend_path_str}", file=sys.stderr)
        
        # Cambiar al directorio backend
        original_cwd = os.getcwd()
        os.chdir(backend_path)
        print(f"✓ Directorio cambiado a: {backend_path}", file=sys.stderr)
    else:
        print(f"⚠️ Backend path no existe: {backend_path}", file=sys.stderr)
        # Intentar buscar backend en otras ubicaciones
        possible_paths = [
            project_root / "backend",
            current_dir / "backend",
            Path("/var/task/backend"),
            Path("/vercel/path0/backend"),
        ]
        for possible_path in possible_paths:
            if os.path.exists(possible_path):
                print(f"✓ Encontrado backend en: {possible_path}", file=sys.stderr)
                backend_path = possible_path
                sys.path.insert(0, str(possible_path))
                os.chdir(possible_path)
                break
        else:
            raise FileNotFoundError(f"Backend directory not found. Tried: {possible_paths}")
    
    # Verificar que main.py existe
    main_py = backend_path / "main.py"
    if not os.path.exists(main_py):
        raise FileNotFoundError(f"main.py not found in {backend_path}")
    print(f"✓ main.py encontrado: {main_py}", file=sys.stderr)
    
    # Intentar importar mangum
    print("\n--- Importando dependencias ---", file=sys.stderr)
    try:
        from mangum import Mangum
        print("✓ Mangum importado", file=sys.stderr)
    except ImportError as e:
        print(f"✗ ERROR importando mangum: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    
    # Intentar importar la app
    try:
        print("Importando main.app...", file=sys.stderr)
        from main import app
        print("✓ App importada correctamente", file=sys.stderr)
    except ImportError as e:
        print(f"✗ ERROR importando app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    except Exception as e:
        print(f"✗ ERROR inesperado importando app: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    
    # Crear handler
    print("\n--- Creando handler ---", file=sys.stderr)
    try:
        handler = Mangum(app, lifespan="off")
        print("✓ Handler creado correctamente", file=sys.stderr)
    except Exception as e:
        print(f"✗ ERROR creando handler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        raise
    
    print("\n" + "=" * 80, file=sys.stderr)
    print("✓ FUNCIÓN SERVERLESS INICIALIZADA CORRECTAMENTE", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
    
except Exception as e:
    print("\n" + "=" * 80, file=sys.stderr)
    print("✗ ERROR CRÍTICO EN INICIALIZACIÓN", file=sys.stderr)
    print("=" * 80, file=sys.stderr)
    print(f"Error: {e}", file=sys.stderr)
    import traceback
    traceback.print_exc(file=sys.stderr)
    
    # Crear una app de fallback que muestre el error
    try:
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
                    "path": path,
                    "traceback": traceback.format_exc()
                }
            )
        
        if 'Mangum' in globals():
            handler = Mangum(error_app, lifespan="off")
        else:
            handler = error_app
    except:
        # Si incluso el fallback falla, crear un handler mínimo
        def handler(event, context):
            return {
                "statusCode": 500,
                "body": f"Error crítico: {str(e)}"
            }
