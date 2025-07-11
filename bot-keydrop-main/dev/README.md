# 🛠️ PASTA DE DESENVOLVIMENTO

## 📋 **Descrição:**
Esta pasta é destinada a todos os arquivos temporários, testes, scripts de desenvolvimento e experimentos. Ela mantém o projeto principal limpo e organizado.

## 📁 **Estrutura:**

### 🧪 **tests/**
- Todos os arquivos de teste
- Scripts de validação
- Testes unitários e de integração
- Exemplos: `teste_*.py`, `test_*.py`

### 🔧 **scripts/**
- Scripts utilitários de desenvolvimento
- Automações temporárias
- Ferramentas de build e deploy
- Exemplos: `build_*.py`, `deploy_*.py`, `setup_*.py`

### 📝 **examples/**
- Códigos de exemplo
- Protótipos
- Demonstrações de funcionalidades
- Exemplos: `exemplo_*.py`, `demo_*.py`

### 🗂️ **temp/**
- Arquivos temporários
- Downloads temporários
- Arquivos de trabalho
- Cache temporário

### 💾 **backup/**
- Backups de desenvolvimento
- Versões antigas de arquivos
- Snapshots de trabalho
- Recuperação de dados

### 📊 **logs/**
- Logs de desenvolvimento
- Arquivos de debug
- Saídas de testes
- Relatórios de execução

## 🔒 **Regras de Uso:**

### ✅ **Permitido:**
- Todos os arquivos de teste e desenvolvimento
- Scripts temporários e experimentais
- Backups de trabalho
- Logs e arquivos de debug
- Protótipos e exemplos

### ❌ **NÃO Permitido:**
- Arquivos de produção
- Configurações principais
- Código final do projeto
- Arquivos sensíveis (tokens, senhas)

## 🚀 **Comandos Úteis:**

### Limpar pasta de desenvolvimento:
```bash
# Windows PowerShell
Remove-Item -Path "dev\*" -Recurse -Force -ErrorAction SilentlyContinue

# Linux/Mac
rm -rf dev/*
```

### Executar testes:
```bash
# Na pasta de desenvolvimento
cd dev/tests
python teste_exemplo.py
```

### Fazer backup:
```bash
# Copiar arquivo para backup
Copy-Item "arquivo.py" "dev/backup/arquivo_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').py"
```

## 📌 **Exemplos de Uso:**

### 1. **Teste de Nova Funcionalidade:**
```python
# dev/tests/teste_nova_funcionalidade.py
import sys
sys.path.append('../../')
from modern_gui import ModernGUI

# Código de teste aqui
```

### 2. **Script de Build:**
```python
# dev/scripts/build_release.py
import shutil
import os

def build_release():
    # Código de build aqui
    pass
```

### 3. **Exemplo de Uso:**
```python
# dev/examples/exemplo_bot.py
# Exemplo de como usar o bot

def exemplo_simples():
    # Código de exemplo aqui
    pass
```

## 🔄 **Integração com .gitignore:**

A pasta `dev/` já está configurada no `.gitignore` principal para ser ignorada pelo Git, mantendo apenas o código de produção no repositório.

## 🎯 **Benefícios:**

✅ **Organização:** Separa desenvolvimento de produção  
✅ **Limpeza:** Mantém o projeto principal limpo  
✅ **Flexibilidade:** Permite experimentação livre  
✅ **Segurança:** Evita commits acidentais de código temporário  
✅ **Produtividade:** Facilita o desenvolvimento e testes  

---

**👨‍💻 Desenvolvido por:** William Medrado (wmedrado)  
**📞 Discord:** wmedrado  
**📧 Email:** willfmedrado@gmail.com

*Use esta pasta livremente para todos os seus desenvolvimentos e testes!* 🚀
