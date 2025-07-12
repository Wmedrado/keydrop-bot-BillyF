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
