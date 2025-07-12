"""Heuristics to suggest actions based on common error messages."""

from __future__ import annotations


def analyze_error(message: str) -> str:
    message = message.lower()
    if "429" in message or "too many requests" in message:
        return "Possível bloqueio por excesso de acessos. Aguarde alguns minutos e reduza a frequência."
    if "ban" in message:
        return "Conta possivelmente banida. Verifique suas credenciais e evite novas tentativas."
    if "timeout" in message or "tempo esgotado" in message:
        return (
            "A operação excedeu o tempo limite. Tente novamente ou revise sua conexão."
        )
    if "no such element" in message:
        return (
            "Elemento não encontrado. A página pode ter mudado; atualize os seletores."
        )
    return "Erro desconhecido. Consulte os logs para mais detalhes."
