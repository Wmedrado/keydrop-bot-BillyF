@echo off
chcp 65001 >nul 2>&1
title Bot KeyDrop - Gerador de Executavel
color 0B
echo.
echo  ==================================================
echo   BOT KEYDROP - GERADOR DE EXECUTAVEL
echo  ==================================================
echo   Desenvolvido por: Billy Franck (wmedrado)
echo   Discord: wmedrado
echo  ==================================================
echo.
echo   Verificando dependencias...
echo.

REM Verificar se o PyInstaller está instalado
python -c "import PyInstaller" 2>nul
if %errorlevel% neq 0 (
    echo  [!] PyInstaller nao encontrado!
    echo  [#] Instalando PyInstaller...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo  [!] Erro ao instalar PyInstaller!
        pause
        exit /b 1
    )
)

echo  [*] PyInstaller encontrado!
echo.
echo   Gerando executavel...
echo.

cd /d "%~dp0.."

REM Criar executável da interface moderna
echo   Compilando interface moderna...
pyinstaller --onefile --windowed --icon="bot-icone.ico" --add-data="bot-icone.ico;." --add-data="bot-icone.png;." --add-data="github_token.txt;." --name="KeyDrop_Bot_Moderno" --distpath="startup/executavel" modern_gui.py

REM Criar executável da interface clássica
echo   Compilando interface classica...
pyinstaller --onefile --windowed --icon="bot-icone.ico" --add-data="bot-icone.ico;." --add-data="bot-icone.png;." --add-data="github_token.txt;." --name="KeyDrop_Bot_Classico" --distpath="startup/executavel" gui_keydrop.py

REM Limpar arquivos temporários
echo   Limpando arquivos temporarios...
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"

echo.
echo  ==================================================
echo   EXECUTAVEIS GERADOS COM SUCESSO!
echo  ==================================================
echo.
echo   Localizacao: startup/executavel/
echo   KeyDrop_Bot_Moderno.exe - Interface Moderna
echo   KeyDrop_Bot_Classico.exe - Interface Classica
echo.
echo  ==================================================
echo   DICAS:
echo  • Execute os .exe diretamente
echo  • Mantenha os arquivos de config no mesmo diretorio
echo  • Use a interface moderna para melhor experiencia
echo  ==================================================
echo.
pause
explorer "startup\executavel"
