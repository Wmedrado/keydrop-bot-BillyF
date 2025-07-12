# Histórico de Decisões


Este arquivo registra as decisões técnicas tomadas durante o desenvolvimento automatizado do projeto.
Cada nova funcionalidade ou ajuste relevante deve adicionar um bloco seguindo o modelo abaixo.

```
## <Nome da funcionalidade ou ajuste>
- **Motivo:** <descrição do motivo>
- **Afeta/Substitui:** <lógica ou módulo afetado>
- **Justificativa técnica:** <detalhes>
- **Tipo:** <fallback | workaround | melhoria | outro>
```

## Sistema de Histórico de Decisões
- **Motivo:** Registrar as motivações de cada mudança implementada pela IA.
- **Afeta/Substitui:** adiciona `ci/check_history.py` e altera o workflow `ci.yml`.
- **Justificativa técnica:** Facilita auditoria e impede regressões não justificadas.
- **Tipo:** melhoria
Este arquivo documenta justificativas para alterações em arquivos críticos. Sempre descreva abaixo a razão de qualquer mudança nesses arquivos.

## Staging sandbox pipeline
- **Motivo:** validar merges na branch principal sem impactar usuários finais.
- **Afeta/Substitui:** adiciona `ci/run_staging_pipeline.sh` e atualiza `ci.yml` com job de staging.
- **Justificativa técnica:** roda container isolado por 3 minutos em modo debug e checa logs para falhas críticas.
- **Tipo:** melhoria

## Validação opcional do template de PR
- **Motivo:** remover bloqueio de merge por documentação incompleta.
- **Afeta/Substitui:** remove `validate_pr.yml`, passo `Validate PR description` em `ci.yml` e checagem em `run_pipeline.sh`.
- **Justificativa técnica:** simplifica o fluxo de CI, mantendo a recomendação do template sem impedir integrações úteis.
- **Tipo:** melhoria
