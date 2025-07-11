
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




## 5. Novos Requisitos Adicionais

### 5.1. Requisitos Funcionais Adicionais

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
    *   Um botão de 


stop de emergência na interface que, ao ser acionado, deve fechar *todas* as guias do navegador abertas pelo bot de forma rápida e sem travamentos. Se necessário, deve ser capaz de encerrar os processos do navegador diretamente para garantir a interrupção imediata.

*   **Créditos do Desenvolvedor:**
    *   A interface deve exibir os créditos do desenvolvedor: "William Medrado (wmedrado) github".
    *   Deve informar a versão atual do aplicativo.

*   **Escalabilidade:**
    *   A arquitetura deve ser projetada para permitir escalabilidade futura, facilitando a adição de novas funcionalidades e o gerenciamento de um número ainda maior de guias, se necessário.

*   **Exibição Detalhada de Instâncias de Guias:**
    *   A interface deve exibir detalhadamente cada instância de guia de navegador aberta, possivelmente com seu status (participando, aguardando, falha, etc.) e informações relevantes.

*   **Projeto Exemplo:**
    *   O bot deve ser capaz de visualizar um arquivo de projeto exemplo fornecido pelo usuário para obter informações e referências, se necessário. (Este arquivo será fornecido posteriormente).

### 5.2. Detalhes da Interface (UI/UX)

*   **Qualidade Visual:** A interface deve ser de alta qualidade visual, moderna e profissional, adequada para uma multinacional.
*   **Responsividade:** Garantir que a interface se adapte perfeitamente a diferentes tamanhos de tela e resoluções.
*   **Detalhes de Estilo (Sugestões para a IA):**
    *   **Tamanho de Fonte:** Utilizar fontes claras e legíveis, com tamanhos variando entre 14px (texto padrão) e 24px (títulos de seção).
    *   **Cores:** Paleta de cores moderna e sóbria, com bom contraste. Sugestão: Tons de azul escuro, cinza e branco para o fundo e texto, com um toque de cor (ex: verde ou laranja) para elementos interativos e indicadores de status.
    *   **Tamanho de Checkbox:** Checkboxes com tamanho padrão (ex: 16x16px ou 20x20px) para fácil interação.
    *   **Layout:** Layout limpo e organizado, com espaçamento adequado entre os elementos para evitar poluição visual.
    *   **Animações:** Animações sutis para transições e feedback visual, sem comprometer a performance.

### 5.3. Requisitos de Desenvolvimento Adicionais

*   **Script de Desenvolvimento Passo a Passo:** Gerar um arquivo de texto com um script detalhado, dividido por etapas, que a IA deverá seguir para construir a aplicação. Ao concluir cada etapa com sucesso, a IA deverá marcar a etapa como concluída no script.



