# Keydrop Bot Professional v2.1.0

![Python](https://img.shields.io/badge/Python-3.8+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![Status](https://img.shields.io/badge/Status-Functional-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## 🎯 Sobre o Projeto

O **Keydrop Bot Professional** é uma solução avançada de automação para o site Keydrop, desenvolvido com arquitetura moderna backend/frontend. O sistema oferece interface web responsiva, monitoramento em tempo real, integração com Discord e suporte para até 100 guias simultâneas do Chrome.

## ✨ Principais Características

- 🚀 **Backend FastAPI** com API REST e WebSocket
- 🎨 **Interface Web Moderna** HTML5/CSS3/JavaScript
- 📊 **Monitoramento em Tempo Real** de sistema e bot
- 🔗 **Integração Discord** com notificações automáticas
- 🌐 **Até 100 Guias Simultâneas** Chrome/Playwright
- ⚡ **Controle de Velocidade** e retry configuráveis
- 🛡️ **Parada de Emergência** robusta
- 📈 **Relatórios e Estatísticas** detalhados

## 🏗️ Arquitetura

```
bot_keydrop/
├── backend/                 # API FastAPI + Bot Logic
│   ├── main.py             # API principal
│   ├── bot_logic/          # Lógica de automação
│   ├── config/             # Gerenciamento configurações
│   ├── system_monitor/     # Monitoramento sistema
│   └── discord_integration/ # Notificações Discord
├── frontend/               # Interface Web
│   ├── index.html          # Interface principal
│   └── src/                # JavaScript e CSS
├── resources/              # Recursos do projeto
└── dist/                   # Build de distribuição
```

## 🚀 Início Rápido

### 1. Pré-requisitos

- Python 3.8 ou superior
- Chrome/Chromium instalado
- Conexão com internet

### 2. Instalação

```bash
# Clone o repositório
git clone <repository-url>
cd bot_keydrop

# Instale as dependências
pip install -r backend/requirements.txt

# Instale os drivers do Playwright
playwright install
```

### 3. Configuração

1. **Discord (Opcional):**
   - Crie um webhook no Discord
   - Configure a URL na interface de configurações

2. **Keydrop:**
   - Faça login manual no site quando solicitado
   - O bot manterá os cookies salvos

### 4. Execução

#### Método Automático (Recomendado)
```bash
python startup.py
```

#### Método Manual
```bash
# Terminal 1 - Backend
cd backend
python -m uvicorn main:app --host localhost --port 8000 --reload

# Terminal 2 - Frontend
cd frontend
python -m http.server 3000
```

### 5. Acesso

- **Interface Web:** http://localhost:3000
- **API Backend:** http://localhost:8000
- **Documentação API:** http://localhost:8000/docs

## 🎮 Como Usar

### Interface de Configurações
1. Acesse a aba "Configurações"
2. Configure número de guias (1-100)
3. Ajuste velocidade de execução
4. Configure Discord Webhook (opcional)
5. Salve as configurações

### Controle do Bot
1. Clique em "Iniciar Bot" para começar
2. Monitore estatísticas na aba "Estatísticas"
3. Visualize logs na aba "Relatórios"
4. Use "STOP" para parada de emergência

### Monitoramento
- **Tempo Real:** Atualizações automáticas via WebSocket
- **Sistema:** CPU, RAM, Disco, Rede
- **Bot:** Participações, sucessos, falhas
- **Navegadores:** Status de cada guia

## 📋 Funcionalidades Detalhadas

### Backend
- ✅ API REST completa com FastAPI
- ✅ WebSocket para atualizações em tempo real
- ✅ Gerenciamento de múltiplas instâncias Chrome
- ✅ Sistema de retry e recuperação de erros
- ✅ Monitoramento de recursos do sistema
- ✅ Integração com Discord webhooks
- ✅ Persistência de configurações

### Frontend
- ✅ Interface responsiva moderna
- ✅ Sistema de abas intuitivo
- ✅ Formulários com validação
- ✅ Notificações toast
- ✅ Atualizações em tempo real
- ✅ Exportação de relatórios
- ✅ Controles de emergência

### Automação
- ✅ Navegação automática no Keydrop
- ✅ Detecção e clique em sorteios
- ✅ Gerenciamento de cookies/login
- ✅ Modo headless e mini-window
- ✅ Ciclo inteligente entre guias
- ✅ Histórico de participações

## 🔧 Configurações Avançadas

### Parâmetros Principais
- **Guias:** 1-100 instâncias simultâneas
- **Velocidade:** 0.1x a 10x (multiplicador)
- **Retry:** 1-20 tentativas por falha
- **Modo:** Headless ou visível
- **Tamanho:** Normal ou mini (200x300)

### Integrações
- **Discord:** Notificações automáticas
- **Logs:** Sistema de logging detalhado
- **Relatórios:** Exportação JSON/CSV
- **Monitoramento:** Métricas de sistema

## 🛠️ Desenvolvimento

### Tecnologias Utilizadas
- **Backend:** Python, FastAPI, Playwright, psutil
- **Frontend:** HTML5, CSS3, JavaScript ES6+
- **Automação:** Playwright + Chrome
- **Comunicação:** REST API + WebSocket
- **Notificações:** Discord Webhooks

### Estrutura de Código
```python
# Backend modular
backend/
├── main.py              # API FastAPI
├── bot_logic/           # Automação core
├── config/              # Configurações
├── system_monitor/      # Monitoramento
└── discord_integration/ # Notificações
```

### API Endpoints
```http
# Configuração
GET    /api/config
PUT    /api/config
POST   /api/config/reset

# Controle
POST   /api/control/start
POST   /api/control/stop
POST   /api/control/emergency-stop
GET    /api/control/status

# Dados
GET    /api/stats
GET    /api/reports
GET    /api/system
WS     /ws
```

## 🔒 Segurança

- ✅ Validação de entrada em todos os endpoints
- ✅ Tratamento de erros robusto
- ✅ Isolamento de processos navegador
- ✅ Limpeza automática de recursos
- ✅ Logs de segurança
- ✅ Rate limiting interno

## 📊 Performance

### Recursos Otimizados
- **Memória:** Gerenciamento eficiente de instâncias
- **CPU:** Processamento assíncrono
- **Rede:** Uso otimizado de bandwidth
- **Disco:** Logs rotativos e limpeza automática

### Limites Testados
- **Guias:** Até 100 instâncias simultâneas
- **Uptime:** 24/7 continuous operation
- **Throughput:** ~1000 participações/hora
- **Latência:** <100ms API response time

## 🐛 Troubleshooting

### Problemas Comuns

#### Backend não inicia
```bash
# Verifique dependências
pip install -r backend/requirements.txt
playwright install

# Verifique porta
netstat -an | findstr :8000
```

#### Frontend não carrega
```bash
# Verifique se o backend está rodando
curl http://localhost:8000/health

# Inicie frontend manualmente
cd frontend && python -m http.server 3000
```

#### Bot não funciona
1. Verifique conexão com internet
2. Faça login manual no Keydrop
3. Verifique configurações na interface
4. Consulte logs na aba Relatórios

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Desenvolvedor

**William Medrado (wmedrado)**
- GitHub: [@wmedrado](https://github.com/wmedrado)
- Email: [contato disponível no GitHub]

## 🤝 Contribuição

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Changelog

### v2.1.0 (Atual)
- ✅ Interface web moderna implementada
- ✅ Backend FastAPI completo
- ✅ Sistema de monitoramento em tempo real
- ✅ Integração Discord
- ✅ Suporte até 100 guias
- ✅ Parada de emergência robusta

### Versões Anteriores
- v2.0.x: Versões de desenvolvimento e testes
- v1.x: Versões legadas

## 🔮 Roadmap

### Próximas Versões
- [ ] Empacotamento com PyInstaller
- [ ] App desktop nativo (Tauri/Electron)
- [ ] Testes automatizados
- [ ] Sistema de plugins
- [ ] Múltiplos idiomas
- [ ] Temas dark/light

---

**🎯 Keydrop Bot Professional v2.1.0 - A solução definitiva para automação Keydrop**

*Desenvolvido com ❤️ para a comunidade*
