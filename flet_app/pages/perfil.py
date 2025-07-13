import flet as ft

def render(page: ft.Page):
    # Dados simulados
    nome = "William Dev"
    lucro = "R$ 3.582,20"
    tempo_uso = "28h 16min"
    bots_ativos = 4

    # Layout
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(f"Nome: {nome}", size=22),
                ft.Text(f"Lucro Total: {lucro}", size=22),
                ft.Text(f"Tempo de Uso: {tempo_uso}", size=22),
                ft.Text(f"Bots Ativos: {bots_ativos}", size=22),
                ft.ElevatedButton(
                    "Atualizar Dados",
                    on_click=lambda e: page.snack_bar.open(
                        ft.SnackBar(ft.Text("Dados atualizados com sucesso!"))
                    )
                )
            ],
            spacing=15,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.START
        ),
        padding=20,
        expand=True
    )
