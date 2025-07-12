# Keydrop Bot Professional

Este repositório contém várias versões do **Keydrop Bot**, uma aplicação para automatizar participações em sorteios do site Keydrop. A edição mais recente utiliza um backend FastAPI com frontend leve em HTML/JavaScript.

## Estrutura do Projeto

```
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

## Requisitos

- **Sistema operacional**: Windows 10 ou superior
- **Python**: 3.8 ou mais recente
- **Google Chrome/Chromium** instalado
- **Internet** para baixar dependências e acessar o Keydrop

As bibliotecas Python necessárias estão listadas em `bot_keydrop/backend/requirements.txt`.

## Instalação Rápida (Windows)

1. Clone este repositório ou baixe o código.
2. Execute `install_requirements.bat` para instalar todas as dependências.
3. Instale os navegadores do Playwright executando `python -m playwright install` se o script não fizer isso automaticamente.

## Como Usar

### Desenvolvimento

```bash
python bot_keydrop/startup.py
```

O script `startup.py` inicia o backend FastAPI na porta `8000` e um servidor
HTTP simples para a interface web (porta `3000`). Após iniciado, a interface
pode ser acessada em `http://localhost:3000` e a API em
`http://localhost:8000`.

### Produção ou Executável

Para iniciar a versão utilizada em produção ou em um executável criado com
PyInstaller, utilize o `production_launcher.py`:

```bash
python bot_keydrop/production_launcher.py
```

O launcher verifica o Chrome, cria as pastas necessárias, inicia o servidor e
abre o navegador padrão apontando para a interface do bot.

### Lançador com Seleção de Interface

Se preferir escolher entre a interface web clássica ou a nova interface moderna
em DearPyGUI, utilize o `interface_selector.py`:

```bash
python bot_keydrop/interface_selector.py
```

### Launcher Unificado

Para iniciar apenas a interface desktop, somente a API FastAPI ou ambos ao mesmo tempo, utilize o `launcher.py` na raiz do projeto:

```bash
python launcher.py
```

## Configuração do Bot

As configurações padrão encontram-se no arquivo `config.json` na raiz do
repositório. Altere os campos conforme a necessidade (número de guias, velocidade,
integração com Discord, etc.). A interface também permite editar essas
configurações.

## Testes

Para executar quaisquer testes presentes no repositório:

```bash
pytest -q       # se o pytest estiver configurado
python -m unittest discover -v
```

## Licença

Este projeto é distribuído sob a licença MIT. Consulte os arquivos de
documentação das pastas internas para informações detalhadas de cada versão.
=======
# keybotv3
Keydrop Bot v3

This project automates interactions with Keydrop using a FastAPI backend.

## Notifications

Additional notification helpers are available under `bot_keydrop/backend/notifications`:

- **Windows**: desktop notifications using `win10toast`.
- **Telegram**: simple message sending via the Telegram Bot API.
