# KeyDrop Bot - Professional Edition v2.0

**Desenvolvido por William Medrado**

## 🚀 Características

- **Interface Gráfica Profissional**: Controle total via GUI moderna e expansível (1000x700)
- **Multi-Perfil**: Suporte a até 200 janelas simultâneas com perfis independentes
- **Configurável**: Tempos de espera totalmente personalizáveis
- **Monitoramento Avançado**: Status em tempo real, métricas de sistema e contador de saldo
- **Anti-Detecção**: Sistema avançado para evitar bloqueios
- **24/7 Ready**: Projetado para uso intensivo contínuo
- **Modo Login**: Suporte específico para login via Steam
- **Reiniciar Guias**: Função para reiniciar drivers sem parar o bot
- **Otimização de Performance**: Suporte otimizado para até 200 janelas

## 📋 Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado
- Windows 10/11

## 🛠️ Instalação

1. **Clone/Baixe** o projeto
2. **Execute** o `iniciar_bot.bat` OU:
   ```bash
   pip install -r requirements.txt
   python main.py
   ```

## 🎯 Como Usar

1. **Abra** o `main.py` ou execute `iniciar_bot.bat`
2. **Configure** o número de janelas e tempos de espera
3. **Clique** em "Iniciar Bots"
4. **Faça login** em cada janela que abrir
5. **Aguarde** - o bot funcionará automaticamente

## ⚙️ Configurações

- **Número de Janelas**: 1-200 perfis simultâneos (com validação de recursos)
- **Intervalo entre Sorteios**: Tempo de espera entre tentativas (30-600 segundos)
- **Intervalo entre Tabs**: Delay entre mudanças de abas (1-10 segundos)
- **Perfis Independentes**: Cada janela tem seu próprio perfil Chrome
- **Modo Headless**: Execução sem interface gráfica (recomendado para >50 bots)
- **Modo Login**: Abertura automática da tela de login da Steam
- **Webhook Discord**: Notificações automáticas para alertas

## 📊 Monitoramento

- Status em tempo real de cada bot com cores indicativas
- Contador de participações bem-sucedidas por bot
- Saldo de skins individual e total em tempo real
- Registro de erros e alertas automatizados
- Tempo de execução em tempo real
- Métricas de sistema (CPU, RAM, processos Chrome)
- Painel de informações consolidado e otimizado

## 🔧 Funcionalidades Avançadas

- **Reiniciar Guias**: Reinicia drivers sem parar o bot (botão dedicado)
- **Configuração de Startup**: Inicialização automática do Windows
- **Otimizador de Performance**: Ajustes automáticos baseados no número de bots
- **Sistema Anti-Spam**: Remoção de notificações desnecessárias
- **Validação de Recursos**: Verificação automática antes de iniciar muitos bots

## 🔧 Estrutura do Projeto

```
BOT-KEYDROP-BY-WILL/
├── main.py                 # Arquivo principal
├── gui_keydrop.py         # Interface gráfica
├── keydrop_bot.py         # Lógica do bot
├── requirements.txt       # Dependências
├── iniciar_bot.bat       # Script de inicialização
├── README.md             # Este arquivo
└── profiles/             # Perfis dos navegadores (criado automaticamente)
```

## 🛡️ Segurança

- Anti-detecção WebDriver
- User-Agent personalizado
- Perfis isolados
- Tratamento de exceções robusto

## 💡 Dicas

- Use um número moderado de janelas para evitar sobrecarga
- Deixe o bot rodando continuamente para melhor performance
- Monitore os logs para identificar problemas
- Mantenha o Chrome atualizado

## 📞 Suporte

Para suporte técnico ou melhorias, entre em contato com o desenvolvedor:

**👨‍💻 Desenvolvido por:** William Medrado (wmedrado)  
**📞 Discord:** wmedrado  
**📧 Email:** willfmedrado@gmail.com  
**🌐 GitHub:** https://github.com/wmedrado/bot-keydrop

---

**Desenvolvido por William Medrado para uso profissional. Use com responsabilidade.**
