# 📋 Configuração do GitHub para Sistema de Atualização

## 🚀 Passos para Configurar o Repositório

### 1. Criar Repositório no GitHub

1. Acesse [GitHub](https://github.com) e faça login
2. Clique em "New repository"
3. Nome: `bot-keydrop`
4. Descrição: "Bot profissional para KeyDrop com suporte a múltiplas janelas"
5. Visibilidade: Public ou Private (recomendado Private)
6. Clique em "Create repository"

### 2. Configurar Repositório Local

```bash
# Navegar para a pasta do projeto
cd "C:\Users\William\Desktop\BOT-KEYDROP-BY-WILL"

# Inicializar Git (se não existe)
git init

# Adicionar remote
git remote add origin https://github.com/Wmedrado/bot-keydrop.git

# Configurar .gitignore
echo "__pycache__/" >> .gitignore
echo "*.pyc" >> .gitignore
echo ".env" >> .gitignore
echo "logs/*.log" >> .gitignore
echo "data/Profile-*/" >> .gitignore
echo "backup/*.json" >> .gitignore

# Primeiro commit
git add .
git commit -m "feat: Initial commit - KeyDrop Bot Professional Edition"
git push -u origin main
```

### 3. Criar Primeira Release

1. Vá para seu repositório no GitHub
2. Clique na aba "Releases"
3. Clique em "Create a new release"
4. Preencha os campos:
   - **Tag version:** `v2.0.0`
   - **Release title:** `KeyDrop Bot v2.0.0 - Professional Edition`
   - **Description:**
     ```markdown
     ## 🚀 KeyDrop Bot Professional Edition v2.0.0
     
     ### ✨ Principais Recursos
     - 🖥️ Interface moderna com CustomTkinter
     - 🚀 Suporte a até 200 janelas simultâneas
     - 🏆 Modo CONTENDER (sorteios de 1 hora)
     - 📱 Relatórios automáticos no Discord
     - 🔄 Sistema de atualização automática
     - 📊 Monitoramento de performance
     - 🧹 Limpeza automática de cache
     
     ### 🔧 Melhorias Técnicas
     - Otimização de recursos para múltiplas janelas
     - Seletor corrigido para sorteios CONTENDER
     - Sistema de backup automático
     - Reorganização completa do projeto
     
     ### 📋 Requisitos
     - Python 3.7+
     - Windows 10/11
     - Chrome instalado
     - 8GB+ RAM (recomendado 16GB para 100+ bots)
     
     ### 🚀 Instalação
     1. Baixe e extraia os arquivos
     2. Execute `install_complete.bat`
     3. Use `launcher.bat` para iniciar
     ```
5. Clique em "Publish release"

### 4. Atualizar version.json

Edite o arquivo `version.json` com suas informações:

```json
{
    "version": "2.0.0",
    "build": "20250708",
    "name": "KeyDrop Bot Professional Edition",
    "description": "Bot profissional para KeyDrop com suporte a até 200 janelas simultâneas",
    "author": "SEU_NOME",
    "github_repo": "https://github.com/Wmedrado/bot-keydrop",
    "features": [
        "Interface moderna com CustomTkinter",
        "Suporte a até 200 janelas simultâneas",
        "Modo CONTENDER (sorteios de 1 hora)",
        "Relatórios automáticos no Discord",
        "Monitoramento de performance",
        "Sistema de atualização automática",
        "Otimização de recursos",
        "Backup automático de configurações"
    ],
    "changelog": [
        "Corrigido seletor de sorteio CONTENDER",
        "Implementado sistema de atualização automática",
        "Adicionada interface moderna",
        "Melhorias no monitoramento de performance",
        "Reorganização completa do projeto"
    ]
}
```

### 5. Workflow de Releases (Opcional)

Crie `.github/workflows/release.yml`:

```yaml
name: Create Release
on:
  push:
    tags:
      - 'v*'

jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v3
      
      - name: Create Release
        uses: actions/create-release@v1
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        with:
          tag_name: ${{ github.ref }}
          release_name: KeyDrop Bot ${{ github.ref }}
          draft: false
          prerelease: false
```

### 6. Configurar Token (Opcional)

Para evitar rate limiting:

1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Scopes: `public_repo` ou `repo`
4. Copie o token
5. Adicione ao arquivo de configuração (não commite o token!)

## 🔄 Workflow de Atualizações

### Para Desenvolvedores

```bash
# Fazer mudanças
git add .
git commit -m "feat: nova funcionalidade"

# Atualizar versão
# Editar version.json com nova versão

# Criar tag
git tag v2.1.0
git push origin v2.1.0

# Criar release no GitHub
# O sistema automaticamente detectará a nova versão
```

### Para Usuários

1. Bot verifica automaticamente por atualizações
2. Clica no botão "🔄 Atualizar" na interface
3. Confirma a atualização
4. Bot reinicia automaticamente com nova versão

## 📊 Monitoramento

### Logs de Atualização
- `logs/update.log`: Registro de todas as atualizações
- `logs/error.log`: Erros durante atualizações
- `backup/`: Backups automáticos

### Métricas
- Versão atual vs. disponível
- Histórico de atualizações
- Taxa de sucesso de atualizações
- Tempo de downtime durante updates

## 🔐 Segurança

### Verificações
- ✅ Verificação de assinatura digital
- ✅ Checksum dos arquivos
- ✅ Backup antes da atualização
- ✅ Rollback automático em caso de falha

### Proteção de Dados
- Configurações preservadas
- Perfis do usuário mantidos
- Logs históricos preservados
- Tokens e senhas não são afetados

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro de conexão:**
   ```
   ❌ Não foi possível conectar ao GitHub
   ```
   **Solução:** Verificar conexão com internet

2. **Permissão negada:**
   ```
   ❌ Permissão negada para atualizar arquivos
   ```
   **Solução:** Executar como administrador

3. **Versão corrompida:**
   ```
   ❌ Arquivo version.json inválido
   ```
   **Solução:** Reinstalar usando install_complete.bat

### Contato para Suporte

- **GitHub Issues:** [Abrir issue](https://github.com/Wmedrado/bot-keydrop/issues)
- **Discord:** Seu servidor/canal
- **Email:** seu.email@exemplo.com

---

**Desenvolvido por Billy Franck**  
Sistema de atualização automática v2.0.0
