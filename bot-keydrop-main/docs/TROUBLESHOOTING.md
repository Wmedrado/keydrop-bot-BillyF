# 🛠️ GUIA DE SOLUÇÃO DE PROBLEMAS

## 🔧 Problemas Comuns e Soluções

### ❌ **"Python não foi encontrado"**
**Problema**: O sistema não consegue encontrar o Python.

**Soluções**:
1. Instale Python 3.8+ do site oficial: https://python.org
2. Certifique-se de marcar "Add Python to PATH" na instalação
3. Reinicie o terminal/prompt após a instalação
4. Teste: `python --version`

### ❌ **"Erro ao instalar dependências"**
**Problema**: Versões incompatíveis de dependências.

**Soluções**:
1. **SOLUÇÃO RÁPIDA**: Execute `CORRIGIR_DEPENDENCIAS.bat`
2. **OU** Execute: `python corrigir_dependencias.py`
3. **OU** Manual:
   ```bash
   pip install --upgrade pip
   pip install selenium>=4.15.0
   pip install webdriver-manager>=4.0.0
   pip install requests>=2.31.0
   pip install psutil>=5.9.0
   pip install pywin32
   ```

### ❌ **"Could not find a version that satisfies the requirement pywin32==306"**
**Problema**: Versão específica do pywin32 não compatível com Python mais recente.

**Soluções**:
1. **SOLUÇÃO AUTOMÁTICA**: Execute `CORRIGIR_DEPENDENCIAS.bat`
2. **OU** Execute: `pip install pywin32` (sem versão específica)
3. **OU** Atualize Python para versão mais recente compatível

### ❌ **"ChromeDriver não encontrado"**
**Problema**: Driver do Chrome não está disponível.

**Soluções**:
1. Instale Google Chrome: https://google.com/chrome
2. O bot baixa o driver automaticamente
3. Se falhar, baixe manualmente: https://chromedriver.chromium.org
4. Coloque o chromedriver.exe na pasta do bot

### ❌ **"Erro ao criar perfis"**
**Problema**: Falta permissão para criar diretórios.

**Soluções**:
1. Execute como administrador
2. Verifique permissões da pasta
3. Crie manualmente as pastas: `profiles`, `data`, `backup`

### ❌ **"Bot não participa de sorteios"**
**Problema**: Bot não consegue encontrar sorteios.

**Soluções**:
1. Verifique se está logado no KeyDrop
2. Desative o modo login após fazer login
3. Verifique conexão com internet
4. Aguarde aparecer sorteios na página

### ❌ **"Interface não abre"**
**Problema**: GUI não carrega.

**Soluções**:
1. Verifique se tkinter está instalado: `python -m tkinter`
2. Instale se necessário: `pip install tk`
3. Execute: `python gui_keydrop.py` diretamente

### ❌ **"Muitos bots causam lentidão"**
**Problema**: Sistema lento com muitos bots.

**Soluções**:
1. Ative o modo headless para >20 bots
2. Aumente a RAM disponível
3. Feche outros programas
4. Use o otimizador: `python final_optimizer.py`

### ❌ **"Bot para sozinho"**
**Problema**: Bot para de funcionar.

**Soluções**:
1. Verifique os logs na interface
2. Use a função "Reiniciar Guias"
3. Verifique se o Chrome não fechou
4. Reinicie o bot completamente

### ❌ **"Saldo não atualiza"**
**Problema**: Contador de saldo não funciona.

**Soluções**:
1. Verifique se está logado no KeyDrop
2. Aguarde alguns minutos para atualizar
3. Desative/reative o modo login
4. Use "Reiniciar Guias"

### ❌ **"Discord webhook não funciona"**
**Problema**: Notificações Discord não chegam.

**Soluções**:
1. Verifique se o webhook está correto
2. Teste o webhook manualmente
3. Verifique conexão com internet
4. Verifique se o Discord está funcionando

## 🔍 Diagnóstico Avançado

### **Verificar Logs**
```bash
# Execute com logs detalhados
python main.py --debug
```

### **Testar Componentes**
```bash
# Testar melhorias
python teste_melhorias.py

# Otimizar sistema
python final_optimizer.py

# Testar GUI
python gui_keydrop.py
```

### **Verificar Recursos**
1. Abra o Gerenciador de Tarefas
2. Monitore uso de CPU e RAM
3. Verifique processos do Chrome
4. Feche processos órfãos se necessário

## 📞 Suporte

### **Informações do Sistema**
Antes de reportar problemas, colete:
- Versão do Windows
- Versão do Python (`python --version`)
- Versão do Chrome
- Mensagens de erro completas
- Número de bots sendo executados

### **Arquivos de Log**
Verifique os arquivos:
- `bot_config.json` - Configurações
- `data/Profile-*/chrome_debug.log` - Logs do Chrome
- Console do Python - Mensagens de erro

### **Reset Completo**
Se nada funcionar:
1. Pare todos os bots
2. Feche todos os processos Chrome
3. Delete a pasta `profiles`
4. Delete a pasta `data`
5. Execute: `python final_optimizer.py`
6. Reinicie o bot

## 🚨 Problemas Críticos

### **Bot Detectado pelo KeyDrop**
**Sintomas**: Contas banidas, captchas frequentes
**Soluções**:
1. Reduza o número de bots
2. Aumente os intervalos entre ações
3. Use perfis diferentes
4. Varie os horários de uso

### **Uso Excessivo de Recursos**
**Sintomas**: Sistema travando, lentidão geral
**Soluções**:
1. Reduza para máximo 50 bots
2. Ative modo headless
3. Aumente RAM do sistema
4. Use SSD ao invés de HDD

### **Erro de Segurança**
**Sintomas**: Antivírus bloqueia o bot
**Soluções**:
1. Adicione exceção no antivírus
2. Execute como administrador
3. Desative proteção em tempo real temporariamente

---

💡 **Dica**: Sempre execute `python final_optimizer.py` após resolver problemas para garantir que o sistema esteja otimizado.
