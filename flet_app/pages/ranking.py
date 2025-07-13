import flet as ft

def render(page: ft.Page):
    ranking = [
        {"posicao": 1, "nome": "PlayerOne", "bots_ativos": 15},
        {"posicao": 2, "nome": "PlayerTwo", "bots_ativos": 12},
        {"posicao": 3, "nome": "PlayerThree", "bots_ativos": 10},
        {"posicao": 4, "nome": "PlayerFour", "bots_ativos": 9},
        {"posicao": 5, "nome": "PlayerFive", "bots_ativos": 8},
    ]

    def get_icon_and_color(pos):
        if pos == 1:
            return ft.Icons.DIAMOND, "#41dcff"  # Diamante azul
        elif pos == 2:
            return ft.Icons.STAR, "#FAFC7A"     # Estrela prata
        elif pos == 3:
            return ft.Icons.STAR, "#aa9682"     # Estrela bronze
        else:
            return None, None

    def item(pos, nome, bots_ativos):
        icon_name, color = get_icon_and_color(pos)
        icon_control = (
            ft.Icon(icon_name, color=color, size=24) if icon_name else ft.Container(width=24)
        )
        nome_text = ft.Text(nome, weight=ft.FontWeight.BOLD, size=18)
        if color:
            nome_text.color = color

        row_content = ft.Row(
            [
                ft.Text(str(pos), size=18, width=24, text_align=ft.TextAlign.CENTER),
                icon_control,
                nome_text,
                ft.Text(str(bots_ativos), size=18, expand=True, text_align=ft.TextAlign.RIGHT),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=8,
        )

        container = ft.Container(
            content=row_content,
            on_hover=lambda e: (
                setattr(row_content, "scale", 1.05) if e.data == "true" else setattr(row_content, "scale", 1.0),
                row_content.update()
            )
        )

        padded_container = ft.Container(
            content=container,
            padding=ft.padding.symmetric(vertical=8, horizontal=12)
        )

        return padded_container

    itens = [item(r["posicao"], r["nome"], r["bots_ativos"]) for r in ranking]

    titulo = ft.Container(
        content=ft.Text("Ranking de Bots Ativos", size=24, weight=ft.FontWeight.BOLD),
        padding=ft.padding.symmetric(vertical=12)
    )

    return ft.Column(
        [
            titulo,
            ft.Divider(),
            *itens
        ],
        spacing=10,
        expand=True
    )
