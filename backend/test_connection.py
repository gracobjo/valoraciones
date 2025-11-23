"""
Script simple para verificar que el backend esté funcionando
"""
import requests
import sys

def test_backend():
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✓ Backend está funcionando correctamente")
            print(f"  Respuesta: {response.json()}")
            return True
        else:
            print(f"✗ Backend respondió con código: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("✗ No se puede conectar al backend en http://localhost:8000")
        print("  Asegúrate de que el backend esté ejecutándose:")
        print("  cd backend && python run.py")
        return False
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

if __name__ == "__main__":
    success = test_backend()
    sys.exit(0 if success else 1)




