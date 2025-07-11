# Script de Desenvolvimento do Bot de Interação com Chrome

Este script detalha as etapas que a IA deve seguir para desenvolver o bot de interação com o Google Chrome, conforme os requisitos e tecnologias definidos. Cada etapa deve ser marcada como concluída após sua bem-sucedida execução.

## Estrutura do Projeto

- [ ] **Etapa 1: Criar a estrutura de diretórios.**
  Crie a seguinte estrutura de pastas:
  ```
  /bot_keydrop
  ├── frontend/
  │   ├── src/
  │   ├── public/
  │   └── package.json
  ├── backend/
  │   ├── main.py
  │   ├── bot_logic/
  │   ├── system_monitor/
  │   ├── discord_integration/
  │   ├── config/
  │   └── requirements.txt
  ├── resources/
  ├── dist/
  ├── README.md
  └── .gitignore
  ```

## Desenvolvimento do Backend (Python)

- [ ] **Etapa 2: Configurar o ambiente Python e dependências.**
  Instale as bibliotecas Python necessárias no ambiente virtual do projeto `backend/requirements.txt`:
  ```
  fastapi
  uvicorn
  playwright
  psutil
  discord-webhook
  ```
  Certifique-se de instalar os drivers do Playwright:
  `playwright install`

- [ ] **Etapa 3: Implementar o módulo de configuração (`backend/config/`).**
  Crie um módulo para gerenciar as configurações do bot (quantidade de guias, velocidade, tentativas de retry, webhook do Discord, etc.). Deve ser capaz de salvar e carregar as configurações de um arquivo (ex: JSON ou YAML).

- [ ] **Etapa 4: Implementar o módulo de monitoramento de sistema (`backend/system_monitor/`).**
  Utilize `psutil` para coletar dados de uso de RAM, CPU, HD e consumo de internet. Crie funções que retornem esses dados de forma estruturada.

- [ ] **Etapa 5: Implementar o módulo de integração com Discord (`backend/discord_integration/`).**
  Utilize `discord-webhook` para enviar notificações para o Discord. Crie funções para enviar mensagens de início/fim de sessão, erros, relatórios e lucros.

- [ ] **Etapa 6: Implementar o módulo de lógica do bot (`backend/bot_logic/`).**
  Este é o coração do bot. Divida em submódulos:
  *   **`browser_manager.py`:** Responsável por iniciar, fechar e gerenciar instâncias do Chrome usando Playwright. Deve suportar modo headless e modo mini (200x300).
  *   **`automation_tasks.py`:** Contém a lógica para interagir com o Keydrop (navegar, clicar em botões de sorteio). Implemente os mecanismos de retry e reinício de guias em caso de falha.
  *   **`scheduler.py`:** Gerencia o agendamento assíncrono das tarefas em cada guia, controlando a velocidade de execução e o ciclo entre as guias.

- [ ] **Etapa 7: Desenvolver a API FastAPI (`backend/main.py`).**
  Crie os endpoints da API para:
  *   Receber e aplicar configurações do frontend.
  *   Iniciar, parar e reiniciar o bot.
  *   Limpar cache do navegador (sem perder logins).
  *   Expor os dados de monitoramento de sistema via WebSockets para atualizações em tempo real.
  *   Expor endpoints para relatórios e logs.

## Desenvolvimento do Frontend (Tauri + UI Framework)

- [ ] **Etapa 8: Configurar o ambiente Tauri e UI Framework.**
  Configure o projeto Tauri no diretório `frontend/`. Escolha e configure um framework UI (React, Vue.js ou Svelte) para construir a interface.

- [ ] **Etapa 9: Desenvolver a interface de Configurações.**
  Crie a guia de configurações com os seguintes elementos:
  *   Campos de entrada para quantidade de guias, velocidade de execução, número de tentativas de retry.
  *   Checkbox para modo headless.
  *   Checkbox para login opcional (Keydrop e Steam).
  *   Checkbox para modo mini de janelas.
  *   Campo para URL do Discord Webhook.
  *   Botões: `Reiniciar Guias`, `Parar Todos os Bots`, `Iniciar Todos os Bots`, `Limpar Cache`, `Salvar Configurações`, `Atualizar`.
  *   Implemente a comunicação com a API FastAPI para enviar e receber configurações.

- [ ] **Etapa 10: Desenvolver a interface de Estatísticas.**
  Crie a guia de estatísticas para exibir em tempo real:
  *   Uso de RAM, CPU, HD.
  *   Consumo total de internet em GB.
  *   Exibição detalhada de cada instância de guia de navegador aberta (status, informações relevantes).
  *   Utilize WebSockets para receber atualizações em tempo real do backend.

- [ ] **Etapa 11: Desenvolver a interface de Relatório.**
  Crie a guia de relatório para exibir:
  *   Logs de execução do bot.
  *   Resultados de sorteios (sucessos, falhas).
  *   Lucros obtidos (se aplicável).

- [ ] **Etapa 12: Implementar o Stop de Emergência.**
  Crie um botão de stop de emergência visível e acessível em todas as guias. Ao ser clicado, deve enviar um comando para o backend para fechar *todas* as guias do navegador e encerrar processos relacionados de forma robusta.

- [ ] **Etapa 13: Adicionar Créditos e Versão.**
  Inclua os créditos do desenvolvedor "William Medrado (wmedrado) github" e a versão atual do aplicativo em um local apropriado na interface (ex: rodapé ou aba 


Sobre).

## Empacotamento

- [ ] **Etapa 14: Configurar o PyInstaller.**
  Configure o PyInstaller para empacotar o aplicativo Python (backend) em um executável autônomo. Certifique-se de incluir todos os arquivos e dependências necessárias.

- [ ] **Etapa 15: Integrar o executável do backend com o Tauri.**
  Configure o Tauri para incluir o executável do backend e iniciar/gerenciar o processo do backend quando o aplicativo Tauri for iniciado.

## Testes e Documentação

- [ ] **Etapa 16: Realizar testes unitários e de integração.**
  Escreva e execute testes para garantir a funcionalidade de cada módulo e a integração entre frontend e backend.

- [ ] **Etapa 17: Gerar documentação técnica e guia de uso.**
  Crie uma documentação técnica detalhada do código e um guia de uso para o usuário final, explicando como configurar e operar o bot.

## Finalização

- [ ] **Etapa 18: Revisão final e otimização.**
  Revise todo o código e a aplicação para garantir que todos os requisitos foram atendidos, com foco em performance, gestão de recursos e qualidade visual. Realize otimizações adicionais se necessário.



