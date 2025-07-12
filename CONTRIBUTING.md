# Diretrizes para Contribuições Geradas por IA

Este projeto aceita códigos produzidos automaticamente por inteligências artificiais. Para garantir estabilidade e evitar falhas, siga os passos abaixo antes de enviar um Pull Request.

## 1. Padronização
- Utilize nomes de funções e variáveis descritivos.
- Estruture o código em funções ou classes curtas e coesas.
- Adicione docstrings explicativas em português ou inglês.
- Siga a formatação aplicada pelo `black` e as verificações do `flake8`.

## 2. Testes Obrigatórios
- Toda nova funcionalidade deve possuir testes em `tests/`.
- Execute `pytest` localmente e verifique se todos os testes passam.
- Caso algum teste falhe, relate o motivo no PR.

## 3. Pré-commit
- Instale as dependências de desenvolvimento:
  ```bash
  pip install pre-commit flake8 black
  ```
- Ative os hooks com:
  ```bash
  pre-commit install
  ```
  - A cada commit serão executadas apenas verificações de formatação e lint. Execute os testes manualmente com `pytest` quando necessário.

## 4. Processo de Pull Request
- Descreva brevemente o que foi implementado pela IA.
- Inclua o resultado dos testes executados localmente.
- Em caso de falha ou comportamento inesperado, explique no PR para que possamos avaliar.

Seguindo estas diretrizes, conseguimos manter a qualidade do código mesmo sendo gerado por IA.
