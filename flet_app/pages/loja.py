import flet as ft
from flet import Icons  # 👈 Corrige o uso dos ícones

def render(page: ft.Page):
    itens = [
        {"nome": "Upgrade de Bot", "preco": 49.90},
        {"nome": "Macro Exclusivo", "preco": 79.90},
        {"nome": "Análise Premium", "preco": 129.90},
        {"nome": "Slot Extra", "preco": 29.90},
    ]

    cards = []
    for item in itens:
        cards.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(item["nome"], size=16, expand=True),
                            ft.Text(f"R$ {item['preco']:,.2f}"),
                            ft.ElevatedButton("Comprar", icon=Icons.SHOPPING_CART)  # 👈 Aqui foi corrigido
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),
                    padding=15
                )
            )
        )

    return ft.Column([
        ft.Text("Loja", size=24, weight=ft.FontWeight.BOLD),
        ft.Column(cards, spacing=10, expand=True)
    ], spacing=20, expand=True)
