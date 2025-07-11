@echo off
chcp 65001 >nul 2>&1
title Bot KeyDrop - Interface Moderna
color 0A
echo.
echo  ==================================================
echo   BOT KEYDROP - INTERFACE MODERNA
echo  ==================================================
echo   Desenvolvido por: Billy Franck (wmedrado)
echo   Discord: wmedrado
echo  ==================================================
echo.
echo   Iniciando interface moderna...
echo.
cd /d "%~dp0.."
python modern_gui.py
echo.
echo  ==================================================
echo   Interface moderna encerrada
echo  ==================================================
pause
