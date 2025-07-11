# Documentação Técnica do Bot de Interação com Chrome

Este documento consolida os requisitos, a arquitetura e o prompt detalhado para o desenvolvimento de um bot de alto padrão para interação com o Google Chrome. O objetivo é fornecer uma visão abrangente do projeto, servindo como referência para o desenvolvimento e futuras manutenções.




## 1. Requisitos e Arquitetura do Sistema





# Requisitos e Arquitetura do Bot de Interação com Chrome

## 1. Requisitos Funcionais

O bot deve ser capaz de:

*   **Interação com Guias do Chrome:**
    *   Abrir e fechar guias do Google Chrome de forma programática.
    *   Navegar para URLs específicas em cada guia.
    *   Clicar em elementos específicos da página (botões, links, etc.).
    *   Preencher campos de formulário.
    *   Extrair informações de elementos da página.
    *   Gerenciar múltiplas guias simultaneamente de forma assíncrona.

*   **Automação de Sorteios (Keydrop):**
    *   Participar de sorteios no site Keydrop, clicando nos botões de participação.
    *   Aguardar um tempo configurável (padrão 3 minutos para sorteios 'AMATEUR') entre as participações na mesma guia.
    *   Ciclar entre as guias para garantir a participação em todos os sorteios disponíveis.

*   **Gestão de Falhas e Resiliência:**
    *   Detectar falhas na participação do sorteio (ex: botão não encontrado, erro de carregamento da página).
    *   Tentar novamente a participação um número configurável de vezes (padrão 5 tentativas).
    *   Em caso de falha após as tentativas, reiniciar automaticamente a guia específica do navegador e tentar novamente até o sucesso.

*   **Configuração e Parametrização:**
    *   Permitir a configuração da quantidade de guias a serem abertas.
    *   Permitir a configuração da velocidade de execução das ações (tempo de espera entre ações).
    *   Permitir a configuração do número de tentativas em caso de falha.
    *   Salvar e carregar configurações persistentes.

*   **Monitoramento de Performance do Computador:**
    *   Exibir dados de uso de RAM, CPU e HD.
    *   Exibir o consumo total de internet em GB.
    *   Atualizar esses dados em tempo real na interface.

*   **Integração com Discord Webhook:**
    *   Enviar notificações para um webhook do Discord sobre:
        *   Início e fim de sessão do bot.
        *   Erros e falhas na execução.
        *   Relatórios de resultados (participações, sucessos, falhas).
        *   Lucros obtidos (se aplicável e extraível do site).

*   **Interface de Usuário (UI):**
    *   Interface moderna, intuitiva e responsiva.
    *   Três guias principais:
        *   **Configurações:** Campos parametrizáveis, botões de reiniciar guias, parar todos os bots, iniciar todos os bots, limpar cache (sem perder dados de login), salvar configurações.
        *   **Estatísticas:** Exibição dos dados de performance do computador (RAM, CPU, HD, internet).
        *   **Relatório:** Exibição de relatórios de resultados e lucros.
    *   Botão para verificar e informar sobre novas atualizações do aplicativo.
    *   Capacidade de adicionar novos botões e funcionalidades futuras.

*   **Performance e Otimização:**
    *   Alta performance e baixo consumo de recursos (RAM, CPU) para rodar em máquinas com baixo desempenho.
    *   Capacidade de gerenciar e encerrar 100 guias do Chrome sem travar o aplicativo.
    *   Execução assíncrona das ações para evitar travamentos e otimizar o uso de recursos.
    *   Mecanismos de gestão de memória e CPU eficientes.

*   **Executável:**
    *   Gerar um aplicativo executável para fácil distribuição e uso.

## 2. Requisitos Não Funcionais

*   **Performance:** O aplicativo deve ser altamente otimizado para baixo consumo de RAM e CPU, permitindo a execução fluida mesmo com 100 guias do Chrome abertas e em máquinas de baixo desempenho.
*   **Confiabilidade:** O bot deve ser robusto e resiliente a falhas, com mecanismos de retry e recuperação automática.
*   **Usabilidade:** A interface do usuário deve ser intuitiva e fácil de usar, mesmo para usuários não técnicos.
*   **Manutenibilidade:** O código deve ser bem estruturado, modular e fácil de manter e estender.
*   **Segurança:** O aplicativo deve garantir a segurança dos dados de login e outras informações sensíveis.
*   **Escalabilidade:** A arquitetura deve permitir a adição de novas funcionalidades e a expansão do número de guias gerenciadas no futuro.
*   **Responsividade:** A interface deve se adaptar a diferentes tamanhos de tela e resoluções.




## 3. Arquitetura do Sistema

A arquitetura proposta para o bot será modular e distribuída, visando alta performance, responsividade e facilidade de manutenção. Será composta por três camadas principais:

### 3.1. Camada de Interface do Usuário (Frontend)

Esta camada será responsável por toda a interação com o usuário, exibindo as configurações, estatísticas e relatórios. Deverá ser construída com uma tecnologia que permita a criação de interfaces modernas, responsivas e de alto desempenho.

*   **Componentes Principais:**
    *   **Dashboard de Configurações:** Interface para parametrizar o bot (quantidade de guias, velocidade, tentativas de retry, etc.), com botões de controle (iniciar, parar, reiniciar, limpar cache, salvar).
    *   **Dashboard de Estatísticas:** Exibição em tempo real de métricas de performance do sistema (RAM, CPU, HD, consumo de internet).
    *   **Dashboard de Relatórios:** Visualização de logs de execução, resultados de sorteios e lucros.
    *   **Sistema de Notificações:** Feedback visual para o usuário sobre o status do bot e eventos importantes.

### 3.2. Camada de Lógica de Negócio e Automação (Backend)

Esta camada será o coração do bot, responsável por toda a lógica de automação, gerenciamento de guias do Chrome, monitoramento de sistema e integração com serviços externos (Discord).

*   **Componentes Principais:**
    *   **Módulo de Gerenciamento de Navegador:** Responsável por iniciar, fechar e controlar instâncias do Google Chrome. Deverá utilizar uma biblioteca de automação de navegador robusta e eficiente.
    *   **Módulo de Automação de Páginas:** Contém a lógica para interagir com as páginas web (clicar em botões, preencher campos, extrair dados). Implementará os fluxos específicos para a participação em sorteios no Keydrop.
    *   **Módulo de Agendamento e Controle:** Gerencia a execução assíncrona das tarefas em cada guia, garantindo a parametrização de velocidade e o ciclo entre as guias. Responsável pelos mecanismos de retry e reinício de guias.
    *   **Módulo de Monitoramento de Sistema:** Coleta dados de uso de RAM, CPU, HD e consumo de rede do sistema operacional. Esses dados serão expostos para a camada de interface.
    *   **Módulo de Integração Discord:** Gerencia o envio de mensagens e relatórios para o webhook do Discord.
    *   **Módulo de Persistência:** Armazena e recupera as configurações do bot.

### 3.3. Camada de Comunicação

Esta camada será responsável pela comunicação entre o Frontend e o Backend, garantindo a troca de informações em tempo real e a execução de comandos.

*   **Tecnologias Potenciais:**
    *   **WebSockets:** Para comunicação em tempo real entre o Frontend e o Backend, ideal para atualizações de estatísticas e logs.
    *   **APIs RESTful:** Para comandos e configurações que não exigem comunicação em tempo real.

### 3.4. Considerações de Performance e Recursos

Para garantir o baixo consumo de recursos e a capacidade de lidar com 100 guias do Chrome, a arquitetura deverá priorizar:

*   **Assincronicidade:** Todas as operações de automação de navegador e comunicação devem ser assíncronas para evitar bloqueios e maximizar a utilização da CPU.
*   **Gerenciamento de Processos:** O bot deve ter controle granular sobre os processos do Chrome, permitindo o encerramento eficiente de guias e a recuperação de falhas sem afetar o aplicativo principal.
*   **Otimização de Memória:** Utilização de bibliotecas e técnicas que minimizem o consumo de memória, especialmente ao lidar com múltiplas instâncias do navegador.
*   **Execução Distribuída (Opcional, para escalabilidade futura):** Embora não seja um requisito inicial, a arquitetura deve permitir a futura expansão para execução de tarefas em diferentes processos ou até máquinas, caso a demanda por mais guias ou automações mais complexas aumente.

## 4. Fluxo de Operação Simplificado

1.  O usuário configura o bot na interface (Frontend) e clica em 'Iniciar'.
2.  O Frontend envia os parâmetros para o Backend via API/WebSocket.
3.  O Backend inicia o número configurado de instâncias do Chrome (ou reutiliza as existentes).
4.  Para cada guia, o Módulo de Automação de Páginas navega para o Keydrop e tenta participar do sorteio.
5.  O Módulo de Agendamento e Controle gerencia os tempos de espera e o ciclo entre as guias.
6.  Em caso de falha, o Módulo de Agendamento e Controle aciona o mecanismo de retry e, se necessário, reinicia a guia.
7.  O Módulo de Monitoramento de Sistema coleta dados de performance e os envia para o Frontend via WebSocket.
8.  O Módulo de Integração Discord envia notificações de status e relatórios.
9.  O usuário pode parar, reiniciar ou limpar o cache a qualquer momento através do Frontend.




## 2. Seleção de Tecnologias e Ferramentas





## 2. Seleção de Tecnologias e Ferramentas

### 2.1. Tecnologias para a Interface do Usuário (Frontend)

Para a camada de interface do usuário, que exige uma interface moderna, responsiva e com baixo consumo de recursos, as seguintes tecnologias foram consideradas com base na pesquisa:

*   **Electron:** Permite construir aplicações desktop multiplataforma usando tecnologias web (HTML, CSS, JavaScript). É amplamente utilizado e possui uma vasta comunidade e ecossistema. No entanto, é conhecido por seu consumo de recursos relativamente alto, o que pode ser uma desvantagem para o requisito de baixo desempenho.

*   **Tauri:** Uma alternativa mais moderna e leve ao Electron. Utiliza a linguagem Rust para o backend e o motor de renderização do sistema operacional para o frontend, resultando em aplicações menores e mais eficientes em termos de recursos. É uma excelente opção para o requisito de baixo consumo de RAM e CPU.

*   **React Native for Windows + macOS:** Permite criar aplicações nativas para Windows e macOS usando React. Oferece uma performance nativa e uma experiência de usuário mais integrada ao sistema operacional. Pode ser uma boa opção se a equipe de desenvolvimento já tiver experiência com React.

*   **.NET MAUI:** Framework da Microsoft para criar aplicações desktop e móveis multiplataforma com C# e XAML. Oferece uma boa performance e integração com o ecossistema .NET.

*   **Flutter:** Framework do Google para criar aplicações multiplataforma com uma única base de código. É conhecido por sua alta performance e interfaces de usuário expressivas. A comunidade e o ecossistema estão em rápido crescimento.

**Decisão:**

Considerando os requisitos de alta performance, baixo consumo de recursos e uma interface moderna, **Tauri** se destaca como a melhor opção para o frontend. Sua arquitetura leve e o uso de tecnologias web para a interface permitem o desenvolvimento de uma aplicação rápida, eficiente e com um visual de alto padrão. A combinação de Rust no backend com um frontend em React ou Vue.js (que pode ser integrado com o Tauri) oferece uma base sólida para o projeto.

### 2.2. Tecnologias para a Lógica de Negócio e Automação (Backend)

Para a camada de lógica de negócio e automação, que exige controle preciso do navegador, baixo consumo de recursos e integração com o sistema operacional, as seguintes tecnologias foram avaliadas:

#### 2.2.1. Automação de Navegador

*   **Playwright:** É uma biblioteca moderna e de alto desempenho para automação de navegadores. Suporta Chromium, Firefox e WebKit com uma única API, e é otimizada para cenários de automação em larga escala, incluindo execução assíncrona e gerenciamento de múltiplas instâncias. Sua capacidade de operar em modo headless (sem interface gráfica) e o foco em performance a tornam ideal para o requisito de baixo consumo de recursos e gerenciamento de 100 guias.

*   **Selenium:** Uma ferramenta amplamente utilizada para automação de navegadores. Embora robusta, pode ser mais intensiva em recursos e complexa de gerenciar em cenários de alta concorrência de guias em comparação com o Playwright.

*   **Pyppeteer:** Uma porta Python do Puppeteer, que é uma biblioteca Node.js para controle do Chrome/Chromium. É uma boa opção, mas o Playwright oferece suporte a mais navegadores e tem um desenvolvimento mais ativo.

**Decisão:**

**Playwright** é a escolha mais adequada para a automação do Chrome devido à sua performance, capacidade de lidar com múltiplas instâncias de forma eficiente, suporte a execução assíncrona e menor consumo de recursos em comparação com outras opções. A biblioteca `playwright-python` será utilizada.

#### 2.2.2. Monitoramento de Sistema

*   **psutil:** Uma biblioteca Python multiplataforma que fornece acesso a detalhes do sistema e do processo, como utilização de CPU, memória, discos, rede e processos em execução. É amplamente recomendada para monitoramento de recursos devido à sua facilidade de uso e abrangência de informações.

**Decisão:**

**psutil** será utilizada para coletar os dados de uso de RAM, CPU, HD e consumo de internet, fornecendo as métricas necessárias para a interface de estatísticas.

#### 2.2.3. Integração com Discord Webhook

*   **`discord-webhook` (PyPI):** Uma biblioteca Python simples e eficaz para enviar mensagens para webhooks do Discord. Permite o envio de texto, embeds e até arquivos, o que é ideal para as notificações de início/fim de sessão, erros, relatórios e lucros.

*   **`requests`:** A biblioteca `requests` pode ser usada diretamente para fazer requisições HTTP POST para o endpoint do webhook do Discord. Embora funcione, uma biblioteca dedicada como `discord-webhook` simplifica o processo e oferece funcionalidades mais específicas para embeds e formatação.

**Decisão:**

A biblioteca **`discord-webhook`** será utilizada para a integração com o Discord, facilitando o envio de notificações formatadas e relatórios.

#### 2.2.4. Estrutura do Backend

Para a estrutura do backend, considerando a necessidade de comunicação em tempo real com o frontend (Tauri) e a gestão de tarefas assíncronas, Python com um framework assíncrono seria a melhor escolha:

*   **FastAPI:** Um framework web moderno e rápido para construir APIs com Python 3.7+ baseado em tipagem padrão do Python. É conhecido por sua alta performance (comparável a Node.js e Go), documentação automática e suporte a operações assíncronas (`async/await`). Pode ser facilmente integrado com WebSockets para a comunicação em tempo real com o frontend.

*   **Flask:** Um microframework web para Python. É leve e flexível, mas para o requisito de alta performance e comunicação em tempo real com WebSockets, o FastAPI é mais otimizado.

**Decisão:**

**FastAPI** será o framework principal para o backend, fornecendo a API para o frontend e gerenciando a lógica de negócio, automação e monitoramento. Sua capacidade assíncrona é crucial para o gerenciamento eficiente de múltiplas guias do Chrome e para a comunicação em tempo real com o frontend via WebSockets.

### 2.3. Tecnologias para Empacotamento e Executável

*   **PyInstaller:** Uma ferramenta que empacota aplicações Python em executáveis autônomos para Windows, Linux, macOS e AIX. É amplamente utilizada e confiável para criar o aplicativo executável final.

**Decisão:**

**PyInstaller** será utilizado para criar o executável do bot, facilitando a distribuição e o uso em diferentes máquinas.




## 3. Prompt Detalhado para Desenvolvimento de Bot de Interação com Chrome




# Prompt Detalhado para Desenvolvimento de Bot de Interação com Chrome

## Objetivo Geral

Desenvolver um bot de alto padrão para interação com guias do Google Chrome, com foco em performance, responsividade, baixo consumo de recursos e integração com Discord. O bot deve ser um aplicativo executável com uma interface de usuário moderna e intuitiva, capaz de automatizar a participação em sorteios online (especificamente no Keydrop) e fornecer monitoramento de performance do sistema.

## Requisitos Funcionais Detalhados

1.  **Interação com Guias do Chrome:**
    *   Abrir, fechar e gerenciar múltiplas guias do Google Chrome de forma programática e assíncrona.
    *   Navegar para URLs específicas em cada guia.
    *   Realizar cliques em elementos da página (botões, links) e preencher campos de formulário.
    *   Extrair informações de elementos da página.
    *   Capacidade de encerrar até 100 guias do Chrome sem travar o aplicativo, com boa gestão de memória e CPU.

2.  **Automação de Sorteios (Keydrop):**
    *   Automatizar a participação em sorteios no site Keydrop, identificando e clicando nos botões de participação.
    *   Implementar um sistema de agendamento assíncrono para que o bot abra uma guia, participe do sorteio, aguarde um tempo padrão (3 minutos para sorteios 



'AMATEUR'), e então passe para a próxima guia, ciclando até a centésima guia e retornando à primeira.

3.  **Gestão de Falhas e Resiliência:**
    *   Detectar automaticamente falhas na participação do sorteio (ex: elemento não encontrado, página não carregada, erro de rede).
    *   Implementar um mecanismo de retry configurável (padrão 5 tentativas) para tentar novamente a participação na mesma guia em caso de falha.
    *   Se as tentativas falharem, reiniciar automaticamente *apenas* a guia específica do navegador que falhou e tentar novamente até o sucesso, respeitando a ordem de execução.

4.  **Configuração e Parametrização (via Interface do Usuário):**
    *   **Quantidade de Guias:** Campo configurável para definir o número de guias do Chrome a serem gerenciadas.
    *   **Velocidade de Execução:** Campo configurável para ajustar a velocidade das ações (tempo de espera entre as interações do bot com a página, além do tempo padrão de 3 minutos para sorteios 'AMATEUR').
    *   **Número de Tentativas de Retry:** Campo configurável para definir o número de vezes que o bot tentará novamente em caso de falha.
    *   **Botões de Controle:**
        *   `Reiniciar Guias`: Reinicia todas as guias do Chrome gerenciadas pelo bot.
        *   `Parar Todos os Bots`: Interrompe todas as operações do bot.
        *   `Iniciar Todos os Bots`: Inicia/retoma as operações do bot.
        *   `Limpar Cache`: Limpa o cache e dados de navegação das guias do Chrome, *sem* excluir informações de login de sites.
        *   `Salvar Configurações`: Persiste as configurações definidas pelo usuário.
        *   `Atualizar`: Verifica e informa sobre novas atualizações do aplicativo.

5.  **Monitoramento de Performance do Computador (via Interface do Usuário):**
    *   Exibir em tempo real dados de uso de RAM, CPU e HD.
    *   Exibir o consumo total de internet em GB.

6.  **Integração com Discord Webhook:**
    *   Enviar notificações automáticas para um webhook do Discord para:
        *   Início e fim de sessão do bot.
        *   Erros e falhas detalhadas (com informações da guia e motivo da falha).
        *   Relatórios de resultados (número de participações bem-sucedidas, falhas, etc.).
        *   Lucros obtidos (se a extração for viável do site Keydrop).

7.  **Interface de Usuário (UI) - Alto Padrão:**
    *   Design moderno, intuitivo e responsivo, adequado para uma multinacional.
    *   Três guias principais:
        *   **Configurações:** Contém todos os campos parametrizáveis e botões de controle.
        *   **Estatísticas:** Exibe os dados de performance do computador.
        *   **Relatório:** Apresenta os logs de execução, resultados e lucros.
    *   Preparado para receber novos botões e funcionalidades futuras de forma modular.

8.  **Performance e Otimização:**
    *   Desenvolvido para rodar em máquinas com baixo desempenho, com foco em gestão eficiente de memória e CPU.
    *   Execução assíncrona de todas as operações de automação para evitar travamentos e otimizar o uso de recursos.
    *   Mecanismos robustos de gestão de memória e CPU para lidar com múltiplas instâncias do Chrome.

9.  **Aplicativo Executável:**
    *   Gerar um único arquivo executável para fácil distribuição e instalação em sistemas Windows, Linux e macOS.

## Requisitos Não Funcionais Detalhados

*   **Performance:** O aplicativo deve ser altamente otimizado para baixo consumo de RAM e CPU, permitindo a execução fluida mesmo com 100 guias do Chrome abertas e em máquinas de baixo desempenho. A responsividade da interface não deve ser comprometida durante as operações do bot.
*   **Confiabilidade:** O bot deve ser robusto e resiliente a falhas, com mecanismos de retry e recuperação automática de guias.
*   **Usabilidade:** A interface do usuário deve ser extremamente intuitiva e fácil de usar, mesmo para usuários não técnicos, com feedback claro sobre o status e as operações do bot.
*   **Manutenibilidade:** O código deve ser bem estruturado, modular, com documentação interna clara e fácil de manter e estender para futuras funcionalidades.
*   **Segurança:** Garantir a segurança dos dados de login e outras informações sensíveis, evitando o armazenamento em texto claro e utilizando práticas de segurança recomendadas.
*   **Escalabilidade:** A arquitetura deve permitir a adição de novas funcionalidades e a expansão do número de guias gerenciadas no futuro sem a necessidade de grandes refatorações.
*   **Responsividade:** A interface deve se adaptar perfeitamente a diferentes tamanhos de tela e resoluções, garantindo uma experiência de usuário consistente.

## Tecnologias Recomendadas

Com base na análise de requisitos e seleção de tecnologias, as seguintes ferramentas e frameworks são recomendados para o desenvolvimento:

*   **Frontend (Interface do Usuário):**
    *   **Tauri:** Para a criação do aplicativo desktop multiplataforma, aproveitando sua leveza e performance.
    *   **Framework UI (dentro do Tauri):** React, Vue.js ou Svelte para construir a interface moderna e responsiva.

*   **Backend (Lógica de Negócio e Automação):**
    *   **Python:** Linguagem principal para a lógica do bot.
    *   **FastAPI:** Para construir a API de comunicação entre o frontend e o backend, e gerenciar a lógica assíncrona.
    *   **Playwright (com `playwright-python`):** Para automação de navegador, devido à sua performance, capacidade assíncrona e eficiência no gerenciamento de múltiplas guias.
    *   **psutil:** Para monitoramento de recursos do sistema (RAM, CPU, HD, rede).
    *   **`discord-webhook`:** Para integração com o Discord webhook.

*   **Empacotamento:**
    *   **PyInstaller:** Para gerar o aplicativo executável final.

## Estrutura do Projeto (Sugestão)

```
/bot_keydrop
├── frontend/ (código do Tauri + UI Framework)
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/ (código Python)
│   ├── main.py (FastAPI app)
│   ├── bot_logic/ (módulos de automação, agendamento, etc.)
│   ├── system_monitor/ (módulo de psutil)
│   ├── discord_integration/ (módulo de webhook)
│   ├── config/ (gerenciamento de configurações)
│   └── requirements.txt
├── resources/ (ícones, imagens, etc.)
├── dist/ (diretório para o executável gerado)
├── README.md
└── .gitignore
```

## Instruções para a IA

Com base nos requisitos detalhados e nas tecnologias recomendadas, a IA deve:

1.  **Estruturar o Projeto:** Criar a estrutura de diretórios conforme a sugestão acima.
2.  **Desenvolver o Frontend:** Implementar a interface do usuário com as três guias (`Configurações`, `Estatísticas`, `Relatório`), garantindo responsividade e um design moderno. Os campos de configuração devem ser funcionais e os botões devem enviar comandos para o backend.
3.  **Desenvolver o Backend:**
    *   Implementar a API FastAPI para comunicação com o frontend.
    *   Desenvolver o módulo de automação de navegador usando Playwright, incluindo a lógica de participação em sorteios, gerenciamento assíncrona de guias, e os mecanismos de retry e reinício de guias.
    *   Integrar o psutil para coletar e expor os dados de monitoramento de sistema via API/WebSockets para o frontend.
    *   Implementar a integração com Discord webhook para todas as notificações especificadas.
    *   Desenvolver o módulo de persistência para salvar e carregar configurações.
4.  **Conectar Frontend e Backend:** Estabelecer a comunicação entre as duas camadas, preferencialmente usando WebSockets para dados em tempo real (estatísticas, logs) e REST para comandos e configurações.
5.  **Empacotar o Aplicativo:** Configurar o PyInstaller para criar um executável multiplataforma do bot.
6.  **Testes:** Realizar testes unitários e de integração para garantir a funcionalidade, performance e resiliência do bot.
7.  **Documentação:** Gerar documentação técnica do código e um guia de uso para o usuário final.

Este prompt serve como um guia abrangente para o desenvolvimento do bot, cobrindo todos os aspectos funcionais, não funcionais e tecnológicos. A IA deve usar sua capacidade de raciocínio e implementação para transformar esses requisitos em um produto de software de alta qualidade.





## 3. Prompt Detalhado para Desenvolvimento de Bot de Interação com Chrome

### 3.1. Objetivo Geral

Desenvolver um bot de alto padrão para interação com guias do Google Chrome, com foco em performance, responsividade, baixo consumo de recursos e integração com Discord. O bot deve ser um aplicativo executável com uma interface de usuário moderna e intuitiva, capaz de automatizar a participação em sorteios online (especificamente no Keydrop) e fornecer monitoramento de performance do sistema.

### 3.2. Requisitos Funcionais Detalhados

1.  **Interação com Guias do Chrome:**
    *   Abrir, fechar e gerenciar múltiplas guias do Google Chrome de forma programática e assíncrona.
    *   Navegar para URLs específicas em cada guia.
    *   Realizar cliques em elementos da página (botões, links) e preencher campos de formulário.
    *   Extrair informações de elementos da página.
    *   Capacidade de encerrar até 100 guias do Chrome sem travar o aplicativo, com boa gestão de memória e CPU.

2.  **Automação de Sorteios (Keydrop):**
    *   Automatizar a participação em sorteios no site Keydrop, identificando e clicando nos botões de participação.
    *   Implementar um sistema de agendamento assíncrono para que o bot abra uma guia, participe do sorteio, aguarde um tempo padrão (3 minutos para sorteios 'AMATEUR'), e então passe para a próxima guia, ciclando até a centésima guia e retornando à primeira.

3.  **Gestão de Falhas e Resiliência:**
    *   Detectar automaticamente falhas na participação do sorteio (ex: elemento não encontrado, página não carregada, erro de rede).
    *   Implementar um mecanismo de retry configurável (padrão 5 tentativas) para tentar novamente a participação na mesma guia em caso de falha.
    *   Se as tentativas falharem, reiniciar automaticamente *apenas* a guia específica do navegador que falhou e tentar novamente até o sucesso, respeitando a ordem de execução.

4.  **Configuração e Parametrização (via Interface do Usuário):**
    *   **Quantidade de Guias:** Campo configurável para definir o número de guias do Chrome a serem gerenciadas.
    *   **Velocidade de Execução:** Campo configurável para ajustar a velocidade das ações (tempo de espera entre as interações do bot com a página, além do tempo padrão de 3 minutos para sorteios 'AMATEUR').
    *   **Número de Tentativas de Retry:** Campo configurável para definir o número de vezes que o bot tentará novamente em caso de falha.
    *   **Botões de Controle:**
        *   `Reiniciar Guias`: Reinicia todas as guias do Chrome gerenciadas pelo bot.
        *   `Parar Todos os Bots`: Interrompe todas as operações do bot.
        *   `Iniciar Todos os Bots`: Inicia/retoma as operações do bot.
        *   `Limpar Cache`: Limpa o cache e dados de navegação das guias do Chrome, *sem* excluir informações de login de sites.
        *   `Salvar Configurações`: Persiste as configurações definidas pelo usuário.
        *   `Atualizar`: Verifica e informa sobre novas atualizações do aplicativo.

5.  **Monitoramento de Performance do Computador (via Interface do Usuário):**
    *   Exibir em tempo real dados de uso de RAM, CPU e HD.
    *   Exibir o consumo total de internet em GB.

6.  **Integração com Discord Webhook:**
    *   Enviar notificações automáticas para um webhook do Discord para:
        *   Início e fim de sessão do bot.
        *   Erros e falhas detalhadas (com informações da guia e motivo da falha).
        *   Relatórios de resultados (número de participações bem-sucedidas, falhas, etc.).
        *   Lucros obtidos (se a extração for viável do site Keydrop).

7.  **Interface de Usuário (UI) - Alto Padrão:**
    *   Design moderno, intuitivo e responsivo, adequado para uma multinacional.
    *   Três guias principais:
        *   **Configurações:** Contém todos os campos parametrizáveis e botões de controle.
        *   **Estatísticas:** Exibe os dados de performance do computador.
        *   **Relatório:** Apresenta os logs de execução, resultados e lucros.
    *   Preparado para receber novos botões e funcionalidades futuras de forma modular.

8.  **Performance e Otimização:**
    *   Desenvolvido para rodar em máquinas com baixo desempenho, com foco em gestão eficiente de memória e CPU.
    *   Execução assíncrona de todas as operações de automação para evitar travamentos e otimizar o uso de recursos.
    *   Mecanismos robustos de gestão de memória e CPU para lidar com múltiplas instâncias do Chrome.

9.  **Aplicativo Executável:**
    *   Gerar um único arquivo executável para fácil distribuição e instalação em sistemas Windows, Linux e macOS.

### 3.3. Requisitos Não Funcionais Detalhados

*   **Performance:** O aplicativo deve ser altamente otimizado para baixo consumo de RAM e CPU, permitindo a execução fluida mesmo com 100 guias do Chrome abertas e em máquinas de baixo desempenho. A responsividade da interface não deve ser comprometida durante as operações do bot.
*   **Confiabilidade:** O bot deve ser robusto e resiliente a falhas, com mecanismos de retry e recuperação automática de guias.
*   **Usabilidade:** A interface do usuário deve ser extremamente intuitiva e fácil de usar, mesmo para usuários não técnicos, com feedback claro sobre o status e as operações do bot.
*   **Manutenibilidade:** O código deve ser bem estruturado, modular, com documentação interna clara e fácil de manter e estender para futuras funcionalidades.
*   **Segurança:** Garantir a segurança dos dados de login e outras informações sensíveis, evitando o armazenamento em texto claro e utilizando práticas de segurança recomendadas.
*   **Escalabilidade:** A arquitetura deve permitir a adição de novas funcionalidades e a expansão do número de guias gerenciadas no futuro sem a necessidade de grandes refatorações.
*   **Responsividade:** A interface deve se adaptar perfeitamente a diferentes tamanhos de tela e resoluções, garantindo uma experiência de usuário consistente.

### 3.4. Tecnologias Recomendadas

Com base na análise de requisitos e seleção de tecnologias, as seguintes ferramentas e frameworks são recomendados para o desenvolvimento:

*   **Frontend (Interface do Usuário):**
    *   **Tauri:** Para a criação do aplicativo desktop multiplataforma, aproveitando sua leveza e performance.
    *   **Framework UI (dentro do Tauri):** React, Vue.js ou Svelte para construir a interface moderna e responsiva.

*   **Backend (Lógica de Negócio e Automação):**
    *   **Python:** Linguagem principal para a lógica do bot.
    *   **FastAPI:** Para construir a API de comunicação entre o frontend e o backend, e gerenciar a lógica assíncrona.
    *   **Playwright (com `playwright-python`):** Para automação de navegador, devido à sua performance, capacidade assíncrona e eficiência no gerenciamento de múltiplas guias.
    *   **psutil:** Para monitoramento de recursos do sistema (RAM, CPU, HD, rede).
    *   **`discord-webhook`:** Para integração com o Discord webhook.

*   **Empacotamento:**
    *   **PyInstaller:** Para gerar o aplicativo executável final.

### 3.5. Estrutura do Projeto (Sugestão)

```
/bot_keydrop
├── frontend/ (código do Tauri + UI Framework)
│   ├── src/
│   ├── public/
│   └── package.json
├── backend/ (código Python)
│   ├── main.py (FastAPI app)
│   ├── bot_logic/ (módulos de automação, agendamento, etc.)
│   ├── system_monitor/ (módulo de psutil)
│   ├── discord_integration/ (módulo de webhook)
│   ├── config/ (gerenciamento de configurações)
│   └── requirements.txt
├── resources/ (ícones, imagens, etc.)
├── dist/ (diretório para o executável gerado)
├── README.md
└── .gitignore
```

### 3.6. Instruções para a IA

Com base nos requisitos detalhados e nas tecnologias recomendadas, a IA deve:

1.  **Estruturar o Projeto:** Criar a estrutura de diretórios conforme a sugestão acima.
2.  **Desenvolver o Frontend:** Implementar a interface do usuário com as três guias (`Configurações`, `Estatísticas`, `Relatório`), garantindo responsividade e um design moderno. Os campos de configuração devem ser funcionais e os botões devem enviar comandos para o backend.
3.  **Desenvolver o Backend:**
    *   Implementar a API FastAPI para comunicação com o frontend.
    *   Desenvolver o módulo de automação de navegador usando Playwright, incluindo a lógica de participação em sorteios, gerenciamento assíncrona de guias, e os mecanismos de retry e reinício de guias.
    *   Integrar o psutil para coletar e expor os dados de monitoramento de sistema via API/WebSockets para o frontend.
    *   Implementar a integração com Discord webhook para todas as notificações especificadas.
    *   Desenvolver o módulo de persistência para salvar e carregar configurações.
4.  **Conectar Frontend e Backend:** Estabelecer a comunicação entre as duas camadas, preferencialmente usando WebSockets para dados em tempo real (estatísticas, logs) e REST para comandos e configurações.
5.  **Empacotar o Aplicativo:** Configurar o PyInstaller para criar um executável multiplataforma do bot.
6.  **Testes:** Realizar testes unitários e de integração para garantir a funcionalidade, performance e resiliência do bot.
7.  **Documentação:** Gerar documentação técnica do código e um guia de uso para o usuário final.

Este prompt serve como um guia abrangente para o desenvolvimento do bot, cobrindo todos os aspectos funcionais, não funcionais e tecnológicos. A IA deve usar sua capacidade de raciocínio e implementação para transformar esses requisitos em um produto de software de alta qualidade.





## 4. Novos Requisitos Adicionais

### 4.1. Requisitos Funcionais Adicionais

*   **Modo Headless (Opcional):**
    *   O bot deve permitir a execução do navegador em modo headless (sem interface gráfica) como uma opção configurável na interface.

*   **Login Opcional (Keydrop e Steam):**
    *   Um checkbox opcional na interface que, quando marcado, instrui o bot a abrir duas abas específicas para login:
        *   `https://key-drop.com/pt/`
        *   `https://steamcommunity.com/login/home/?goto=`
    *   O bot deve aguardar o login manual do usuário nessas abas antes de prosseguir com as operações de sorteio.

*   **Modo Mini de Janelas (Opcional):**
    *   Um checkbox opcional na interface que, quando marcado, instrui o bot a abrir as janelas do navegador em um tamanho reduzido (200x300 pixels).

*   **Stop de Emergência:**
    *   Um botão de stop de emergência na interface que, ao ser acionado, deve fechar *todas* as guias do navegador abertas pelo bot de forma rápida e sem travamentos. Se necessário, deve ser capaz de encerrar os processos do navegador diretamente para garantir a interrupção imediata.

*   **Créditos do Desenvolvedor:**
    *   A interface deve exibir os créditos do desenvolvedor: "William Medrado (wmedrado) github".
    *   Deve informar a versão atual do aplicativo.

*   **Escalabilidade:**
    *   A arquitetura deve ser projetada para permitir escalabilidade futura, facilitando a adição de novas funcionalidades e o gerenciamento de um número ainda maior de guias, se necessário.

*   **Exibição Detalhada de Instâncias de Guias:**
    *   A interface deve exibir detalhadamente cada instância de guia de navegador aberta, possivelmente com seu status (participando, aguardando, falha, etc.) e informações relevantes.

*   **Projeto Exemplo:**
    *   O bot deve ser capaz de visualizar um arquivo de projeto exemplo fornecido pelo usuário para obter informações e referências, se necessário. (Este arquivo será fornecido posteriormente).

### 4.2. Detalhes da Interface (UI/UX)

*   **Qualidade Visual:** A interface deve ser de alta qualidade visual, moderna e profissional, adequada para uma multinacional.
*   **Responsividade:** Garantir que a interface se adapte perfeitamente a diferentes tamanhos de tela e resoluções.
*   **Detalhes de Estilo (Sugestões para a IA):**
    *   **Tamanho de Fonte:** Utilizar fontes claras e legíveis, com tamanhos variando entre 14px (texto padrão) e 24px (títulos de seção).
    *   **Cores:** Paleta de cores moderna e sóbria, com bom contraste. Sugestão: Tons de azul escuro, cinza e branco para o fundo e texto, com um toque de cor (ex: verde ou laranja) para elementos interativos e indicadores de status.
    *   **Tamanho de Checkbox:** Checkboxes com tamanho padrão (ex: 16x16px ou 20x20px) para fácil interação.
    *   **Layout:** Layout limpo e organizado, com espaçamento adequado entre os elementos para evitar poluição visual.
    *   **Animações:** Animações sutis para transições e feedback visual, sem comprometer a performance.

### 4.3. Requisitos de Desenvolvimento Adicionais

*   **Script de Desenvolvimento Passo a Passo:** Gerar um arquivo de texto com um script detalhado, dividido por etapas, que a IA deverá seguir para construir a aplicação. Ao concluir cada etapa com sucesso, a IA deverá marcar a etapa como concluída no script.





### 4.4. Localização do Projeto Exemplo

O arquivo de projeto exemplo estará localizado na pasta `exemplo/` dentro do diretório raiz do projeto (`/bot_keydrop/exemplo/`). A IA deve consultar este diretório para obter informações e referências, se necessário.


