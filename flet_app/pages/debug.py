import flet as ft

def render(page: ft.Page):
    logs = [
        "Iniciando bot...",
        "Bot conectado ao servidor.",
        "Erro detectado: timeout na requisição.",
        "Cache limpo com sucesso.",
        "Notificação enviada para Discord."
    ]

    log_text = "\n".join(logs)
    log_area = ft.Text(
        log_text,
        font_family="Consolas",
        size=14,
        expand=True,
        selectable=True,
    )

    def reiniciar_bot(e):
        page.snack_bar = ft.SnackBar(ft.Text("Bot reiniciado!"))
        page.snack_bar.open = True
        page.update()

    def limpar_cache(e):
        page.snack_bar = ft.SnackBar(ft.Text("Cache limpo!"))
        page.snack_bar.open = True
        page.update()

    def testar_notificacao(e):
        page.snack_bar = ft.SnackBar(ft.Text("Notificação testada!"))
        page.snack_bar.open = True
        page.update()

    return ft.Container(
        content=ft.Column(
            [
                ft.Text("Debug", size=24, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=log_area,
                    padding=10,
                    bgcolor="#2A2A2A",
                    border_radius=10,
                    expand=True,
                ),
                ft.Row(
                    [
                        ft.ElevatedButton("Reiniciar Bot", on_click=reiniciar_bot),
                        ft.ElevatedButton("Limpar Cache", on_click=limpar_cache),
                        ft.ElevatedButton("Testar Notificação", on_click=testar_notificacao),
                    ],
                    spacing=15,
                ),
            ],
            expand=True,
            spacing=20,
        ),
        padding=20,
        expand=True,
    )
