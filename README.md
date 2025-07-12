# 🤖 Keydrop Bot Professional

Automatize suas participações em sorteios do Keydrop de forma prática! Esta versão utiliza um backend **FastAPI** com uma interface web leve em HTML/JavaScript.

## ✨ Funcionalidades
- 🔗 Automação completa das interações no site Keydrop
- 🌐 Backend FastAPI com interface web simples
- 📊 Painel opcional com gráficos de CPU/RAM e controles do bot
- 💬 Integração com notificações (Windows e Telegram)
- 🔄 Sistema de atualização automática por JSON hospedado

## 📁 Estrutura do Projeto
```text
keydrop-bot-v3/
├── bot_keydrop/           # Versão profissional (backend + frontend)
│   ├── backend/           # API FastAPI e lógica do bot
│   ├── frontend/          # Interface web simples
│   ├── production_launcher.py  # Launcher para uso em produção
│   └── startup.py         # Início rápido para desenvolvimento
├── bot-keydrop-main/      # Versões 2.x legadas
├── config.json            # Exemplo de configuração do bot
├── install_requirements.bat  # Script de instalação de dependências
└── README.md              # Este arquivo
```

## 🛠 Requisitos
- **Sistema operacional**: Windows 10 ou superior
- **Python**: 3.8 ou mais recente
- **Google Chrome/Chromium** instalado
- **Internet** para baixar dependências e acessar o Keydrop

As bibliotecas necessárias para a API estão em `bot_keydrop/backend/requirements.txt`.
Para a interface desktop, instale também os pacotes listados em `bot_keydrop/requirements.txt`.
O script `install_requirements.bat` cobre ambos automaticamente.

## ⚡ Instalação Rápida (Windows)
1. Clone este repositório ou baixe o código.
2. Execute `install_requirements.bat` para instalar todas as dependências.
3. Instale os navegadores do Playwright executando `python -m playwright install` caso o script não faça isso automaticamente.

## 🚀 Como Usar
### Desenvolvimento
```bash
python bot_keydrop/startup.py
```
O script inicia o backend FastAPI na porta `8000` e um servidor HTTP simples para a interface web (porta `3000`). A interface fica em `http://localhost:3000` e a API em `http://localhost:8000`. Um painel opcional pode ser acessado em `http://localhost:8000/ui`.

### Produção ou Executável
Para iniciar a versão utilizada em produção ou em um executável criado com PyInstaller:
```bash
python bot_keydrop/production_launcher.py
```
O launcher verifica o Chrome, cria as pastas necessárias, inicia o servidor e abre a interface do bot.

### Lançador com Seleção de Interface
Escolha entre a interface web clássica ou a nova interface em DearPyGUI com:
```bash
python bot_keydrop/interface_selector.py
```

### Launcher Unificado
Para iniciar apenas a interface desktop, somente a API ou ambos:
```bash
python launcher.py
```

## 🔄 Sistema de Atualização Automática
O utilitário `update_manager.py` verifica se há uma versão mais recente por meio de um arquivo JSON hospedado. Caso uma nova versão seja encontrada, o script baixa o pacote `.zip` ou `.exe` e reinicia o bot.
```bash
python bot_keydrop/update_manager.py
```
Um exemplo de JSON pode ser visto em `update_info_example.json`.

## ⚙ Configuração do Bot
As configurações padrão estão em `config.json`. Modifique os campos conforme necessário (número de guias, velocidade, integração com Discord etc.). A interface permite editar essas configurações. Há também a opção `stealth_headless_mode` para executar o navegador em modo headless protegido contra detecção.

## 🧪 Testes
Para executar quaisquer testes presentes no repositório:
```bash
pytest -q       # se o pytest estiver configurado
python -m unittest discover -v
```

## 🛠 Builds Disponíveis
Execute `python gerador_exe/builder.py` para gerar os executáveis. O script cria automaticamente dois arquivos em `gerador_exe/binario_final`:

- `KeydropBot.exe` – versão padrão para uso cotidiano.
- `KeydropBot_DEBUG.exe` – build de depuração que testa todos os componentes e registra logs detalhados.

- **Produção:** gera um executável enxuto pronto para uso.
- **Debug:** inclui ferramentas de diagnóstico e executa `debug_tester.py` ao iniciar.

Para gerar o build padrão:

```bash
python gerador_exe/builder.py
```

Para criar o executável de debug e ativar o modo de desenvolvimento defina a variável de ambiente `MODO_DEBUG=1`:

```bash
MODO_DEBUG=1 python gerador_exe/builder.py
```

Com `MODO_DEBUG=1` o programa exibe todos os logs, pinta a interface de vermelho e executa uma falha simulada após alguns segundos.

## 📦 Instalador Windows
Depois de gerar o executável em `dist/KeydropBot_Professional.exe`, execute
`python gerador_exe/installer_builder.py --exe dist/KeydropBot_Professional.exe --arch x64 --version <versão>`
para gerar instaladores `.exe` e `.msi` via `makensis` e `wixl`.

## 🐳 Docker
Com Docker instalado, é possível levantar rapidamente a API executando:

```bash
docker compose up --build
```

O serviço ficará acessível na porta `8000`.

## 📄 Licença
Distribuído sob a licença MIT. Consulte os arquivos de documentação das pastas internas para mais detalhes.

## 🔔 Notificações
Auxiliares de notificação ficam em `bot_keydrop/backend/notifications`:
- **Windows**: notificações desktop via `win10toast`.
- **Telegram**: envio simples de mensagens via API do Telegram.


## 🚀 Build Pipeline
Execute `python ci/build_pipeline.py --snapshot` para rodar lint, testes e gerar `build/build_info.txt`.
Use `launcher.py --watch` para iniciar o monitoramento em tempo real que grava `logs/live_monitor.html`.

## 🚀 Integração Contínua

O repositório possui um workflow do GitHub Actions que valida cada Pull Request.
Ele instala as dependências, executa `flake8`, `black` e roda toda a suíte de testes com cobertura.
Após os testes, um revisor automático avalia os logs e gera `build_results/auto_review.txt`.
Somente problemas encontrados nos arquivos modificados pelo PR contam como erro crítico.
Se tais erros forem detectados, o PR é bloqueado; caso contrário, ele é aprovado automaticamente.
Os relatórios são gerados em `tests/test_report.html` e `tests/coverage.txt`.

