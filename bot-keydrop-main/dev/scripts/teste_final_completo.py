#!/usr/bin/env python3
"""
Teste final completo do KeyDrop Bot v2.0.1
"""

import os
import sys
import json
import subprocess
from pathlib import Path

def teste_completo():
    """Executa todos os testes necessários"""
    print("=" * 60)
    print("TESTE COMPLETO - KEYDROP BOT v2.0.1")
    print("=" * 60)
    
    base_dir = Path(__file__).parent.parent.parent
    testes_passaram = 0
    total_testes = 0
    
    # Teste 1: Verificar se version.json está correto
    total_testes += 1
    print(f"\n[{total_testes}] Verificando version.json...")
    try:
        with open(base_dir / "version.json", "r", encoding="utf-8") as f:
            version_data = json.load(f)
        
        if version_data["version"] == "2.0.1":
            print("✅ Versão correta: 2.0.1")
            testes_passaram += 1
        else:
            print(f"❌ Versão incorreta: {version_data['version']}")
    except Exception as e:
        print(f"❌ Erro ao ler version.json: {e}")
    
    # Teste 2: Verificar se os executáveis existem
    total_testes += 1
    print(f"\n[{total_testes}] Verificando executáveis...")
    
    exec_moderno = base_dir / "startup" / "executavel" / "KeyDrop_Bot_Moderno.exe"
    exec_classico = base_dir / "startup" / "executavel" / "KeyDrop_Bot_Classico.exe"
    
    if exec_moderno.exists() and exec_classico.exists():
        print("✅ Ambos os executáveis existem")
        print(f"   - Moderno: {exec_moderno.stat().st_size / 1024 / 1024:.2f} MB")
        print(f"   - Clássico: {exec_classico.stat().st_size / 1024 / 1024:.2f} MB")
        testes_passaram += 1
    else:
        print("❌ Executáveis não encontrados")
    
    # Teste 3: Verificar se o ícone existe
    total_testes += 1
    print(f"\n[{total_testes}] Verificando ícone...")
    
    icone_ico = base_dir / "bot-icone.ico"
    icone_png = base_dir / "bot-icone.png"
    
    if icone_ico.exists() and icone_png.exists():
        print("✅ Ícones encontrados")
        print(f"   - ICO: {icone_ico.stat().st_size / 1024:.2f} KB")
        print(f"   - PNG: {icone_png.stat().st_size / 1024:.2f} KB")
        testes_passaram += 1
    else:
        print("❌ Ícones não encontrados")
    
    # Teste 4: Verificar se github_token.txt está configurado
    total_testes += 1
    print(f"\n[{total_testes}] Verificando token do GitHub...")
    
    token_file = base_dir / "github_token.txt"
    if token_file.exists():
        token = token_file.read_text().strip()
        if token and len(token) > 10:
            print("✅ Token do GitHub configurado")
            testes_passaram += 1
        else:
            print("❌ Token do GitHub vazio")
    else:
        print("❌ Arquivo github_token.txt não encontrado")
    
    # Teste 5: Verificar se o README está atualizado
    total_testes += 1
    print(f"\n[{total_testes}] Verificando README...")
    
    readme_file = base_dir / "README.md"
    if readme_file.exists():
        readme_content = readme_file.read_text(encoding="utf-8")
        if "2.0.1" in readme_content and "wmedrado" in readme_content:
            print("✅ README atualizado com versão e contato")
            testes_passaram += 1
        else:
            print("❌ README não atualizado")
            print(f"   - Versão 2.0.1: {'✅' if '2.0.1' in readme_content else '❌'}")
            print(f"   - Contato wmedrado: {'✅' if 'wmedrado' in readme_content else '❌'}")
    else:
        print("❌ README.md não encontrado")
    
    # Teste 6: Verificar estrutura de pastas
    total_testes += 1
    print(f"\n[{total_testes}] Verificando estrutura de pastas...")
    
    pastas_obrigatorias = ["startup", "dev", "src", "docs"]
    pastas_existem = all((base_dir / pasta).exists() for pasta in pastas_obrigatorias)
    
    if pastas_existem:
        print("✅ Estrutura de pastas correta")
        testes_passaram += 1
    else:
        print("❌ Estrutura de pastas incorreta")
    
    # Resultado final
    print("\n" + "=" * 60)
    print(f"RESULTADO FINAL: {testes_passaram}/{total_testes} testes passaram")
    print("=" * 60)
    
    if testes_passaram == total_testes:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ KeyDrop Bot v2.0.1 está pronto para release!")
        return True
    else:
        print("❌ Alguns testes falharam. Verifique os problemas acima.")
        return False

if __name__ == "__main__":
    sucesso = teste_completo()
    sys.exit(0 if sucesso else 1)
