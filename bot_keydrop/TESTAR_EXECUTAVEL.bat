@echo off
echo ========================================
echo   KEYDROP BOT PROFESSIONAL v2.1.0
echo   Teste Final do Executavel
echo ========================================
echo.
echo Desenvolvido por: William Medrado
echo.
echo Testando executavel...
echo.

cd /d "%~dp0dist"

if exist "KeydropBot_Desktop_v2.1.0.exe" (
    echo ✅ Executavel encontrado!
    echo 🚀 Iniciando aplicacao...
    echo.
    start "" "KeydropBot_Desktop_v2.1.0.exe"
    echo.
    echo ✅ Aplicacao iniciada!
    echo 📱 A interface grafica deve aparecer agora.
    echo.
    echo 💡 Se a interface nao abrir:
    echo    1. Verifique se o antivirus nao esta bloqueando
    echo    2. Execute como administrador
    echo    3. Consulte o README_FINAL.md
    echo.
) else (
    echo ❌ Executavel nao encontrado!
    echo 📁 Verifique se esta na pasta correta
    echo.
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul
