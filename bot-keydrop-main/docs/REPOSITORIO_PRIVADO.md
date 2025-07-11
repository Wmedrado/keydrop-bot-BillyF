# 🔒 Guia para Atualizações com Repositório Privado

## 👨‍💻 Desenvolvido por Billy Franck (wmedrado)

Este guia explica como configurar o sistema de atualizações automáticas com repositório privado no GitHub.

## 🎯 Problema e Solução

### ❌ **Problema:**
- Repositório privado no GitHub
- Bot não consegue acessar releases sem autenticação
- Necessidade de manter código protegido

### ✅ **Solução:**
- **GitHub Personal Access Token (PAT)**
- **GitHub Releases públicas** (mesmo com repo privado)
- **Sistema de autenticação seguro**

## 🔧 Configuração Passo a Passo

### 1. **Criar Token de Acesso Pessoal**

1. Acesse: https://github.com/settings/tokens
2. Clique em "Generate new token" → "Generate new token (classic)"
3. Configure as permissões:
   - ✅ **repo** (Full control of private repositories)
   - ✅ **repo:status** (Access commit status)
   - ✅ **public_repo** (Access public repositories)
4. Clique em "Generate token"
5. **⚠️ IMPORTANTE**: Copie o token imediatamente (não será mostrado novamente)

### 2. **Configurar Token no Bot**

#### Opção A: Variável de Ambiente (Recomendada)
```bash
# Windows
set GITHUB_TOKEN=ghp_seu_token_aqui

# Ou adicionar nas variáveis de sistema
```

#### Opção B: Arquivo de Configuração
```json
// bot_config.json
{
  "github_token": "ghp_seu_token_aqui",
  "num_bots": 2,
  // ... outras configurações
}
```

#### Opção C: Arquivo Separado
```bash
# Criar arquivo: github_token.txt
ghp_seu_token_aqui
```

### 3. **Configurar Releases no GitHub**

#### Criar Release:
```bash
# Via GitHub Web
1. Acesse: https://github.com/Wmedrado/bot-keydrop/releases
2. Clique em "Create a new release"
3. Tag: v2.0.1
4. Title: KeyDrop Bot v2.0.1
5. Description: Changelog das modificações
6. Anexar arquivo ZIP com o código atualizado
7. Publicar
```

#### Via GitHub CLI:
```bash
# Instalar GitHub CLI
# Criar release
gh release create v2.0.1 --title "KeyDrop Bot v2.0.1" --notes "Changelog aqui"

# Anexar arquivo
gh release upload v2.0.1 keydrop-bot-v2.0.1.zip
```

### 4. **Implementar no Bot**

#### Modificar modern_gui.py:
```python
# Substituir UpdateManager por PrivateUpdateManager
from src.private_update_manager import PrivateUpdateManager

class ModernKeyDropGUI:
    def __init__(self):
        # ... código existente ...
        self.update_manager = PrivateUpdateManager()
    
    def verificar_atualizacao(self):
        self.update_manager.update_with_gui(self.root)
```

## 🛠️ Estrutura de Releases

### **Formato Recomendado:**
```
releases/
├── v2.0.1/
│   ├── keydrop-bot-v2.0.1.zip
│   ├── CHANGELOG.md
│   └── README.md
```

### **Conteúdo do ZIP:**
```
keydrop-bot-v2.0.1.zip
├── modern_gui.py
├── keydrop_bot.py
├── main_modern.py
├── requirements.txt
├── src/
│   ├── utils.py
│   ├── update_manager.py
│   └── private_update_manager.py
├── docs/
└── scripts/
```

## 🔐 Segurança

### **Boas Práticas:**
1. **Token Seguro**: Nunca commitar o token no código
2. **Permissões Mínimas**: Apenas acesso necessário
3. **Rotação**: Renovar token periodicamente
4. **Backup**: Manter backup do token

### **Arquivos a Não Commitar:**
```bash
# .gitignore
github_token.txt
bot_config.json
profiles/
logs/
*.log
__pycache__/
```

## 📊 Vantagens da Solução

### ✅ **Repositório Privado:**
- Código protegido
- Controle de acesso
- Histórico privado

### ✅ **Releases Públicas:**
- Atualizações automáticas
- Changelog visível
- Versionamento claro

### ✅ **Autenticação:**
- Segura via token
- Controle de permissões
- Fácil revogação

## 🔄 Fluxo de Atualização

### **Processo Automático:**
1. Bot verifica releases usando token
2. Compara versão atual com última release
3. Baixa arquivo ZIP se nova versão
4. Faz backup dos arquivos importantes
5. Aplica atualização mantendo configurações
6. Notifica usuário para reiniciar

### **Arquivos Preservados:**
- `bot_config.json` (configurações)
- `profiles/` (dados de login)
- `logs/` (histórico)
- `github_token.txt` (token)

## 🚀 Implementação Completa

### **Script de Deploy:**
```bash
# deploy.bat
@echo off
echo Criando release...

# Versão
set VERSION=2.0.1

# Criar ZIP
powershell Compress-Archive -Path "*.py","src","docs","scripts" -DestinationPath "keydrop-bot-v%VERSION%.zip"

# Criar release
gh release create v%VERSION% --title "KeyDrop Bot v%VERSION%" --notes-file CHANGELOG.md

# Upload arquivo
gh release upload v%VERSION% keydrop-bot-v%VERSION%.zip

echo Release criada com sucesso!
```

### **Testar Atualização:**
```python
# teste_update.py
from src.private_update_manager import PrivateUpdateManager

updater = PrivateUpdateManager()
update_info = updater.check_for_updates()

if update_info.get("available"):
    print(f"✅ Atualização disponível: v{update_info['version']}")
    updater.download_update(update_info)
else:
    print("ℹ️ Nenhuma atualização disponível")
```

## 📞 Suporte

### **Problemas Comuns:**
- **Token inválido**: Verificar permissões e validade
- **Repo não encontrado**: Verificar nome e acesso
- **Erro de download**: Verificar conexão e token

### **Contato:**
- **Discord**: wmedrado
- **GitHub**: Abrir issue no repositório

---

## 🎉 Conclusão

Com esta configuração, você pode:
- ✅ Manter repositório privado
- ✅ Distribuir atualizações automaticamente
- ✅ Proteger código fonte
- ✅ Controlar acesso

**Seu bot está pronto para atualizações automáticas seguras!**

---

*Desenvolvido com ❤️ por Billy Franck (wmedrado)*
