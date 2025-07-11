# Prompt Detalhado para Desenvolvimento de Bot de Interação com Chrome (v2)

## Objetivo Geral

Desenvolver um bot de alto padrão para interação com guias do Google Chrome, com foco em performance, responsividade, baixo consumo de recursos e integração com Discord. O bot deve ser um aplicativo executável com uma interface de usuário moderna e intuitiva, capaz de automatizar a participação em sorteios online (especificamente no Keydrop) e fornecer monitoramento de performance do sistema, incorporando funcionalidades avançadas de gerenciamento de navegador e resiliência.

## 1. Requisitos Funcionais Detalhados

1.  **Interação com Guias do Chrome:**
    *   Abrir, fechar e gerenciar múltiplas guias do Google Chrome de forma programática e assíncrona.
    *   **Cada guia aberta deve utilizar um perfil de usuário do Chrome diferente.** Isso é crucial para isolar sessões, gerenciar logins e mitigar problemas relacionados a IP ou detecção de bot.
    *   Navegar para URLs específicas em cada guia.
    *   Realizar cliques em elementos da página (botões, links) e preencher campos de formulário.
    *   Extrair informações de elementos da página.
    *   Capacidade de encerrar até 100 guias do Chrome sem travar o aplicativo, com boa gestão de memória e CPU.
    *   **Modo Headless (Opcional):** Implementar uma opção configurável na interface para executar o navegador em modo headless (sem interface gráfica).
    *   **Modo Mini de Janelas (Opcional):** Adicionar um checkbox opcional na interface. Quando marcado, o bot deve abrir as janelas do navegador em um tamanho reduzido (200x300 pixels).
    *   **Otimização de Imagens e Recursos Web (Opcional):** Considerar a opção de desabilitar o carregamento de imagens ou carregar versões de baixa resolução nas guias do Chrome para otimização de performance em máquinas de baixo desempenho. Isso deve ser configurável via argumentos do Playwright.
    *   **Persistência de Dados de Sessão do Navegador:** O bot deve ser capaz de persistir os dados de sessão do navegador (cookies, localStorage) de forma segura para cada perfil, permitindo que o usuário permaneça logado em sites como Keydrop e Steam entre as execuções, sem precisar fazer login manualmente a cada reinício do bot.

2.  **Automação de Sorteios (Keydrop):**
    *   Automatizar a participação em sorteios no site Keydrop, identificando e clicando nos botões de participação.
    *   Implementar um sistema de agendamento assíncrono para que o bot abra uma guia, participe do sorteio, aguarde um tempo padrão (3 minutos para sorteios 'AMATEUR'), e então passe para a próxima guia, ciclando até a centésima guia e retornando à primeira.

3.  **Gestão de Falhas e Resiliência:**
    *   Detectar automaticamente falhas na participação do sorteio (ex: elemento não encontrado, página não carregada, erro de rede).
    *   Implementar um mecanismo de retry configurável (padrão 5 tentativas) para tentar novamente a participação na mesma guia em caso de falha.
    *   Se as tentativas falharem, reiniciar automaticamente *apenas* a guia específica do navegador que falhou e tentar novamente até o sucesso, respeitando a ordem de execução.
    *   **Captcha/Anti-bot Detection Handling:** Considerar a inclusão de um módulo para lidar com sistemas anti-bot (CAPTCHAs, detecção de comportamento robótico) que possam ser implementados pelo site. Isso pode envolver detecção ou integração com serviços de resolução de CAPTCHA (se permitido e viável).

4.  **Configuração e Parametrização (via Interface do Usuário):**
    *   **Quantidade de Guias:** Campo configurável para definir o número de guias do Chrome a serem gerenciadas.
    *   **Velocidade de Execução:** Campo configurável para ajustar a velocidade das ações (tempo de espera entre as interações do bot com a página, além do tempo padrão de 3 minutos para sorteios 'AMATEUR').
    *   **Número de Tentativas de Retry:** Campo configurável para definir o número de vezes que o bot tentará novamente em caso de falha.
    *   **Login Opcional (Keydrop e Steam):** Adicionar um checkbox opcional na interface. Quando marcado, o bot deve abrir duas abas específicas para login (`https://key-drop.com/pt/` e `https://steamcommunity.com/login/home/?goto=`). O bot deve pausar as operações de sorteio e aguardar o login manual do usuário nessas abas antes de prosseguir.
    *   **Botões de Controle:**
        *   `Reiniciar Guias`: Reinicia todas as guias do Chrome gerenciadas pelo bot.
        *   `Parar Todos os Bots`: Interrompe todas as operações do bot.
        *   `Iniciar Todos os Bots`: Inicia/retoma as operações do bot.
        *   `Limpar Cache`: Limpa o cache e dados de navegação das guias do Chrome, *sem* excluir informações de login de sites (apenas para o perfil ativo, se aplicável).
        *   `Salvar Configurações`: Persiste as configurações definidas pelo usuário.
        *   `Atualizar`: Verifica e informa sobre novas atualizações do aplicativo.
    *   **Validação de Entradas do Usuário:** Implementar validação robusta para todas as entradas do usuário na interface (ex: quantidade de guias deve ser um número inteiro positivo, URL do webhook válida).

5.  **Monitoramento de Performance do Computador (via Interface do Usuário):**
    *   Exibir em tempo real dados de uso de RAM, CPU e HD.
    *   Exibir o consumo total de internet em GB.
    *   **Exibição Detalhada de Instâncias de Guias:** A interface deve exibir detalhadamente cada instância de guia de navegador aberta, possivelmente com seu status (participando, aguardando, falha, etc.) e informações relevantes (ex: URL atual, perfil em uso).

6.  **Integração com Discord Webhook:**
    *   Enviar notificações automáticas para um webhook do Discord para:
        *   Início e fim de sessão do bot.
        *   Erros e falhas detalhadas (com informações da guia, perfil e motivo da falha).
        *   Relatórios de resultados (número de participações bem-sucedidas, falhas, etc.).
        *   Lucros obtidos (se a extração for viável do site Keydrop).

7.  **Interface de Usuário (UI) - Alto Padrão:**
    *   Design moderno, intuitivo e responsivo, adequado para uma multinacional.
    *   Três guias principais:
        *   **Configurações:** Contém todos os campos parametrizáveis e botões de controle.
        *   **Estatísticas:** Exibe os dados de performance do computador e o status detalhado das instâncias de guias.
        *   **Relatório:** Apresenta os logs de execução, resultados e lucros.
    *   Preparado para receber novos botões e funcionalidades futuras de forma modular.
    *   **Detalhes de Estilo (Sugestões para a IA):**
        *   **Tamanho de Fonte:** Utilizar fontes claras e legíveis, com tamanhos variando entre 14px (texto padrão) e 24px (títulos de seção).
        *   **Cores:** Paleta de cores moderna e sóbria, com bom contraste. Sugestão: Tons de azul escuro, cinza e branco para o fundo e texto, com um toque de cor (ex: verde ou laranja) para elementos interativos e indicadores de status.
        *   **Tamanho de Checkbox:** Checkboxes com tamanho padrão (ex: 16x16px ou 20x20px) para fácil interação.
        *   **Layout:** Layout limpo e organizado, com espaçamento adequado entre os elementos para evitar poluição visual.
        *   **Animações:** Animações sutis para transições e feedback visual, sem comprometer a performance.
    *   **Notificações Visuais e Sonoras:** Para eventos críticos (sucesso em sorteio, falha grave, stop de emergência acionado), incluir alertas visuais (pop-ups, mudança de cor de status) e/ou sonoros na própria interface do bot.

8.  **Performance e Otimização:**
    *   Desenvolvido para rodar em máquinas com baixo desempenho, com foco em gestão eficiente de memória e CPU.
    *   Execução assíncrona de todas as operações de automação para evitar travamentos e otimizar o uso de recursos.
    *   Mecanismos robustos de gestão de memória e CPU para lidar com múltiplas instâncias do Chrome.

9.  **Aplicativo Executável:**
    *   Gerar um único arquivo executável para fácil distribuição e instalação em sistemas Windows, Linux e macOS.
    *   **Atualização Automática do Aplicativo:** Implementar um mecanismo de atualização automática para o próprio executável do bot. Isso permitirá que o bot se atualize para novas versões sem a necessidade de o usuário baixar e instalar manualmente a cada lançamento.

10. **Stop de Emergência:**
    *   Implementar um botão de stop de emergência na interface. Ao ser acionado, o bot deve fechar *todas* as guias do navegador abertas por ele de forma rápida e sem travamentos. Se necessário, o bot deve ser capaz de encerrar os processos do navegador diretamente para garantir a interrupção imediata e limpa.

11. **Créditos do Desenvolvedor:**
    *   A interface deve exibir os créditos do desenvolvedor: "William Medrado (wmedrado) github".
    *   Deve informar a versão atual do aplicativo.

12. **Escalabilidade:**
    *   A arquitetura deve ser projetada para permitir escalabilidade futura, facilitando a adição de novas funcionalidades e o gerenciamento de um número ainda maior de guias, se necessário.

13. **Projeto Exemplo:**
    *   A IA deve ser instruída a visualizar um arquivo de projeto exemplo (localizado em `exemplo/` dentro do diretório raiz do projeto) para obter informações e referências, se necessário, durante o desenvolvimento.

## 2. Requisitos Não Funcionais Detalhados

*   **Performance:** O aplicativo deve ser altamente otimizado para baixo consumo de RAM e CPU, permitindo a execução fluida mesmo com 100 guias do Chrome abertas e em máquinas de baixo desempenho. A responsividade da interface não deve ser comprometida durante as operações do bot.
*   **Confiabilidade:** O bot deve ser robusto e resiliente a falhas, com mecanismos de retry e recuperação automática de guias.
*   **Usabilidade:** A interface do usuário deve ser extremamente intuitiva e fácil de usar, mesmo para usuários não técnicos, com feedback claro sobre o status e as operações do bot.
*   **Manutenibilidade:** O código deve ser bem estruturado, modular, com documentação interna clara e fácil de manter e estender para futuras funcionalidades.
*   **Segurança:** Garantir a segurança dos dados de login e outras informações sensíveis, evitando o armazenamento em texto claro e utilizando práticas de segurança recomendadas.
*   **Escalabilidade:** A arquitetura deve permitir a adição de novas funcionalidades e a expansão do número de guias gerenciadas no futuro sem a necessidade de grandes refatorações.
*   **Responsividade:** A interface deve se adaptar perfeitamente a diferentes tamanhos de tela e resoluções, garantindo uma experiência de usuário consistente.

## 3. Tecnologias Recomendadas

Com base na análise de requisitos e seleção de tecnologias, as seguintes ferramentas e frameworks são recomendados para o desenvolvimento:

*   **Frontend (Interface do Usuário):**
    *   **Tauri:** Para a criação do aplicativo desktop multiplataforma, aproveitando sua leveza e performance.
    *   **Framework UI (dentro do Tauri):** React, Vue.js ou Svelte para construir a interface moderna e responsiva.

*   **Backend (Lógica de Negócio e Automação):**
    *   **Python:** Linguagem principal para a lógica do bot.
    *   **FastAPI:** Para construir a API de comunicação entre o frontend e o backend, e gerenciar a lógica assíncrona.
    *   **Playwright (com `playwright-python`):** Para automação de navegador, devido à sua performance, capacidade assíncrona e eficiência no gerenciamento de múltiplas guias. **Crucial para o gerenciamento de perfis de usuário distintos por guia.**
    *   **psutil:** Para monitoramento de recursos do sistema (RAM, CPU, HD, rede).
    *   **`discord-webhook`:** Para integração com o Discord webhook.

*   **Empacotamento:**
    *   **PyInstaller:** Para gerar o aplicativo executável final.

## 4. Estrutura do Projeto (Sugestão)

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
│   ├── profiles/ (diretório para perfis de usuário do Chrome)
│   └── requirements.txt
├── resources/ (ícones, imagens, etc.)
├── dist/ (diretório para o executável gerado)
├── exemplo/ (diretório para o projeto exemplo fornecido pelo usuário)
├── README.md
└── .gitignore
```

## 5. Instruções para a IA

Com base nos requisitos detalhados e nas tecnologias recomendadas, a IA deve:

1.  **Estruturar o Projeto:** Criar a estrutura de diretórios conforme a sugestão acima, incluindo o diretório `profiles/` para os perfis do Chrome e `exemplo/` para o projeto de referência.
2.  **Desenvolver o Frontend:** Implementar a interface do usuário com as três guias (`Configurações`, `Estatísticas`, `Relatório`), garantindo responsividade, um design moderno (seguindo as sugestões de estilo) e as novas funcionalidades (checkboxes para headless, mini mode, login opcional, botão de stop de emergência, exibição de créditos/versão, e exibição detalhada de instâncias de guias). Implementar validação de entradas do usuário e notificações visuais/sonoras.
3.  **Desenvolver o Backend:**
    *   Implementar a API FastAPI para comunicação com o frontend.
    *   Desenvolver o módulo de automação de navegador usando Playwright, **garantindo que cada nova guia utilize um perfil de usuário do Chrome distinto e persistente**. Incluir a lógica de participação em sorteios, gerenciamento assíncrono de guias, mecanismos de retry e reinício de guias, e a capacidade de otimizar o carregamento de recursos web. Implementar a persistência de dados de sessão para cada perfil.
    *   Integrar o psutil para coletar e expor os dados de monitoramento de sistema via API/WebSockets para o frontend.
    *   Implementar a integração com Discord webhook para todas as notificações especificadas.
    *   Desenvolver o módulo de persistência para salvar e carregar configurações.
    *   Implementar a lógica para o botão de stop de emergência, que deve fechar todas as guias e encerrar processos do navegador de forma robusta.
    *   Considerar a implementação de um módulo para lidar com detecção anti-bot/CAPTCHA, se aplicável.
4.  **Conectar Frontend e Backend:** Estabelecer a comunicação entre as duas camadas, preferencialmente usando WebSockets para dados em tempo real (estatísticas, logs) e REST para comandos e configurações.
5.  **Empacotar o Aplicativo:** Configurar o PyInstaller para criar um executável multiplataforma do bot. **Incluir um mecanismo de atualização automática para o próprio executável.**
6.  **Testes:** Realizar testes unitários e de integração para garantir a funcionalidade, performance e resiliência do bot.
7.  **Documentação:** Gerar documentação técnica do código e um guia de uso para o usuário final.

Este prompt serve como um guia abrangente para o desenvolvimento do bot, cobrindo todos os aspectos funcionais, não funcionais e tecnológicos. A IA deve usar sua capacidade de raciocínio e implementação para transformar esses requisitos em um produto de software de alta qualidade, prestando atenção especial à gestão de perfis de usuário do Chrome e à resiliência do sistema.

