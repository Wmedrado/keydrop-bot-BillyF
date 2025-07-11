@echo off
title Keydrop Bot v3.0.0 - Instalador Automático
color 0A

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║        🤖 KEYDROP BOT PROFESSIONAL v3.0.0           ║
echo ║             Instalador de Dependências              ║
echo ╚══════════════════════════════════════════════════════╝
echo.

echo [ETAPA 1/5] Verificando Python...
python --version 2>nul
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    echo.
    echo 📥 Por favor, instale Python 3.8+ em:
    echo https://www.python.org/downloads/
    echo.
    echo Marque a opção "Add Python to PATH" durante a instalação.
    pause
    exit /b 1
) else (
    echo ✅ Python encontrado!
)

echo.
echo [ETAPA 2/5] Atualizando pip...
python -m pip install --upgrade pip --quiet
echo ✅ pip atualizado!

echo.
echo [ETAPA 3/5] Instalando Selenium e WebDriver Manager...
pip install selenium==4.15.2 webdriver-manager==4.0.1 --quiet
echo ✅ Automação instalada!

echo.
echo [ETAPA 4/5] Instalando bibliotecas auxiliares...
pip install requests==2.31.0 psutil==5.9.6 --quiet
echo ✅ Bibliotecas auxiliares instaladas!

echo.
echo [ETAPA 5/5] Verificando instalação...
python -c "import selenium; print('✅ Selenium ' + selenium.__version__ + ' - OK')" 2>nul
python -c "import webdriver_manager; print('✅ WebDriver Manager - OK')" 2>nul
python -c "import requests; print('✅ Requests - OK')" 2>nul
python -c "import psutil; print('✅ PSUtil - OK')" 2>nul

echo.
echo ╔══════════════════════════════════════════════════════╗
echo ║                ✅ INSTALAÇÃO CONCLUÍDA!              ║
echo ╚══════════════════════════════════════════════════════╝
echo.
echo 🚀 Agora você pode executar:
echo.
echo   1️⃣  KeydropBot_v3.0.0_AUTO.exe  (Executável - Recomendado)
echo   2️⃣  python keydrop_bot_desktop.py  (Script Python)
echo.
echo 💡 DICA: Use o executável para melhor experiência!
echo.
echo 📋 PRÓXIMOS PASSOS:
echo   • Execute o bot
echo   • Configure número de bots e velocidade
echo   • Ative "🏆 Participar Sorteios 1h (Contender)"
echo   • Configure Discord webhook (opcional)
echo   • Clique em "INICIAR AUTOMAÇÃO"
echo.
pause
