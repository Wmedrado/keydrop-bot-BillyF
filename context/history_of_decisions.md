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

## Ferramenta de análise estática com SonarCloud
- **Motivo:** Detectar duplicações, código morto e alta complexidade para reduzir riscos futuros.
- **Afeta/Substitui:** adiciona `sonar-project.properties` e etapas no workflow `ci.yml`.
- **Justificativa técnica:** Integração via GitHub Actions permite bloquear PRs com falhas graves e gerar relatórios automáticos.
- **Tipo:** melhoria
