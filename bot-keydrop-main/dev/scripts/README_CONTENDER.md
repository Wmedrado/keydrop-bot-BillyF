# 🎯 Modo CONTENDER - Documentação Completa

## 📋 Descrição
O modo CONTENDER é uma funcionalidade automatizada do KeyDrop Bot que participa automaticamente de giveaways disponíveis no site key-drop.com. Ele é projetado para rodar a cada 1 hora, conforme a estratégia definida para maximizar as chances de ganhar prêmios.

## 🎯 Funcionalidades

### ✅ Principais Recursos
- **Participação Automática**: Encontra e participa de todos os giveaways disponíveis
- **Execução Programada**: Roda automaticamente a cada 1 hora
- **Seletores Robustos**: Múltiplos métodos para encontrar botões de participação
- **Verificação de Login**: Confirma se o usuário está logado antes de executar
- **Logs Detalhados**: Registra todas as ações e resultados
- **Estatísticas**: Acompanha sucessos, falhas e participações
- **Interface Amigável**: Menu interativo para facilitar o uso

### 🔧 Recursos Técnicos
- **Chrome Seguro**: Configurações otimizadas para evitar detecção
- **Perfil Temporário**: Usa perfil temporário para evitar conflitos
- **Tratamento de Erros**: Robusto sistema de tratamento de exceções
- **Múltiplos Seletores**: Diferentes métodos para encontrar elementos da página

## 📁 Estrutura de Arquivos

```
dev/scripts/
├── contender_corrigido.py          # Script principal do modo CONTENDER
├── executar_contender.py           # Interface de execução
├── teste_contender_completo.py     # Testes completos
├── INICIAR_CONTENDER.bat          # Inicializador Windows
└── diagnosticar_contender.py      # Diagnóstico de problemas
```

## 🚀 Como Usar

### 1. Método Fácil (Recomendado)
```bash
# No Windows
dev\scripts\INICIAR_CONTENDER.bat

# No terminal
cd dev/scripts
python executar_contender.py
```

### 2. Método Avançado
```bash
cd dev/scripts
python contender_corrigido.py
```

### 3. Executar Testes
```bash
cd dev/scripts
python teste_contender_completo.py
```

## 📋 Pré-requisitos

### ✅ Requisitos Obrigatórios
1. **Python 3.7+** instalado
2. **Chrome/Chromium** instalado
3. **ChromeDriver** compatível
4. **Profile do Chrome** configurado com login no KeyDrop
5. **Conexão à internet** estável

### 📦 Dependências Python
```bash
pip install selenium
pip install webdriver-manager  # (opcional, para gerenciar ChromeDriver)
```

## ⚙️ Configuração

### 1. Configurar Profile do Chrome
```bash
# Localizar profiles existentes
ls profiles/

# Verificar se profile tem login salvo
# Arquivo: profiles/Profile-X/Preferences
```

### 2. Verificar ChromeDriver
```bash
# Teste manual
python -c "from selenium import webdriver; webdriver.Chrome()"
```

### 3. Testar Acesso ao Site
```bash
# Executar diagnóstico
python diagnosticar_contender.py
```

## 📊 Monitoramento

### 📈 Estatísticas Disponíveis
- **Execuções Totais**: Número de vezes que o bot foi executado
- **Sucessos**: Execuções completadas com sucesso
- **Falhas**: Execuções que falharam
- **Giveaways Participados**: Total de participações realizadas
- **Última Execução**: Data/hora da última execução
- **Próxima Execução**: Data/hora programada para próxima execução

### 📄 Logs Gerados
```
dev/logs/
├── teste_contender_YYYYMMDD_HHMMSS.log
├── resultado_teste_YYYYMMDD_HHMMSS.json
├── contender_stats.json
└── contender_execution_YYYYMMDD_HHMMSS.log
```

## 🎯 Seletores Utilizados

### 🔍 Métodos de Detecção
1. **Link Text**: `"Participar no Sorteio"`
2. **XPath Específico**: `//*[@id="main-view"]/div/div[2]/div/div[3]/div/div/div/div/div[5]/a`
3. **CSS Selector**: `div.flex.flex-col.gap-2\.5 > a`
4. **Href Pattern**: `a[href*='giveaway']`

### 🎯 Fluxo de Execução
```
1. Inicializar Chrome com perfil
2. Acessar site principal (key-drop.com)
3. Verificar se usuário está logado
4. Navegar para página de giveaways
5. Encontrar botões "Participar no Sorteio"
6. Clicar em cada botão encontrado
7. Aguardar processamento
8. Registrar resultados
9. Limpar recursos
```

## 🔧 Solução de Problemas

### ❌ Problemas Comuns

#### 1. ChromeDriver não encontrado
```bash
# Solução 1: Instalar webdriver-manager
pip install webdriver-manager

# Solução 2: Download manual
# https://chromedriver.chromium.org/
```

#### 2. Profile não funciona
```bash
# Verificar se profile existe
ls profiles/Profile-*/Preferences

# Criar novo profile se necessário
# Fazer login manual no Chrome
```

#### 3. Site não carrega
```bash
# Verificar conexão
ping key-drop.com

# Testar acesso manual
# Abrir Chrome e acessar key-drop.com
```

#### 4. Botões não encontrados
```bash
# Executar diagnóstico
python diagnosticar_contender.py

# Verificar estrutura da página
python inspecionar_contender.py
```

### 🔍 Diagnóstico
```bash
# Teste completo
python teste_contender_completo.py

# Verificar dependências
python -c "import selenium; print(selenium.__version__)"

# Teste de acesso
python -c "from selenium import webdriver; d = webdriver.Chrome(); d.get('https://key-drop.com'); print(d.title); d.quit()"
```

## 📋 Modos de Execução

### 1. Execução Única
- Executa uma vez e para
- Ideal para testes
- Mostra resultados imediatamente

### 2. Modo Automático
- Executa a cada 1 hora
- Roda continuamente
- Para com Ctrl+C

### 3. Modo Teste
- Executa testes de verificação
- Não participa de giveaways
- Valida configuração

## 📝 Exemplos de Uso

### Exemplo 1: Execução Básica
```python
from contender_corrigido import ContenderBot

bot = ContenderBot()
profile_path = "profiles/Profile-1"
resultado = bot.executar_modo_contender(profile_path)
```

### Exemplo 2: Execução com Logs
```python
import logging

logging.basicConfig(level=logging.INFO)
bot = ContenderBot()
resultado = bot.executar_modo_contender("profiles/Profile-1")
```

### Exemplo 3: Execução Programada
```python
import schedule
import time

def executar_contender():
    bot = ContenderBot()
    bot.executar_modo_contender("profiles/Profile-1")

# Executar a cada hora
schedule.every().hour.do(executar_contender)

while True:
    schedule.run_pending()
    time.sleep(1)
```

## 🛡️ Segurança

### 🔒 Medidas de Segurança
- **User-Agent Real**: Simula navegador real
- **Timing Humano**: Pausas entre ações
- **Perfil Existente**: Usa perfil com histórico
- **Configurações Anti-Detecção**: Desabilita flags de automação

### ⚠️ Avisos Importantes
- **Use por sua conta e risco**: Automação pode violar ToS
- **Monitore execuções**: Verifique logs regularmente
- **Mantenha atualizado**: Seletores podem mudar
- **Respeite rate limits**: Não execute muito frequentemente

## 🔄 Atualizações

### 📅 Versão Atual
- **Versão**: 1.0.0
- **Data**: 2024-12-19
- **Desenvolvedor**: Billy Franck (wmedrado)

### 🔄 Histórico de Mudanças
- **v1.0.0**: Implementação inicial completa
- **v1.0.1**: Correções de seletores
- **v1.0.2**: Melhorias na detecção de login

### 🔮 Próximas Funcionalidades
- [ ] Integração com Discord para notificações
- [ ] Dashboard web para monitoramento
- [ ] Suporte a múltiplos sites
- [ ] Filtros de giveaways por valor
- [ ] Backup automático de configurações

## 📞 Suporte

### 👨‍💻 Desenvolvedor
- **Nome**: Billy Franck
- **Discord**: wmedrado
- **GitHub**: [Repositório do projeto]

### 🐛 Reportar Problemas
1. Executar diagnóstico completo
2. Salvar logs de erro
3. Descrever o problema detalhadamente
4. Entrar em contato via Discord

### 💡 Sugestões
- Abra issues no GitHub
- Entre em contato via Discord
- Contribua com melhorias

---

**⚠️ Disclaimer**: Este software é fornecido "como está" sem garantias. Use por sua conta e risco. O desenvolvedor não se responsabiliza por banimentos, perdas ou danos resultantes do uso deste software.
