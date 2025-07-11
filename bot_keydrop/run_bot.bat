@echo off
title Keydrop Bot Professional v2.1.0
color 0A

echo.
echo ====================================================================
echo  KEYDROP BOT PROFESSIONAL v2.1.0
echo  Desenvolvido por William Medrado (wmedrado)
echo ====================================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python nao encontrado!
    echo 💡 Instale Python 3.8+ de https://python.org
    pause
    exit /b 1
)

:: Check if we're in the right directory
if not exist "startup.py" (
    echo ❌ Arquivo startup.py nao encontrado!
    echo 💡 Execute este batch na pasta do projeto
    pause
    exit /b 1
)

echo 🚀 Iniciando Keydrop Bot Professional...
echo.

:: Run the startup script
python startup.py

pause
