@echo off
echo ========================================
echo Instalando dependencias de JurisMed AI
echo ========================================
echo.

echo [1/3] Instalando paquetes Python...
pip install -r requirements.txt

echo.
echo [2/3] Descargando modelo spaCy...
python -m spacy download es_core_news_sm

echo.
echo [3/3] Verificando instalacion...
python -c "import fastapi; import fitz; import spacy; print('✓ Todas las dependencias instaladas correctamente')"

echo.
echo ========================================
echo Instalacion completada!
echo Ahora puedes ejecutar: python run.py
echo ========================================
pause




