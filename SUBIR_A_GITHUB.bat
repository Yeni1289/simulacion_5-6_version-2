@echo off
chcp 65001 >nul
cls
echo.
echo ╔══════════════════════════════════════════════════════════════╗
echo ║   🚀 SUBIR PROYECTO A GITHUB                                 ║
echo ╚══════════════════════════════════════════════════════════════╝
echo.
echo Este script te ayudará a subir el proyecto a GitHub paso a paso.
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 1: Verificando Git...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Git no está instalado.
    echo.
    echo Por favor instala Git desde: https://git-scm.com/download/win
    echo Después vuelve a ejecutar este script.
    echo.
    pause
    exit /b 1
)
git --version
echo ✓ Git está instalado
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 2: Inicializando repositorio Git...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if exist ".git" (
    echo.
    echo ⚠️  El repositorio Git ya existe.
    echo ¿Deseas reinicializarlo? (S/N)
    set /p reinit=
    if /i "%reinit%"=="S" (
        rmdir /s /q .git
        git init
        echo ✓ Repositorio reinicializado
    ) else (
        echo ✓ Usando repositorio existente
    )
) else (
    git init
    echo ✓ Repositorio Git inicializado
)
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 3: Agregando archivos al repositorio...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git add .
echo ✓ Archivos agregados
echo.
git status
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 4: Haciendo commit...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git commit -m "Initial commit: Notebook Viewer con interfaz moderna"
echo ✓ Commit creado
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 5: Conectando con GitHub...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo Tu repositorio de GitHub es:
echo https://github.com/Yeni1289/simulacion_5-6_version-2
echo.

REM Verificar si ya existe el remoto
git remote get-url origin >nul 2>&1
if %errorlevel% equ 0 (
    echo ⚠️  El remoto 'origin' ya existe.
    echo Removiendo remoto anterior...
    git remote remove origin
)

git remote add origin https://github.com/Yeni1289/simulacion_5-6_version-2.git
echo ✓ Conectado con GitHub
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 6: Cambiando a rama main...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
git branch -M main
echo ✓ Rama cambiada a 'main'
echo.
pause

echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo   PASO 7: Subiendo a GitHub...
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.
echo IMPORTANTE:
echo Si te pide credenciales, usa:
echo   - Usuario: Yeni1289
echo   - Contraseña: Tu Personal Access Token (NO tu contraseña de GitHub)
echo.
echo ¿Si no tienes un token, créalo en:
echo   GitHub → Settings → Developer settings → Personal access tokens
echo.
pause
echo.
echo Subiendo archivos...
git push -u origin main

if %errorlevel% equ 0 (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║   ✅ ¡ÉXITO! Proyecto subido a GitHub                        ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo Verifica en: https://github.com/Yeni1289/simulacion_5-6_version-2
    echo.
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo   📋 SIGUIENTE PASO: DESPLEGAR EN RAILWAY
    echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    echo.
    echo 1. Ve a: https://railway.app
    echo 2. Click "New Project" → "Deploy from GitHub repo"
    echo 3. Selecciona: simulacion_5-6_version-2
    echo 4. ¡Listo! Railway hará el deploy automáticamente
    echo.
    echo Lee GUIA_DEPLOY.txt para más detalles.
    echo.
) else (
    echo.
    echo ╔══════════════════════════════════════════════════════════════╗
    echo ║   ❌ ERROR al subir a GitHub                                 ║
    echo ╚══════════════════════════════════════════════════════════════╝
    echo.
    echo Posibles soluciones:
    echo 1. Verifica tu conexión a internet
    echo 2. Asegúrate de usar un Personal Access Token, no tu contraseña
    echo 3. Verifica que el repositorio existe en GitHub
    echo 4. Lee GUIA_DEPLOY.txt para más ayuda
    echo.
)

pause
