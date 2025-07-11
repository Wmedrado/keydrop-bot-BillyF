# 🚀 Guia de Instalação - KeyDrop Bot Professional

## 📋 Requisitos do Sistema

### Requisitos Mínimos
- **Sistema Operacional**: Windows 10 ou superior
- **Python**: Versão 3.8 ou superior
- **Chrome**: Versão 100 ou superior
- **RAM**: 4GB mínimo (8GB recomendado)
- **Processador**: Intel i3 ou equivalente

### Requisitos Recomendados
- **RAM**: 16GB ou mais
- **Processador**: Intel i5 ou superior
- **SSD**: Para melhor performance
- **Conexão**: Internet banda larga estável

## 🔧 Instalação Automática (Recomendado)

### 1. Download do Projeto
```bash
git clone https://github.com/seu-usuario/keydrop-bot.git
cd keydrop-bot
```

### 2. Executar Instalação Automática
```bash
# Execute o script de instalação
.\scripts\install.bat
```

O script irá:
- ✅ Verificar Python
- ✅ Atualizar pip
- ✅ Instalar dependências
- ✅ Criar estrutura de pastas
- ✅ Configurar ambiente

## 🛠️ Instalação Manual

### 1. Instalar Python
1. Baixe Python de [python.org](https://python.org/downloads/)
2. Execute o instalador
3. ✅ Marque "Add Python to PATH"
4. Verifique: `python --version`

### 2. Instalar Dependências
```bash
# Atualizar pip
python -m pip install --upgrade pip

# Instalar dependências
pip install -r requirements.txt
```

### 3. Configurar Chrome
```bash
# Instalar ChromeDriver
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### 4. Estrutura de Pastas
```
keydrop-bot/
├── src/              # Código fonte
├── docs/             # Documentação
├── tests/            # Testes
├── scripts/          # Scripts utilitários
├── backup/           # Backups automáticos
├── logs/             # Logs do sistema
├── profiles/         # Perfis do Chrome
└── data/             # Dados do bot
```

## 📦 Dependências

### Principais
- `customtkinter==5.2.2` - Interface moderna
- `selenium==4.15.2` - Automação web
- `webdriver-manager==4.0.1` - Gerenciador ChromeDriver
- `requests==2.31.0` - Requisições HTTP
- `psutil==5.9.6` - Monitoramento sistema

### Opcionais
- `discord-webhook==1.3.0` - Notificações Discord
- `pywin32>=307` - Funcionalidades Windows
- `pillow==10.1.0` - Processamento imagens

## 🎯 Primeira Execução

### 1. Interface Moderna (Recomendado)
```bash
python main_modern.py
```

### 2. Interface Clássica
```bash
python main.py
```

### 3. Modo Linha de Comando
```bash
python keydrop_bot.py --headless --bots 5
```

## ⚙️ Configuração Inicial

### 1. Configurações Básicas
- **Janelas**: 5 (recomendado para teste)
- **Velocidade**: 5 (moderada)
- **Modo**: Headless desabilitado (para teste)

### 2. Modos de Operação
- **🎯 AMATEUR**: Sorteios de 3 minutos
- **🏆 CONTENDER**: Sorteios de 1 hora
- **👁️ Headless**: Navegador oculto
- **🔐 Login**: Automático

### 3. Integração Discord (Opcional)
1. Criar webhook no servidor Discord
2. Copiar URL do webhook
3. Colar no campo "Discord Webhook"
4. Ativar "Relatórios (12h)"

## 🔍 Solução de Problemas

### Erro: "customtkinter not found"
```bash
pip install customtkinter==5.2.2
```

### Erro: "ChromeDriver not found"
```bash
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### Erro: "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### Chrome não abre
1. Verificar se Chrome está instalado
2. Executar como administrador
3. Desativar antivírus temporariamente

### Performance baixa
1. Reduzir número de janelas
2. Ativar modo Headless
3. Fechar programas desnecessários
4. Verificar uso de CPU/RAM

## 📊 Monitoramento

### Logs do Sistema
- Localização: `logs/bot.log`
- Rotação: Automática (10MB)
- Níveis: INFO, WARNING, ERROR, DEBUG

### Performance
- **CPU**: < 50% (ideal)
- **RAM**: < 80% (ideal)
- **Disco**: < 90% (ideal)

### Estatísticas
- Sorteios AMATEUR
- Sorteios CONTENDER
- Taxa de sucesso
- Ganhos acumulados

## 🆘 Suporte

### Arquivos de Log
```
logs/
├── bot.log           # Log principal
├── error.log         # Erros críticos
└── performance.log   # Métricas sistema
```

### Comando de Diagnóstico
```bash
python -m src.utils --diagnose
```

### Restaurar Configurações
```bash
# Deletar arquivo de configuração
del bot_config.json

# Restaurar backup
copy backup\bot_config.json.backup bot_config.json
```

## 🔄 Atualizações

### Automática
- O bot verifica atualizações automaticamente
- Notifica quando nova versão disponível

### Manual
```bash
git pull origin main
pip install -r requirements.txt --upgrade
```

## 🛡️ Segurança

### Proteção de Dados
- Configurações criptografadas
- Tokens em variáveis ambiente
- Backups automáticos

### Melhores Práticas
1. Não compartilhar webhooks Discord
2. Usar senhas fortes
3. Manter sistema atualizado
4. Monitorar logs regularmente

## 📞 Contato

- **Desenvolvedor**: William
- **Email**: [seu-email]
- **Discord**: [seu-discord]
- **GitHub**: [seu-github]

---

**Última atualização**: 2024
**Versão**: 2.0.0
