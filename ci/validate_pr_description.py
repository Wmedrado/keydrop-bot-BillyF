import os
import sys

REQUIRED_SECTIONS = [
    "### 🧠 Objetivo da alteração",
    "### 📍 Arquivos principais alterados",
    "### 🔁 Impacto em outros módulos",
    "### 🧪 Testes existentes cobrem essa lógica?",
    "### 🔐 Algum risco de segurança?",
    "### ✅ Justificativa no history_of_decisions.md?",
]


def main() -> int:
    body = os.environ.get("PR_BODY", "")
    text = body.lower()
    missing = [s for s in REQUIRED_SECTIONS if s.lower() not in text]
    if missing:
        print("PR description missing required sections:")
        for sec in missing:
            print(f"- {sec}")
        return 1
    print("PR description validated")
    return 0


if __name__ == "__main__":
    sys.exit(main())
