@echo off
REM Instalação dos requisitos para o Keydrop Bot Professional
REM Este script instala todas as dependências necessárias para rodar o bot
REM Execute como administrador se necessário

REM Verifica se o Python está instalado
python --version >nul 2>&1
IF ERRORLEVEL 1 (
    echo [ERRO] Python não encontrado! Instale o Python 3.8+ antes de continuar.
    pause
    exit /b 1
)

REM Atualiza o pip
python -m pip install --upgrade pip

REM Instala dependências principais
python -m pip install selenium webdriver-manager psutil requests

REM Instala dependências opcionais para gráficos (matplotlib)
python -m pip install matplotlib

REM Mensagem final
@echo.
echo [OK] Todos os requisitos foram instalados!
echo Agora você pode rodar o Keydrop Bot normalmente.
pause
