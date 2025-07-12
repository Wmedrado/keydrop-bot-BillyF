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
        except Exception:
            logger.error("Erro ao carregar dados de ranking.")
            messagebox.showerror("Erro", "Falha ao carregar o ranking. Verifique sua conexão.")
            return

        sorted_items = sorted(ranking.items(), key=lambda x: x[1], reverse=True)
        style = (
            "<style>.avatar{width:60px;height:60px;border-radius:50%;object-fit:cover;}"
            ".frame-neon{border:2px solid #0ff;box-shadow:0 0 4px #0ff;"
            "animation:neonPulse 1s ease-in-out infinite alternate;}"
            "@keyframes neonPulse{from{box-shadow:0 0 4px #0ff;}to{box-shadow:0 0 12px #0ff;}}"
            ".frame-diamond{border:2px solid transparent;"
            "border-image:linear-gradient(45deg,#09f,#fff,#09f) 1;"
            "animation:diamondSpin 4s linear infinite;}"
            "@keyframes diamondSpin{from{filter:hue-rotate(0deg);}to{filter:hue-rotate(360deg);}}"
            ".frame-gold{border:2px solid gold;box-shadow:0 0 6px gold;}"
            ".avatar-box{display:inline-block;margin-right:4px;vertical-align:middle;}"
            "</style>"
        )
        html = [style, "<h3>Ranking Global</h3><ol>"]
        for idx, (uid, lucro) in enumerate(sorted_items, start=1):
            medal = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else ""))
            highlight = "🔥" if idx == 1 else ("💰" if lucro > 500 else "")
            user_data = db.reference(f"users/{uid}").get() or {}
            name = user_data.get("nome", uid)
            foto = user_data.get("foto_url", "")
            perms = db.reference(f"permissions/{uid}").get() or {}
            frame = perms.get("selected_frame")
            if not frame:
                for item in perms.get("items_owned", []):
                    if str(item).startswith("frame_"):
                        frame = item
                        break
            frame_cls = f"frame-{frame.split('_',1)[1]}" if frame else ""
            avatar = f'<span class="avatar-box"><img src="{foto}" class="avatar {frame_cls}"></span>' if foto else ""
            html.append(f"<li>{medal} {avatar}{name} - R$ {lucro:.2f} {highlight}</li>")
        html.append("</ol>")
        self.html_label.set_html("".join(html))
