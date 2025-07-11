# KeyDrop Bot Professional Edition v2.0.5 - Documentação Completa

## 📋 Visão Geral

O KeyDrop Bot Professional Edition v2.0.5 é uma versão otimizada e robusta do bot para participação automática em giveaways do KeyDrop. Esta versão inclui melhorias significativas em performance, sistema de stop eficiente, mini windows e gerenciamento de memória.

## 🆕 Novidades da Versão 2.0.5

### 🔥 Principais Recursos

1. **Sistema de Stop Robusto**
   - Encerramento eficiente de todos os processos Chrome
   - Eliminação de processos órfãos
   - Botão de emergência para stop forçado
   - Logs detalhados de encerramento

2. **Mini Window Mode**
   - Janelas pequenas (200x300) para economia de recursos
   - Ideal para execução de múltiplos bots
   - Reduz uso de CPU e memória
   - Configurável via interface

3. **Otimizações de Performance**
   - Argumentos otimizados para Chrome
   - Desabilitação de recursos desnecessários
   - Gerenciamento automático de memória
   - Limpeza automática de processos

4. **Gerenciamento de Memória**
   - Monitoramento automático de RAM
   - Limpeza preventiva de memória
   - Limitação de processos simultâneos
   - Estatísticas de uso em tempo real

5. **Interface Moderna Aprimorada**
   - Exibição da versão atual
   - Tooltips explicativos
   - Integração com sistema de memória
   - Controles mais intuitivos

## 🚀 Instalação

### Requisitos

- Windows 10/11
- Python 3.8 ou superior
- Google Chrome instalado
- Conexão com internet

### Instalação Automática

1. Execute o `launcher.py`:
   ```bash
   python launcher.py
   ```

2. O launcher verificará:
   - Versão do Python
   - Arquivos essenciais
   - Google Chrome
   - Dependências

3. Instalará automaticamente as dependências necessárias

### Instalação Manual

```bash
# Clone o repositório
git clone https://github.com/wmedrado/bot-keydrop.git
cd bot-keydrop

# Instale as dependências
pip install -r requirements.txt

# Execute o bot
python modern_gui.py
```

## 📖 Guia de Uso

### 1. Inicialização

**Opção 1: Launcher (Recomendado)**
```bash
python launcher.py
```

**Opção 2: Interface Direta**
```bash
python modern_gui.py
```

**Opção 3: Executável**
- Execute `KeyDrop_Bot_Moderno.exe` (interface moderna)
- Execute `KeyDrop_Bot_Classico.exe` (interface clássica)

### 2. Configuração

#### Configurações Básicas
- **Quantos bots**: Número de instâncias simultâneas (1-200)
- **Intervalo**: Tempo entre tentativas (5-60 segundos)
- **Auto-close**: Fechar automaticamente após X participações
- **Headless**: Executar sem interface gráfica
- **Mini Window**: Janelas pequenas (200x300)

#### Configurações Avançadas
- **Discord Webhook**: Notificações automáticas
- **Modo Login**: Login automático
- **Modo Contender**: Participação em contenders
- **Perfis**: Gerenciamento de perfis Chrome

### 3. Recursos Específicos

#### Mini Window Mode
- Ative a checkbox "Mini Window" na interface
- Ideal para múltiplos bots simultâneos
- Reduz uso de recursos do sistema
- Janelas de 200x300 pixels

#### Sistema de Stop
- Botão "Stop" padrão para encerramento normal
- Botão "Stop Forçado" para emergências
- Encerra todos os processos Chrome relacionados
- Limpa processos órfãos automaticamente

#### Gerenciamento de Memória
- Monitoramento automático de RAM
- Limpeza preventiva quando necessário
- Limite de 500MB por processo
- Estatísticas em tempo real

## 🔧 Configurações Avançadas

### Arquivo de Configuração (bot_config.json)

```json
{
    "num_bots": 5,
    "interval": 30,
    "auto_close": true,
    "max_participacoes": 100,
    "headless": false,
    "mini_window": true,
    "discord_webhook": "",
    "login_mode": false,
    "contender_mode": false,
    "perfil_base": "profiles/default"
}
```

### Otimizações de Performance

O sistema inclui automaticamente:
- `--no-sandbox`
- `--disable-dev-shm-usage`
- `--disable-gpu`
- `--disable-features=TranslateUI`
- `--disable-ipc-flooding-protection`
- `--max_old_space_size=4096`

### Configuração de Memória

```python
# Configurações do MemoryManager
MEMORY_THRESHOLD = 80  # % de RAM para trigger
CLEANUP_INTERVAL = 300  # 5 minutos
MAX_PROCESS_MEMORY = 500  # MB por processo
```

## 📊 Monitoramento

### Interface Principal
- **Status**: Estado atual de cada bot
- **Participações**: Contador de participações
- **Última Atividade**: Última ação realizada
- **Memória**: Uso atual de RAM
- **Versão**: Versão atual do software

### Logs
- Logs detalhados no console
- Histórico de participações
- Erros e avisos
- Estatísticas de performance

### Discord Notifications
Configure um webhook para receber:
- Notificações de participações
- Alertas de erros
- Estatísticas periódicas
- Status dos bots

## 🛠️ Troubleshooting

### Problemas Comuns

#### 1. Erro de "User Data Directory"
**Solução**: O sistema limpa automaticamente perfis conflitantes

#### 2. Chrome não abre
**Soluções**:
- Verificar se Chrome está instalado
- Executar como administrador
- Limpar cache do Chrome

#### 3. Memória alta
**Soluções**:
- Ativar Mini Window
- Reduzir número de bots
- Usar modo headless
- O sistema limpa automaticamente

#### 4. Bots não param
**Soluções**:
- Usar botão "Stop Forçado"
- Aguardar finalização automática
- Reiniciar aplicação

### Comandos de Diagnóstico

```bash
# Verificar processos Chrome
tasklist /FI "IMAGENAME eq chrome.exe"

# Limpar processos manualmente
taskkill /F /IM chrome.exe /T

# Verificar memória
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"
```

## 🔄 Atualizações

### Sistema de Atualização Automática
- Verificação automática de atualizações
- Download e instalação automática
- Backup automático da versão anterior
- Rollback em caso de problemas

### Atualizações Manuais
1. Baixar nova versão do GitHub
2. Fazer backup da configuração atual
3. Extrair arquivos
4. Executar `python launcher.py`

## 📁 Estrutura do Projeto

```
BOT-KEYDROP-BY-WILL/
├── modern_gui.py          # Interface moderna
├── keydrop_bot.py         # Bot principal
├── launcher.py            # Inicializador
├── requirements.txt       # Dependências
├── version.json          # Informações da versão
├── bot_config.json       # Configurações
├── src/
│   ├── memory_manager.py # Gerenciador de memória
│   └── utils.py          # Utilitários
├── profiles/             # Perfis Chrome
├── docs/                 # Documentação
├── dev/                  # Ferramentas de desenvolvimento
└── startup/              # Scripts de inicialização
```

## 🤝 Contribuição

### Reportar Bugs
1. Abra issue no GitHub
2. Descreva o problema detalhadamente
3. Inclua logs e screenshots
4. Especifique versão e sistema operacional

### Sugerir Melhorias
1. Abra issue com tag "enhancement"
2. Descreva a funcionalidade desejada
3. Explique o caso de uso
4. Forneça exemplos se possível

### Contribuir com Código
1. Fork o repositório
2. Crie branch para sua feature
3. Implemente as mudanças
4. Teste extensivamente
5. Envie pull request

## 📄 Licença

Este projeto está sob licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 👨‍💻 Autor

**William Medrado**
- GitHub: [@wmedrado](https://github.com/wmedrado)
- Email: contato@williammedrado.com

## 🙏 Agradecimentos

- Comunidade KeyDrop
- Contribuidores do projeto
- Testadores e usuários
- Equipe de desenvolvimento

## 📋 Changelog

### v2.0.5 (2025-07-09)
- ✅ Sistema de stop robusto implementado
- ✅ Mini Window Mode adicionado
- ✅ Otimizações de performance
- ✅ Gerenciamento automático de memória
- ✅ Interface moderna aprimorada
- ✅ Launcher atualizado

### v2.0.4 (2025-01-08)
- Sistema de atualização automática
- Melhorias na interface
- Correções de bugs críticos

### v2.0.3 (2025-01-07)
- Execução sequencial de bots
- Melhorias no sistema de stop
- Otimizações de performance

---

**© 2025 William Medrado - KeyDrop Bot Professional Edition**
