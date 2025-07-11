@echo off
chcp 65001 >nul 2>&1
title Bot KeyDrop - Menu Principal
color 0F
mode con: cols=65 lines=25

:menu
cls
echo.
echo  ============================================================
echo   BOT KEYDROP - MENU PRINCIPAL
echo  ============================================================
echo   Desenvolvido por: William Medrado (wmedrado)
echo   Discord: wmedrado
echo   Email: willfmedrado@gmail.com
echo  ============================================================
echo.
echo   OPCOES DISPONIVEIS:
echo.
echo  1. [*] Iniciar Interface Moderna (Recomendado)
echo  2. [+] Iniciar Interface Classica
echo  3. [#] Gerar Executavel (.exe)
echo  4. [^] Abrir Pasta de Executaveis
echo  5. [?] Abrir Documentacao
echo  6. [!] Pasta de Desenvolvimento
echo  7. [X] Sair
echo.
echo  ============================================================
set /p opcao=   Escolha uma opcao (1-7): 

if "%opcao%"=="1" goto interface_moderna
if "%opcao%"=="2" goto interface_classica
if "%opcao%"=="3" goto gerar_exe
if "%opcao%"=="4" goto abrir_executaveis
if "%opcao%"=="5" goto abrir_docs
if "%opcao%"=="6" goto pasta_dev
if "%opcao%"=="7" goto sair

echo  [!] Opcao invalida! Tente novamente.
timeout /t 2 >nul
goto menu

:interface_moderna
cls
echo  [*] Iniciando Interface Moderna...
call iniciar_interface_moderna.bat
goto menu

:interface_classica
cls
echo  [+] Iniciando Interface Classica...
call iniciar_interface_classica.bat
goto menu

:gerar_exe
cls
echo  [#] Gerando Executavel...
call gerar_executavel.bat
goto menu

:abrir_executaveis
cls
echo  [^] Abrindo pasta de executaveis...
if exist "executavel" (
    explorer "executavel"
) else (
    echo  [!] Pasta de executaveis nao encontrada!
    echo  [?] Execute primeiro a opcao 3 para gerar os executaveis.
    pause
)
goto menu

:abrir_docs
cls
echo  [?] Abrindo documentacao...
cd /d "%~dp0.."
explorer "docs"
goto menu

:pasta_dev
cls
echo  [!] Abrindo pasta de desenvolvimento...
cd /d "%~dp0.."
if exist "dev" (
    explorer "dev"
) else (
    echo  [!] Pasta de desenvolvimento nao encontrada!
    pause
)
goto menu

:sair
cls
echo.
echo  ============================================================
echo   Obrigado por usar o Bot KeyDrop!
echo  ============================================================
echo   Desenvolvido por: Billy Franck (wmedrado)
echo   Discord: wmedrado
echo  ============================================================
echo.
timeout /t 3 >nul
exit
