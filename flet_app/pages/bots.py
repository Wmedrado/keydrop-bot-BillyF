import flet as ft
from components.bot_card import BotCard

from flet_app.services.bot_service import BotService

def render(page: ft.Page):
    bots = []

    async def reiniciar_bot(e, bot):
        try:
            await BotService.restart_bot(bot.get('id'))
        except Exception:
            pass
        await carregar_bots()

    cards_row = ft.ResponsiveRow(run_spacing=12, spacing=12)

    async def carregar_bots():
        nonlocal bots
        try:
            result = await BotService.get_bots()
            bots = result.get('bots', []) if isinstance(result, dict) else []
        except Exception:
            bots = []
        # Se não vier nenhum bot do backend, adiciona 3 bots fictícios desligados
        if not bots:
            bots = [
                {"nome": "Bot 1", "saldo_skins": "R$ 0.00", "lucro": "R$ 0.00", "status": "parado", "hora": "--:--"},
                {"nome": "Bot 2", "saldo_skins": "R$ 0.00", "lucro": "R$ 0.00", "status": "parado", "hora": "--:--"},
                {"nome": "Bot 3", "saldo_skins": "R$ 0.00", "lucro": "R$ 0.00", "status": "parado", "hora": "--:--"},
            ]
        cards_row.controls.clear()
        for bot in bots:
            # Botão de reiniciar: muda para verde ao clicar, volta ao normal depois
            reiniciar_btn_ref = ft.Ref[ft.IconButton]()
            async def on_reiniciar(e, b=bot, ref=reiniciar_btn_ref):
                btn = ref.current
                if btn:
                    btn.bgcolor = ft.colors.GREEN
                    btn.update()
                page.run_task(reiniciar_bot, e, b)
                if btn:
                    btn.bgcolor = None
                    btn.update()

            bot_card = BotCard(
                nome=bot.get("nome", "Bot"),
                saldo_skins=bot.get("saldo_skins", "R$ 0.00"),
                lucro=bot.get("lucro", "R$ 0.00"),
                status=bot.get("status", "desconhecido"),
                hora=bot.get("hora", "--:--"),
                on_reiniciar=lambda e, b=bot, ref=reiniciar_btn_ref: on_reiniciar(e, b, ref)
            )
            cards_row.controls.append(
                ft.Container(
                    content=bot_card,
                    col={'xs': 12, 'sm': 6, 'md': 4, 'lg': 3},
                    height=280,
                    padding=8,
                    expand=False,
                    tooltip=f"Bot: {bot.get('nome', 'Bot')}. Clique no botão de recarregar para reiniciar este bot. Status: {bot.get('status', 'desconhecido')}"
                )
            )
        page.update()

    # Carrega bots ao abrir a tela
    page.run_task(carregar_bots)

    return ft.Container(
        content=ft.Column([
            ft.Text("Bots", size=24, weight=ft.FontWeight.BOLD, tooltip="Gerencie e monitore seus bots cadastrados."),
            ft.Container(
                content=cards_row,
                padding=20,
                expand=True,
                tooltip="Área de exibição dos bots. Role para ver todos."
            )
        ], scroll=ft.ScrollMode.ALWAYS),
        padding=20,
        expand=True,
        tooltip="Tela de gerenciamento de bots."
    )
