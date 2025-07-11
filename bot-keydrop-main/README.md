# 🔑 KeyDrop Bot - Professional Edition

![Version](https://img.shields.io/badge/version-2.0.5-blue.svg)
![Python](https://img.shields.io/badge/python-3.7+-green.svg)
![License](https://img.shields.io/badge/license-MIT-yellow.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

Bot profissional para KeyDrop com suporte a até **200 janelas simultâneas**, interface moderna e sistema de atualização automática.

## 🚀 Principais Recursos

### 🔥 Novidades v2.0.5

- **🛑 Sistema de Stop Robusto**: Encerramento total de processos Chrome com eliminação de órfãos
- **🔽 Mini Window Mode**: Janelas pequenas (200x300) para economia de recursos e espaço
- **⚡ Otimizações de Performance**: Argumentos Chrome otimizados, economia de 30-40% de RAM
- **🧠 Gerenciamento de Memória**: Monitoramento automático e limpeza preventiva em tempo real
- **🏷️ Interface Aprimorada**: Exibição da versão, tooltips explicativos e controles melhorados
- **🚀 Launcher Atualizado**: Verificação automática de dependências e ambiente otimizado

### 🖥️ Interface Dupla
- **Interface Moderna**: CustomTkinter com design profissional
- **Interface Clássica**: Tkinter tradicional para compatibilidade
- **Painel de Performance**: Monitoramento em tempo real

### 🏆 Modos de Operação
- **AMATEUR**: Sorteios de 3 minutos (padrão)
- **CONTENDER**: Sorteios especiais de 1 hora
- **Modo Híbrido**: Executa ambos simultaneamente

### 📱 Integração Discord
- Relatórios automáticos a cada 12 horas
- Notificações de participação em sorteios
- Estatísticas detalhadas

### 🔄 Sistema de Atualização
- Verificação automática de atualizações
- Download e instalação automática
- Backup automático antes da atualização
- Rollback em caso de falha

### 🧹 Otimização de Performance
- Limpeza automática de cache
- Gerenciamento inteligente de recursos
- Suporte a até 200 janelas simultâneas
- Monitoramento de CPU e memória

## 📋 Requisitos

### Mínimos
- Windows 10/11
- Python 3.7+
- Chrome instalado
- 8GB RAM
- 4 núcleos de CPU

### Recomendados (100+ bots)
- 16GB+ RAM
- 8+ núcleos de CPU
- SSD para melhor performance
- Conexão de alta velocidade

## 🚀 Instalação Rápida

### 1. Download e Extração
```bash
# Baixe o projeto e extraia para:
C:\Users\SEU_USUARIO\Desktop\BOT-KEYDROP-BY-WILL
```

### 2. Instalação Automática
```batch
# Execute como administrador:
install_complete.bat
```

### 3. Inicialização
```batch
# Use o launcher principal:
launcher.bat
```

## 🎮 Como Usar

### Iniciando o Bot

1. **Launcher Principal**
   ```batch
   launcher.bat
   ```
   - Opção 1: Interface Moderna
   - Opção 2: Interface Clássica
   - Opção 3: Instalar/Atualizar

2. **Configuração Básica**
   - Número de bots: 1-200
   - Modo: AMATEUR/CONTENDER
   - Discord webhook (opcional)

3. **Execução**
   - Clique em "▶️ Iniciar Bots"
   - Aguarde o carregamento automático
   - Monitore via painel de performance

### Configurações Avançadas

```json
{
    "num_bots": 50,
    "modo": "CONTENDER",
    "headless": true,
    "login_automatico": true,
    "discord_webhook": "https://discord.com/api/webhooks/...",
    "relatorio_intervalo": 12
}
```

## 📊 Monitoramento

### Painel de Performance
- **CPU**: Uso em tempo real
- **Memória**: Consumo por bot
- **Bots Ativos**: Status individual
- **Participações**: Contadores por tipo

### Logs Automáticos
- `logs/bot.log`: Atividade geral
- `logs/performance.log`: Métricas de sistema
- `logs/discord.log`: Relatórios enviados
- `logs/update.log`: Atualizações aplicadas

## 🔧 Estrutura do Projeto

```
BOT-KEYDROP-BY-WILL/
├── src/                    # Código principal
│   ├── utils.py           # Utilitários
│   ├── icons_config.py    # Configuração visual
│   └── update_manager.py  # Sistema de atualização
├── scripts/               # Scripts de utilitários
│   ├── iniciar_interface_moderna.bat
│   ├── iniciar_interface_classica.bat
│   └── configurar_chrome.bat
├── docs/                  # Documentação
│   ├── INSTALACAO.md
│   ├── SISTEMA_ATUALIZACAO.md
│   └── CONFIGURACAO_GITHUB.md
├── tests/                 # Testes automatizados
├── backup/               # Backups automáticos
├── logs/                 # Logs do sistema
├── data/                 # Dados e perfis
└── profiles/            # Perfis do Chrome
```

## 🔄 Sistema de Atualização

### Como Funciona
1. **Verificação**: Compara versão local com GitHub
2. **Download**: Baixa nova versão automaticamente
3. **Backup**: Cria backup da configuração atual
4. **Instalação**: Substitui arquivos preservando dados
5. **Verificação**: Confirma integridade da atualização

### Usar Atualização
- **Interface Moderna**: Botão "🔄 Atualizar"
- **Interface Clássica**: Menu "Ferramentas"
- **Linha de Comando**: `python -m src.update_manager`

## 🏆 Modo CONTENDER

### Características
- Sorteios especiais de 1 hora
- Maior valor dos prêmios
- Executa junto com sorteios normais
- Prioridade inteligente

### Configuração
```python
# Ativação automática
modo_contender = True
intervalo_verificacao = 3600  # 1 hora
```

## 📱 Integração Discord

### Configuração
1. Criar webhook no Discord
2. Copiar URL do webhook
3. Configurar no bot
4. Relatórios automáticos a cada 12h

### Exemplo de Relatório
```
🔑 KeyDrop Bot - Relatório Automático

📊 Estatísticas (últimas 12h):
• Bots ativos: 50/50
• Participações AMATEUR: 1,247
• Participações CONTENDER: 12
• Taxa de sucesso: 94.2%

🖥️ Performance:
• CPU média: 45%
• Memória: 8.2GB/16GB
• Uptime: 11h 42min
```

## 🔐 Segurança

### Proteções Implementadas
- ✅ Detecção anti-bot contornada
- ✅ Headers otimizados
- ✅ User-Agent randomizado
- ✅ Delays inteligentes
- ✅ Rotação de profiles

### Backup Automático
- Configurações salvas automaticamente
- Backups antes de atualizações
- Rollback em caso de falha
- Retenção de 30 dias

## 🚨 Troubleshooting

### Problemas Comuns

1. **Bot não inicia**
   ```
   ❌ Erro: Chrome não encontrado
   ```
   **Solução**: Execute `scripts/configurar_chrome.bat`

2. **Erro de dependências**
   ```
   ❌ Erro: Módulo não encontrado
   ```
   **Solução**: Execute `install_complete.bat`

3. **Performance baixa**
   ```
   ❌ Aviso: CPU > 90%
   ```
   **Solução**: Reduza número de bots ou use modo headless

### Logs de Diagnóstico
```batch
# Verificar logs
type logs\bot.log
type logs\error.log
```

## 📈 Performance

### Benchmarks
- **10 bots**: 2GB RAM, 20% CPU
- **50 bots**: 6GB RAM, 45% CPU
- **100 bots**: 12GB RAM, 70% CPU
- **200 bots**: 20GB RAM, 95% CPU

### Otimizações
- Modo headless para muitos bots
- Limpeza automática de cache
- Gerenciamento inteligente de recursos
- Pools de conexão otimizados

## 🔄 Roadmap

### v2.1.0 (Próxima)
- [ ] Modo distribuído multi-máquina
- [ ] Dashboard web
- [ ] Integração Telegram
- [ ] Análise de lucro

### v2.2.0 (Futuro)
- [ ] Machine Learning
- [ ] Múltiplas plataformas
- [ ] API REST
- [ ] Mobile app

## 🤝 Contribuição

### Como Contribuir
1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'feat: nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

### Diretrizes
- Seguir padrões de código
- Incluir testes
- Documentar mudanças
- Manter compatibilidade

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Desenvolvedor

**William Medrado**
- GitHub: [@wmedrado](https://github.com/wmedrado)
- Discord: wmedrado
- Email: willfmedrado@gmail.com

## 🙏 Agradecimentos

- Comunidade Python
- Desenvolvedores do Selenium
- Comunidade KeyDrop
- Testadores e usuários

---

**⚠️ Aviso Legal:** Este bot é apenas para fins educacionais. Use com responsabilidade e respeite os termos de serviço do KeyDrop.

**📝 Última Atualização:** Janeiro 2025
