@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════╗
echo ║     📊 NOTEBOOK VIEWER - INICIO          ║
echo ╚══════════════════════════════════════════╝
echo.

echo [1/3] Verificando dependencias...
pip show Django >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Django no encontrado. Instalando dependencias...
    echo.
    pip install Django nbformat markdown
    echo.
) else (
    echo ✓ Django instalado
)

echo.
echo [2/3] Configurando proyecto...
if not exist "templates\notebooks" mkdir "templates\notebooks"
if not exist "static\notebooks" mkdir "static\notebooks"

:: Ejecutar migraciones
python manage.py migrate --run-syncdb >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Base de datos configurada
) else (
    echo ⚠️  Ejecutando migraciones...
    python manage.py migrate
)
echo ✓ Directorios listos

echo.
echo [3/3] Iniciando servidor...
echo.
echo ╔══════════════════════════════════════════╗
echo ║  🚀 Servidor iniciado correctamente      ║
echo ║                                          ║
echo ║  📍 Abre tu navegador en:                ║
echo ║     http://localhost:8000                ║
echo ║                                          ║
echo ║  🔧 Consola de debugging activa          ║
echo ║  ⏹️  Presiona Ctrl+C para detener        ║
echo ╚══════════════════════════════════════════╝
echo.

:: Abrir navegador automáticamente después de 2 segundos
start /B timeout /t 2 >nul && start http://localhost:8000

python manage.py runserver
