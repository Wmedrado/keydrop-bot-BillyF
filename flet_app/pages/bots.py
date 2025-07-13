import flet as ft
from components.bot_card import BotCard

def render(page: ft.Page):
    bots = [
        {
            "nome": "Bot 1",
            "saldo_skins": "R$ 2000.00",
            "lucro": "R$ 10.00",
            "status": "rodando",
            "hora": "12:00",
        },
        {
            "nome": "Bot 2",
            "saldo_skins": "R$ 0.00",
            "lucro": "R$ 0.00",
            "status": "reiniciando",
            "hora": "11:52",
        },
        {
            "nome": "Bot 3",
            "saldo_skins": "R$ 0.00",
            "lucro": "R$ 0.00",
            "status": "parado",
            "hora": "11:00",
        },
    ]

    def reiniciar_bot(e, bot):
        print(f"Reiniciando {bot['nome']}")

    cards = []
    for bot in bots:
        cards.append(
            ft.Container(
                content=BotCard(
                    nome=bot["nome"],
                    saldo_skins=bot["saldo_skins"],
                    lucro=bot["lucro"],
                    status=bot["status"],
                    hora=bot["hora"],
                    on_reiniciar=lambda e, b=bot: reiniciar_bot(e, b),
                ),
                width=360,
                height=280,
                padding=8,
                expand=False
            )
        )

    return ft.Container(
        content=ft.Column([
            ft.Text("Bots", size=24, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Row(
                    controls=cards,
                    spacing=12,
                    run_spacing=12,
                    alignment=ft.MainAxisAlignment.CENTER,
                    wrap=True
                ),
                padding=20,
                expand=True
            )
        ]),
        padding=20,
        expand=True
    )
