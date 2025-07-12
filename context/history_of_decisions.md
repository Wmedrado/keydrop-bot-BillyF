## Sistema de Histórico de Decisões

Este arquivo registra as decisões técnicas tomadas durante o desenvolvimento automatizado do projeto.
Cada nova funcionalidade ou ajuste relevante deve adicionar um bloco seguindo o modelo abaixo.

```
## <Nome da funcionalidade ou ajuste>
- **Motivo:** <descrição do motivo>
- **Afeta/Substitui:** <lógica ou módulo afetado>
- **Justificativa técnica:** <detalhes>
- **Tipo:** <fallback | workaround | melhoria | outro>
```

---

## Sistema de Histórico de Decisões
- **Motivo:** Registrar as motivações de cada mudança implementada pela IA.
- **Afeta/Substitui:** adiciona `ci/check_history.py` e altera o workflow `ci.yml`.
- **Justificativa técnica:** Facilita auditoria e impede regressões não justificadas.
- **Tipo:** melhoria

## Staging sandbox pipeline
- **Motivo:** validar merges na branch principal sem impactar usuários finais.
- **Afeta/Substitui:** adiciona `ci/run_staging_pipeline.sh` e atualiza `ci.yml` com job de staging.
- **Justificativa técnica:** roda container isolado por 3 minutos em modo debug e checa logs para falhas críticas.
- **Tipo:** melhoria

## Resilience and CI automation enhancements
- **Motivo:** Garantir qualidade de código e maior resiliência do bot.
- **Afeta/Substitui:** adiciona utilidades de monitoramento em `bot_keydrop.utils` e novos scripts em `ci/`.
- **Justificativa técnica:** Implementação de scanner de TODOs, enforcer de `__str__`/`__repr__`, circuito de retry, monitor de tempo e rollback automático.
- **Tipo:** melhoria

## SonarCloud static analysis
- **Motivo:** Detectar código duplicado e más práticas automaticamente.
- **Afeta/Substitui:** adiciona `sonar-project.properties`, atualiza `ci.yml` e `README.md`.
- **Justificativa técnica:** Integração com SonarCloud fornece análise estática avançada para reduzir riscos futuros.
- **Tipo:** melhoria

## Validação opcional do template de PR
- **Motivo:** remover bloqueio de merge por documentação incompleta.
- **Afeta/Substitui:** remove `validate_pr.yml`, passo `Validate PR description` em `ci.yml` e checagem em `run_pipeline.sh`.
- **Justificativa técnica:** simplifica o fluxo de CI, mantendo a recomendação do template sem impedir integrações úteis.
- **Tipo:** melhoria


## SonarCloud quality gate enforcement
- **Motivo:** Gerar relatório automático de duplicações, código morto e alta complexidade a cada PR.
- **Afeta/Substitui:** adiciona `ci/sonar_report.py`, atualiza `ci.yml` e `README.md`.
- **Justificativa técnica:** Esperar o resultado do Quality Gate garante que falhas graves sejam detectadas antes do merge.

## Sistema de cache e limitador
- **Motivo:** otimizar operações repetitivas e controle de requisições.
- **Afeta/Substitui:** adiciona `smart_cache`, `history_recorder`, `rate_limiter`, `browser_fallback` e verificação de variáveis sensíveis no CI.
- **Justificativa técnica:** reduz custo computacional, registra histórico individual e previne vazamento de credenciais.
- **Tipo:** melhoria
