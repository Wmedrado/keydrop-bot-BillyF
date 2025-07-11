@echo off
chcp 65001 >nul
title KeyDrop Bot - Modo CONTENDER

echo.
echo 🎯 KeyDrop Bot - Modo CONTENDER
echo 👨‍💻 Desenvolvido por: Billy Franck (wmedrado)
echo 📞 Discord: wmedrado
echo.

REM Mudar para o diretório do script
cd /d "%~dp0"

REM Verificar se Python está instalado
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não está instalado ou não está no PATH
    echo 📥 Baixe Python em: https://python.org/downloads/
    pause
    exit /b 1
)

REM Verificar se o arquivo do contender existe
if not exist "contender_corrigido.py" (
    echo ❌ Arquivo contender_corrigido.py não encontrado
    pause
    exit /b 1
)

REM Executar o script do contender
echo 🚀 Iniciando modo CONTENDER...
echo.

python executar_contender.py

echo.
echo ✅ Modo CONTENDER finalizado
pause
