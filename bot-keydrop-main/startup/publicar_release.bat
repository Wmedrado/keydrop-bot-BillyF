@echo off
chcp 65001 >nul
title KeyDrop Bot - Publicar Release v2.0.1

echo.
echo  ============================================
echo   KEYDROP BOT - PUBLICAR RELEASE v2.0.1
echo  ============================================
echo   Desenvolvido por: William Medrado
echo   Discord: wmedrado
echo  ============================================
echo.

echo [1] Verificando status do Git...
git status

echo.
echo [2] Adicionando arquivos ao Git...
git add .

echo.
echo [3] Criando commit da versão final...
git commit -m "Release v2.0.1 - Versão final com executáveis e todas as funcionalidades"

echo.
echo [4] Criando tag da versão...
git tag v2.0.1

echo.
echo [5] Enviando para o repositório...
git push origin main
git push origin v2.0.1

echo.
echo  ============================================
echo   RELEASE PUBLICADO COM SUCESSO!
echo  ============================================
echo.
echo  Próximos passos:
echo  1. Acesse https://github.com/wmedrado/bot-keydrop/releases
echo  2. Clique em "Create a new release"
echo  3. Selecione a tag v2.0.1
echo  4. Use o arquivo dev/temp/release_v2.0.1_description.md como descrição
echo  5. Anexe os executáveis da pasta startup/executavel/
echo  6. Marque como "Latest Release"
echo.

pause
