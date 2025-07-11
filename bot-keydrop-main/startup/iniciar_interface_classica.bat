@echo off
chcp 65001 >nul 2>&1
title Bot KeyDrop - Interface Classica
color 0E
echo.
echo  ==================================================
echo   BOT KEYDROP - INTERFACE CLASSICA
echo  ==================================================
echo   Desenvolvido por: Billy Franck (wmedrado)
echo   Discord: wmedrado
echo  ==================================================
echo.
echo   Iniciando interface classica...
echo.
cd /d "%~dp0.."
python gui_keydrop.py
echo.
echo  ==================================================
echo   Interface classica encerrada
echo  ==================================================
pause
