@echo off
echo 🚀 Iniciando Jira Report App...

REM Comprobar Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python no encontrado. Instala Python y marcalo en el PATH.
    pause
    exit /b
)

REM Crear entorno virtual si no existe
if not exist venv (
    echo 📦 Creando entorno virtual...
    python -m venv venv
)

REM Activar entorno
call venv\Scripts\activate

REM Instalar dependencias
echo ⬇️  Comprobando dependencias...
pip install -r requirements.txt

REM Ejecutar app
echo ✅ Ejecutando aplicación...
streamlit run app.py

pause
