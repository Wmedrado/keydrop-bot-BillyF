import flet as ft

def LedStatus(ativo: bool):
    cor = ft.Colors.GREEN if ativo else ft.Colors.RED
    return ft.Container(
        content=ft.CircleAvatar(radius=10, bgcolor=cor),
        width=24,
        height=24,
        padding=4,
        alignment=ft.alignment.center
    )

def Spinner():
    return ft.ProgressRing(width=24, height=24, color=ft.Colors.BLUE, stroke_width=4)

def BotsStatus(page: ft.Page):
    bots = [
        {"nome": "Bot 1", "ativo": True},
        {"nome": "Bot 2", "ativo": False},
        {"nome": "Bot 3", "ativo": True},
    ]

    linhas = []
    for bot in bots:
        status = LedStatus(bot["ativo"])
        linhas.append(
            ft.Row([
                status,
                ft.Text(bot["nome"], expand=True)
            ], alignment=ft.MainAxisAlignment.START, spacing=15)
        )

    return ft.Column(linhas, spacing=10, expand=True)
