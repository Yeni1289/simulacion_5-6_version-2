@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════╗
echo ║   🔧 CONFIGURACIÓN INICIAL               ║
echo ╚══════════════════════════════════════════╝
echo.

echo [1/4] Instalando dependencias...
pip install -q Django nbformat markdown
if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias
    pause
    exit /b 1
)
echo ✓ Dependencias instaladas

echo.
echo [2/4] Creando directorios...
if not exist "templates\notebooks" mkdir "templates\notebooks"
if not exist "static\notebooks" mkdir "static\notebooks"
echo ✓ Directorios creados

echo.
echo [3/4] Configurando base de datos...
python manage.py migrate --run-syncdb
if %errorlevel% neq 0 (
    echo ❌ Error en configuración
    pause
    exit /b 1
)
echo ✓ Base de datos configurada

echo.
echo [4/4] Verificando instalación...
python -c "import django; print('Django version:', django.get_version())"
echo ✓ Todo listo

echo.
echo ╔══════════════════════════════════════════╗
echo ║   ✅ CONFIGURACIÓN COMPLETADA            ║
echo ║                                          ║
echo ║   Para iniciar el servidor ejecuta:      ║
echo ║   INICIAR.bat                            ║
echo ╚══════════════════════════════════════════╝
echo.

pause
