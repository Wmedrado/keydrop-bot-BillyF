# Requisitos Funcionais - Sistema de Sorteios KeydropBot

Este documento detalha todos os requisitos funcionais extraídos do bot de referência (`keydrop_bot.py`) para garantir uma automação robusta, eficiente e segura na participação de sorteios Keydrop.

---

## 1. Controle de Participação
- Participação automática em sorteios "amateur" (intervalo mínimo de 3 minutos).
- Participação automática em sorteios "contender" (intervalo mínimo de 1 hora).
- Registro do horário da última participação para cada tipo de sorteio.
- Lógica de retry: múltiplas tentativas automáticas em caso de falha (parâmetro configurável).
- Controle de tentativas máximas para cada ação de participação.
- Execução assíncrona: cada bot opera em thread separada, permitindo múltiplas instâncias simultâneas.
- Gerenciamento de múltiplos bots com perfis isolados (cookies, sessões, cache).

## 2. Controle de Falhas e Erros
- Registro detalhado de erros por bot (contagem, tipo, mensagem).
- Atualização do status do bot em caso de erro ou falha.
- Lógica de robustez para encerrar processos do navegador (fechar guias, encerrar driver, matar processos Chrome).
- Retry automático em caso de falha na participação ou automação.

## 3. Estatísticas e Monitoramento
- Contador de participações (amateur e contender) por bot.
- Registro do saldo inicial, saldo atual e ganhos do bot.
- Registro do horário de início da sessão e tempo total de execução.
- Atualização do status do bot (última atividade, saldo, erros, etc).
- Monitoramento de uso de recursos (RAM, CPU, disco, rede).
- Exibição de estatísticas globais e individuais na interface.

## 4. Notificações e Alertas
- Envio de alerta via Discord se o bot ficar 30 minutos sem participar de sorteios.
- Registro do horário do último alerta enviado.
- Mensagem personalizada de alerta para cada bot.
- Integração opcional com webhook do Discord.

## 5. Otimização de Recursos
- Gerenciamento robusto dos processos do navegador (registro e encerramento de PIDs Chrome).
- Integração opcional com otimizador de memória/processos.
- Minimização do uso de RAM e CPU por bot.
- Opção de rodar bots em modo "headless" ou "mini window" para economizar recursos.

## 6. Segurança e Isolamento
- Cada bot utiliza um diretório de perfil exclusivo para garantir isolamento de sessão, cookies e cache.
- Encerramento seguro e ordenado dos processos do navegador ao finalizar automação.
- Proteção contra vazamento de sessão entre bots.

## 7. Configurações e Parâmetros
- Parâmetro configurável para número de bots/guias.
- Parâmetro configurável para intervalo de execução e tentativas de retry.
- Parâmetro para ativar/desativar modos de operação (headless, mini window, contender, login manual).
- Parâmetro para ativar/desativar integração Discord.

## 8. Interface e Usabilidade
- Exibição em tempo real do status, estatísticas e logs de cada bot.
- Botão para teste completo (login, sorteio, otimização de RAM).
- Botão para fechar apenas as guias/browsers dos bots.
- Logs detalhados de todas as ações e erros.

---

**Observação:** Estes requisitos foram extraídos do bot de referência e devem ser implementados integralmente no bot principal para garantir máxima robustez, performance e segurança na automação de sorteios Keydrop.
