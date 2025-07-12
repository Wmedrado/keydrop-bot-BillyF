# 🚀 Guia de Instalação e Configuração
## Keydrop Bot Professional v2.1.0

**Desenvolvido por:** William Medrado (wmedrado)  
**Versão:** 2.1.0  
**Data:** Janeiro 2025

---

## 📋 Pré-requisitos

### 🔧 Software Necessário
1. **Python 3.8+** - [Download](https://python.org)
2. **Google Chrome** - [Download](https://chrome.google.com)
3. **Git** (opcional) - [Download](https://git-scm.com)

### 💻 Sistema Operacional
- ✅ Windows 10/11
- ✅ macOS 10.15+
- ✅ Linux Ubuntu 18.04+

---

## 🛠️ Instalação

### Método 1: Executável (Recomendado)
1. Baixe `KeydropBot_Professional.exe`
2. Execute o arquivo
3. Aguarde a inicialização
4. Acesse http://localhost:8000

### Método 2: Código Fonte

#### 1. Clone ou baixe o projeto
```bash
git clone https://github.com/wmedrado/keydrop-bot-professional.git
cd keydrop-bot-professional
```

#### 2. Instale dependências Python
```bash
# Backend
cd backend
pip install -r requirements.txt

# O arquivo inclui `undetected-chromedriver`, utilizado para diminuir a
# detecção automática do Chrome.

# Frontend (opcional, para desenvolvimento)
cd ../frontend
npm install
```

#### 3. Instale Playwright browsers
```bash
playwright install chromium
```

#### 4. Execute o bot
```bash
# Opção 1: Script automático
python startup.py

# Opção 2: Batch file (Windows)
run_bot.bat

# Opção 3: Backend apenas
cd backend
python main.py
```

---

## ⚙️ Configuração Inicial

### 1. Primeiro Acesso
1. Abra http://localhost:8000
2. Vá para a aba "Configurações"
3. Configure os parâmetros básicos

### 2. Configurações Recomendadas

#### 🎯 Configurações Básicas
- **Quantidade de Guias:** 5-10 (iniciante), 50+ (avançado)
- **Velocidade:** 2-5 segundos (evita detecção)
- **Tentativas de Retry:** 3-5
- **Modo Headless:** ✅ (economiza recursos)
- **Modo Mini:** ✅ (economiza tela)

#### 🔐 Login (Opcional)
- **Login Keydrop:** ✅ (recomendado)
- **Login Steam:** ✅ (se necessário)

#### 📢 Discord (Opcional)
- **Webhook URL:** Seu webhook Discord
- **Notificações:** ✅ (recomendado)

### 3. Perfis de Usuário
O bot automaticamente cria perfis únicos para cada guia:
- `profiles/profile_1/` - Primeira guia
- `profiles/profile_2/` - Segunda guia
- etc.

---

## 🎮 Como Usar

### 1. Iniciar o Bot
1. Configure os parâmetros
2. Clique "Salvar Configuração"
3. Clique "Iniciar Bot"
4. Monitore nas abas "Estatísticas" e "Relatórios"

### 2. Monitoramento
- **Estatísticas:** Dados em tempo real
- **Relatórios:** Histórico e logs
- **System:** Uso de recursos do sistema

### 3. Controles
- **Pausar/Retomar:** Pausa temporária
- **Stop de Emergência:** Para imediatamente
- **Limpar Cache:** Remove cache mantendo logins
- **Verificar Atualizações:** Busca novas versões

---

## 📊 Interface

### 🎛️ Aba Configurações
- Quantidade de guias Chrome (1-100)
- Velocidade de execução (1-10 segundos)
- Tentativas de retry (1-10)
- Modo headless e mini
- Webhook Discord
- Login opcional

### 📈 Aba Estatísticas
- Uso de RAM, CPU, HD
- Consumo de internet
- Status das guias em tempo real
- Estatísticas de participação
- Taxa de sucesso

### 📋 Aba Relatórios
- Logs de execução
- Histórico de participações
- Exportação JSON/CSV
- Limpeza de dados

### ⚙️ Aba System
- Informações do sistema
- Status do monitoramento
- Configurações técnicas

---

## 🔧 Solução de Problemas

### ❌ Problemas Comuns

#### Bot não inicia
```bash
# Verifique Python
python --version

# Verifique dependências
pip install -r backend/requirements.txt

# Verifique Chrome
where chrome
```

#### Erro "Chrome não encontrado"
1. Instale Google Chrome
2. Verifique o PATH do sistema
3. Reinicie o bot

#### Erro "Porta 8000 ocupada"
1. Feche outras aplicações na porta 8000
2. Ou edite `BACKEND_PORT` nos scripts

#### Erro de memória
1. Reduza a quantidade de guias
2. Ative modo headless
3. Feche outras aplicações

### 🐛 Debug

#### Logs detalhados
```bash
# Execute com debug
python backend/main.py --log-level debug
```

#### Verificar status
- Acesse http://localhost:8000/health
- Verifique logs na aba "Relatórios"

---

## 🛡️ Segurança e Boas Práticas

### ✅ Recomendações
1. **Não use credenciais reais** em testes
2. **Configure velocidade adequada** (evita detecção)
3. **Use VPN** para maior privacidade
4. **Monitore recursos** do sistema
5. **Faça backups** das configurações

### ⚠️ Avisos
- Bot para fins educacionais
- Respeite termos de serviço dos sites
- Use responsavelmente
- Não abuse da automação

---

## 📚 Recursos Avançados

### 🔄 Agendamento Automático
- Sorteios são verificados automaticamente
- Tempo específico para tipo "AMATEUR": 3 minutos
- Ciclo inteligente entre guias

### 🕵️ Modo Stealth
- Headers personalizados
- User-Agent rotativo
- Mascaramento de propriedades webdriver
- Simulação de comportamento humano

### 💾 Persistência de Sessão
- Cookies salvos por perfil
- LocalStorage persistente
- Sessões mantidas entre reinicializações

### 📱 Notificações Discord
- Início/fim de sessão
- Participações em sorteios
- Erros e alertas
- Relatórios estatísticos

---

## 🔗 Links Úteis

- **Interface:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **GitHub:** https://github.com/wmedrado
- **Suporte:** Issues no GitHub

---

## 📝 Changelog

### v2.1.0 (2025-01-09)
- ✅ Interface moderna e responsiva
- ✅ Perfis únicos por guia
- ✅ Persistência de sessão
- ✅ Modo stealth anti-detecção
- ✅ Integração Discord completa
- ✅ Monitoramento em tempo real
- ✅ Sistema de relatórios
- ✅ Stop de emergência
- ✅ Gerenciamento até 100 guias

---

## 👨‍💻 Desenvolvedor

**William Medrado (wmedrado)**
- GitHub: https://github.com/wmedrado
- Bot: Keydrop Bot Professional
- Versão: 2.1.0

---

*Última atualização: Janeiro 2025*
