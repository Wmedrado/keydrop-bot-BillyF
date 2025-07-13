import flet as ft

def CardInfo(label: str, value: str):
    return ft.Card(
        content=ft.Container(
            content=ft.Column(
                [
                    ft.Text(label, size=14, color=ft.Colors.GRAY, weight=ft.FontWeight.MEDIUM),
                    ft.Text(value, size=20, weight=ft.FontWeight.BOLD)
                ],
                tight=True
            ),
            padding=15
        ),
        elevation=2,
        margin=ft.margin.all(5)
    )
