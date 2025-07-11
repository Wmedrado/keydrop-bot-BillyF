@echo off
chcp 65001 > nul
title Teste de Salvamento de Configuracoes

echo.
echo ===========================================================
echo    TESTE DE SALVAMENTO E CARREGAMENTO DE CONFIGURACOES
echo ===========================================================
echo.

cd /d "%~dp0\..\.."

echo Executando teste de salvamento...
python "dev\scripts\teste_salvamento_config.py"

echo.
echo Teste concluido!
echo.
pause
