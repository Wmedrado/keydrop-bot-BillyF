# Sistema de Atualização Automática

## 📋 Visão Geral

O KeyDrop Bot Professional Edition inclui um sistema completo de atualização automática que permite manter o bot sempre na versão mais recente sem intervenção manual.

## 🔧 Como Funciona

### 1. Verificação de Atualizações
- O sistema verifica automaticamente por novas versões no GitHub
- Compara a versão atual com a mais recente disponível
- Mostra informações sobre as melhorias incluídas

### 2. Download Automático
- Baixa automaticamente a versão mais recente
- Verifica a integridade dos arquivos
- Mantém um backup da versão anterior

### 3. Aplicação da Atualização
- Cria backup completo da configuração atual
- Substitui arquivos antigos pelos novos
- Preserva configurações e dados do usuário
- Restaura configurações personalizadas

## 🎮 Como Usar

### Interface Moderna (CustomTkinter)
1. Abra a interface moderna: `launcher.bat` → Opção 1
2. Clique no botão "🔄 Atualizar" na seção de controles
3. Aguarde a verificação automática
4. Se houver atualização, confirme para aplicar

### Interface Clássica (Tkinter)
1. Abra a interface clássica: `launcher.bat` → Opção 2
2. Vá no menu "Ferramentas" → "Verificar Atualizações"
3. Confirme se deseja aplicar a atualização

### Linha de Comando
```batch
python -m src.update_manager
```

## 📁 Estrutura de Arquivos

```
bot-keydrop/
├── src/
│   └── update_manager.py      # Gerenciador de atualizações
├── version.json               # Informações da versão atual
├── backup/                    # Backups automáticos
│   ├── config_backup_*.json
│   └── version_backup_*.json
└── logs/
    └── update.log            # Logs de atualização
```

## ⚙️ Configuração do GitHub

### Para Desenvolvedores

1. **Criar Repository**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/Wmedrado/bot-keydrop
   git push -u origin main
   ```

2. **Configurar Releases**
   - Vá para o GitHub → seu repositório → Releases
   - Clique em "Create a new release"
   - Tag: v2.0.0 (seguir versionamento semântico)
   - Título: "KeyDrop Bot v2.0.0"
   - Descrição: changelog das melhorias
   - Anexar arquivo ZIP com o projeto

3. **Atualizar version.json**
   ```json
   {
       "version": "2.0.0",
       "github_repo": "https://github.com/Wmedrado/bot-keydrop"
   }
   ```

### Para Usuários

1. **Primeira Configuração**
   - O sistema já vem configurado para verificar atualizações
   - Não é necessária configuração adicional

2. **Verificação Manual**
   - Use o botão "🔄 Atualizar" na interface
   - Ou execute: `python -m src.update_manager`

## 🔐 Segurança

### Verificações Automáticas
- ✅ Verificação de integridade dos arquivos
- ✅ Backup automático antes da atualização
- ✅ Rollback em caso de falha
- ✅ Preservação de configurações do usuário

### Proteção de Dados
- Configurações do usuário são preservadas
- Perfis do Chrome mantidos
- Logs históricos preservados
- Backups automáticos por 30 dias
- Sistema de retry automático em caso de falha de conexão
- Fallback para requisições anônimas se o token estiver inválido (repositórios públicos)
- Repositórios privados exigem token válido
- Registro detalhado em `logs/update.log`

## 🚨 Resolução de Problemas

### Erro de Conexão
```
❌ Erro: Não foi possível conectar ao GitHub
```
**Solução:** Verifique sua conexão com a internet

### Erro de Permissão
```
❌ Erro: Permissão negada para atualizar arquivos
```
**Solução:** Execute como administrador

### Falha na Atualização
```
❌ Erro: Falha ao aplicar atualização
```
**Solução:** O sistema restaura automaticamente o backup

### Versão Corrompida
```
❌ Erro: Arquivo version.json corrompido
```
**Solução:** Reinstale usando `install_complete.bat`

## 📊 Logs de Atualização

### Localização
- Arquivo: `logs/update.log`
- Rotação: 7 dias
- Formato: JSON estruturado

### Exemplo de Log
```json
{
    "timestamp": "2025-01-08T14:30:00",
    "action": "update_check",
    "current_version": "2.0.0",
    "latest_version": "2.1.0",
    "status": "success",
    "details": "Nova versão disponível"
}
```

## 🔄 Versionamento

### Formato: MAJOR.MINOR.PATCH
- **MAJOR:** Mudanças incompatíveis
- **MINOR:** Novas funcionalidades
- **PATCH:** Correções de bugs

### Exemplo
- v1.0.0 → v1.1.0: Nova funcionalidade
- v1.1.0 → v1.1.1: Correção de bug
- v1.1.1 → v2.0.0: Mudança major

## 🎯 Roadmap de Atualizações

### Versão 2.1.0 (Planejada)
- [ ] Modo distribuído multi-máquina
- [ ] Dashboard web para monitoramento
- [ ] Integração com Telegram
- [ ] Análise de lucro automática

### Versão 2.2.0 (Planejada)
- [ ] Machine Learning para otimização
- [ ] Suporte a múltiplas plataformas
- [ ] API REST para integração
- [ ] Mobile app companion

## 💡 Dicas Avançadas

### Atualizações Automáticas
```python
# Configurar verificação automática a cada 6 horas
from src.update_manager import UpdateManager
update_manager = UpdateManager()
update_manager.enable_auto_check(interval_hours=6)
```

### Configuração Personalizada
```json
{
    "auto_update": true,
    "check_interval": 21600,
    "backup_retention": 30,
    "github_token": "opcional_para_rate_limit"
}
```

### Integração com CI/CD
```yaml
# .github/workflows/release.yml
name: Release
on:
  push:
    tags: ['v*']
jobs:
  release:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Create Release
        uses: actions/create-release@v1
```

---

**Desenvolvido por Billy Franck**  
Para suporte: abra uma issue no GitHub ou contate via Discord
