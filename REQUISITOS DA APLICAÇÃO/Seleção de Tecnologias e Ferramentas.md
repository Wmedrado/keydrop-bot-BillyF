
# Seleção de Tecnologias e Ferramentas

## 1. Tecnologias para a Interface do Usuário (Frontend)

Para a camada de interface do usuário, que exige uma interface moderna, responsiva e com baixo consumo de recursos, as seguintes tecnologias foram consideradas com base na pesquisa:

*   **Electron:** Permite construir aplicações desktop multiplataforma usando tecnologias web (HTML, CSS, JavaScript). É amplamente utilizado e possui uma vasta comunidade e ecossistema. No entanto, é conhecido por seu consumo de recursos relativamente alto, o que pode ser uma desvantagem para o requisito de 


baixo desempenho.

*   **Tauri:** Uma alternativa mais moderna e leve ao Electron. Utiliza a linguagem Rust para o backend e o motor de renderização do sistema operacional para o frontend, resultando em aplicações menores e mais eficientes em termos de recursos. É uma excelente opção para o requisito de baixo consumo de RAM e CPU.

*   **React Native for Windows + macOS:** Permite criar aplicações nativas para Windows e macOS usando React. Oferece uma performance nativa e uma experiência de usuário mais integrada ao sistema operacional. Pode ser uma boa opção se a equipe de desenvolvimento já tiver experiência com React.

*   **.NET MAUI:** Framework da Microsoft para criar aplicações desktop e móveis multiplataforma com C# e XAML. Oferece uma boa performance e integração com o ecossistema .NET.

*   **Flutter:** Framework do Google para criar aplicações multiplataforma com uma única base de código. É conhecido por sua alta performance e interfaces de usuário expressivas. A comunidade e o ecossistema estão em rápido crescimento.

**Decisão:**

Considerando os requisitos de alta performance, baixo consumo de recursos e uma interface moderna, **Tauri** se destaca como a melhor opção para o frontend. Sua arquitetura leve e o uso de tecnologias web para a interface permitem o desenvolvimento de uma aplicação rápida, eficiente e com um visual de alto padrão. A combinação de Rust no backend com um frontend em React ou Vue.js (que pode ser integrado com o Tauri) oferece uma base sólida para o projeto.




## 2. Tecnologias para a Lógica de Negócio e Automação (Backend)

Para a camada de lógica de negócio e automação, que exige controle preciso do navegador, baixo consumo de recursos e integração com o sistema operacional, as seguintes tecnologias foram avaliadas:

### 2.1. Automação de Navegador

*   **Playwright:** É uma biblioteca moderna e de alto desempenho para automação de navegadores. Suporta Chromium, Firefox e WebKit com uma única API, e é otimizada para cenários de automação em larga escala, incluindo execução assíncrona e gerenciamento de múltiplas instâncias. Sua capacidade de operar em modo headless (sem interface gráfica) e o foco em performance a tornam ideal para o requisito de baixo consumo de recursos e gerenciamento de 100 guias.

*   **Selenium:** Uma ferramenta amplamente utilizada para automação de navegadores. Embora robusta, pode ser mais intensiva em recursos e complexa de gerenciar em cenários de alta concorrência de guias em comparação com o Playwright.

*   **Pyppeteer:** Uma porta Python do Puppeteer, que é uma biblioteca Node.js para controle do Chrome/Chromium. É uma boa opção, mas o Playwright oferece suporte a mais navegadores e tem um desenvolvimento mais ativo.

**Decisão:**

**Playwright** é a escolha mais adequada para a automação do Chrome devido à sua performance, capacidade de lidar com múltiplas instâncias de forma eficiente, suporte a execução assíncrona e menor consumo de recursos em comparação com outras opções. A biblioteca `playwright-python` será utilizada.

### 2.2. Monitoramento de Sistema

*   **psutil:** Uma biblioteca Python multiplataforma que fornece acesso a detalhes do sistema e do processo, como utilização de CPU, memória, discos, rede e processos em execução. É amplamente recomendada para monitoramento de recursos devido à sua facilidade de uso e abrangência de informações.

**Decisão:**

**psutil** será utilizada para coletar os dados de uso de RAM, CPU, HD e consumo de internet, fornecendo as métricas necessárias para a interface de estatísticas.

### 2.3. Integração com Discord Webhook

*   **`discord-webhook` (PyPI):** Uma biblioteca Python simples e eficaz para enviar mensagens para webhooks do Discord. Permite o envio de texto, embeds e até arquivos, o que é ideal para as notificações de início/fim de sessão, erros, relatórios e lucros.

*   **`requests`:** A biblioteca `requests` pode ser usada diretamente para fazer requisições HTTP POST para o endpoint do webhook do Discord. Embora funcione, uma biblioteca dedicada como `discord-webhook` simplifica o processo e oferece funcionalidades mais específicas para embeds e formatação.

**Decisão:**

A biblioteca **`discord-webhook`** será utilizada para a integração com o Discord, facilitando o envio de notificações formatadas e relatórios.

### 2.4. Estrutura do Backend

Para a estrutura do backend, considerando a necessidade de comunicação em tempo real com o frontend (Tauri) e a gestão de tarefas assíncronas, Python com um framework assíncrono seria a melhor escolha:

*   **FastAPI:** Um framework web moderno e rápido para construir APIs com Python 3.7+ baseado em tipagem padrão do Python. É conhecido por sua alta performance (comparável a Node.js e Go), documentação automática e suporte a operações assíncronas (`async/await`). Pode ser facilmente integrado com WebSockets para a comunicação em tempo real com o frontend.

*   **Flask:** Um microframework web para Python. É leve e flexível, mas para o requisito de alta performance e comunicação em tempo real com WebSockets, o FastAPI é mais otimizado.

**Decisão:**

**FastAPI** será o framework principal para o backend, fornecendo a API para o frontend e gerenciando a lógica de negócio, automação e monitoramento. Sua capacidade assíncrona é crucial para o gerenciamento eficiente de múltiplas guias do Chrome e para a comunicação em tempo real com o frontend via WebSockets.

## 3. Tecnologias para Empacotamento e Executável

*   **PyInstaller:** Uma ferramenta que empacota aplicações Python em executáveis autônomos para Windows, Linux, macOS e AIX. É amplamente utilizada e confiável para criar o aplicativo executável final.

**Decisão:**

**PyInstaller** será utilizado para criar o executável do bot, facilitando a distribuição e o uso em diferentes máquinas.

