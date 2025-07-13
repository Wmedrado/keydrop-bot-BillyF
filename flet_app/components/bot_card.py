import flet as ft
import os
from typing import Optional

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(BASE_DIR, "..", "images")

def BotCard(
    nome: str,
    saldo_skins: str,
    lucro: str,
    status: str,
    hora: str,
    on_reiniciar,
    participando_amateur: bool = True,
    participando_contender: bool = True,
):
    borda_cor = {
        "rodando": ft.Colors.GREEN,
        "reiniciando": ft.Colors.ORANGE,
        "parado": ft.Colors.RED,
    }.get(status, ft.Colors.GREY)

    path_amateur = os.path.join(IMAGES_DIR, "amateur.png")
    path_contender = os.path.join(IMAGES_DIR, "contender.png")

    icones_competicoes = []

    if participando_amateur:
        icones_competicoes.append(
            ft.Container(
                content=ft.Image(src=path_amateur, width=64, height=64, fit=ft.ImageFit.CONTAIN, tooltip="Participando de sorteios de 3 minutos - AMATEUR"),
                padding=ft.padding.only(bottom=12),
                tooltip="Participando de sorteios de 3 minutos - AMATEUR"
            )
        )

    if participando_contender:
        icones_competicoes.append(
            ft.Container(
                content=ft.Image(src=path_contender, width=int(64*1.1), height=int(64*1.1), fit=ft.ImageFit.CONTAIN, tooltip="Participando de sorteios de 1 hora - CONTENDER"),
                padding=ft.padding.only(bottom=8, top=0, left=-10, right=0),
                tooltip="Participando de sorteios de 1 hora - CONTENDER"
            )
        )

    def on_hover_enter(e):
        e.control.border = ft.border.Border(
            left=ft.border.BorderSide(width=6, color=borda_cor),
            top=ft.border.BorderSide(width=6, color=borda_cor),
            right=ft.border.BorderSide(width=6, color=borda_cor),
            bottom=ft.border.BorderSide(width=6, color=borda_cor),
        )
        e.control.update()

    def on_hover_exit(e):
        e.control.border = ft.border.Border(
            left=ft.border.BorderSide(width=3, color=borda_cor),
            top=ft.border.BorderSide(width=3, color=borda_cor),
            right=ft.border.BorderSide(width=3, color=borda_cor),
            bottom=ft.border.BorderSide(width=3, color=borda_cor),
        )
        e.control.update()

    botao_reiniciar = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_color=ft.Colors.BLUE,
        tooltip="Reiniciar",
        on_click=on_reiniciar,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=6),
            padding=ft.padding.all(12),
            overlay_color=ft.Colors.TRANSPARENT
        ),
        width=128,
        height=128,
        on_hover=lambda e: (
            on_hover_enter(e) if e.data == "true" else on_hover_exit(e)
        ),
    )

    card_content = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text(nome, size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE, expand=True),

                ft.Row([
                    ft.Icon(ft.Icons.ACCESS_TIME, size=18, color=ft.Colors.BLUE),
                    ft.Text(hora, size=14, color=ft.Colors.BLUE),
                ], spacing=4)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Text(f"Saldo em skins {saldo_skins}", size=18, color="#9C7FFF"),
            ft.Text(f"Lucro {lucro}", size=18, color=ft.Colors.GREEN),

            ft.Row([
                ft.Row(icones_competicoes, spacing=0),

                ft.Container(expand=True),

                ft.Container(
                    content=botao_reiniciar,
                    margin=ft.Margin(80, 0, 16, 1),
                    padding=ft.padding.only(bottom=-10),
                )
            ], vertical_alignment=ft.CrossAxisAlignment.END, spacing=8),
        ], spacing=12, expand=True),
        width=360,
        height=280,
        padding=ft.padding.all(16),
        bgcolor=ft.Colors.BLACK,
        border=ft.border.Border(
            left=ft.border.BorderSide(width=3, color=borda_cor),
            top=ft.border.BorderSide(width=3, color=borda_cor),
            right=ft.border.BorderSide(width=3, color=borda_cor),
            bottom=ft.border.BorderSide(width=3, color=borda_cor),
        ),
        border_radius=12,
        on_hover=lambda e: (
            on_hover_enter(e) if e.data == "true" else on_hover_exit(e)
        )
    )
    return card_content
