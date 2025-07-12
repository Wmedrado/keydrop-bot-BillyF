"""Ranking display component."""
from __future__ import annotations

import logging
import customtkinter as ctk
from tkhtmlview import HTMLLabel

from cloud.firebase_client import initialize_firebase, db

logger = logging.getLogger(__name__)


class RankingFrame(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk, **kwargs):
        super().__init__(master, **kwargs)
        self.html_label = HTMLLabel(self, html="")
        self.html_label.pack(fill="both", expand=True)
        self.refresh()

    def refresh(self) -> None:
        try:
            initialize_firebase()
            ref = db.reference("rankings/top_lucro")
            ranking = ref.order_by_value().limit_to_last(10).get() or {}
        except Exception as e:
            logger.error("Erro ao carregar dados de ranking.")
            messagebox.showerror("Erro", "Falha ao carregar o ranking. Verifique sua conexão.")
            return
        sorted_items = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        html = ["<h3>Ranking Global</h3><ol>"]
        for idx, (uid, lucro) in enumerate(sorted_items, start=1):
            medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else ""))
            highlight = "🔥" if idx == 1 else ("💰" if lucro > 500 else "")
            html.append(f"<li>{medal} {uid} - R$ {lucro:.2f} {highlight}</li>")
        html.append("</ol>")
        self.html_label.set_html("".join(html))
