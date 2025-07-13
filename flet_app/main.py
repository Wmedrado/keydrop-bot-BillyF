import flet as ft
from pages import login, perfil, loja, ranking, debug, bots, manager

def main(page: ft.Page):
    page.title = "Keydrop Bot"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1000
    page.window_height = 700

    saldo_total_skins = 12345.67
    bots_ativos = 17

    saldo_text = ft.Text(f"Saldo total em skins: R$ {saldo_total_skins:,.2f}", size=14)
    # Pontinho verde animado
    import threading
    # Pontinho verde animado sem UserControl
    blinking_dot = ft.Container(
        width=12,
        height=12,
        bgcolor=ft.Colors.GREEN,
        border_radius=6,
        animate_opacity=ft.Animation(1200, ft.AnimationCurve.EASE_IN_OUT),
        opacity=1.0,
        margin=ft.margin.only(right=8)
    )
    import asyncio
    async def blink_dot():
        while True:
            blinking_dot.opacity = 1.0 if blinking_dot.opacity < 0.5 else 0.2
            blinking_dot.update()
            await asyncio.sleep(1.2)

    bots_text = ft.Text(f"Total de bots ativos: {bots_ativos}", size=14)
    bottom_bar = ft.Container(
        content=ft.Row(
            [saldo_text, ft.Container(expand=True),
             ft.Row([
                 blinking_dot,
                 bots_text
             ], alignment=ft.MainAxisAlignment.CENTER)
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=48,  # valor fixo, pode ajustar conforme desejar
        bgcolor=ft.Colors.GREY_900,
        padding=ft.padding.symmetric(horizontal=24),
    )

    titulo_text = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)
    content_column = ft.Column(
        controls=[
            titulo_text,
            login.render(page)
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )
    content_area = ft.Container(
        content=content_column,
        expand=True,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 0),
            colors=[
                "#0a1124",  # azul marinho escuro quase preto
                "#101a36",
                "#000510"
            ],
            tile_mode=ft.GradientTileMode.CLAMP
        )
    )

    def route_change(route):
        rotas = {
            "/login": ("Login", login.render),
            "/perfil": ("Perfil", perfil.render),
            "/loja": ("Loja", loja.render),
            "/ranking": ("Ranking", ranking.render),
            "/debug": ("Debug", debug.render),
            "/bots": ("Bots", bots.render),
            "/manager": ("Gerenciar", manager.render),
        }
        titulo, render_func = rotas.get(route, ("Login", login.render))
        # Atualiza o conteúdo da coluna interna
        content_column.controls.clear()
        content_column.controls.append(titulo_text)
        content_column.controls.append(render_func(page))
        page.update()

    def navegar(e):
        index = e.control.selected_index
        destino = e.control.destinations[index].data
        
        # Add a subtle scale animation to the selected navigation item
        sidebar.selected_index = index
        page.update()
        
        page.go(destino)

    # Custom NavigationRail sem UserControl
    sidebar = ft.NavigationRail(
        selected_index=0,
        extended=True,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.LOGIN, label="Login", data="/login"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil", data="/perfil"),
            ft.NavigationRailDestination(icon=ft.Icons.STORE, label="Loja", data="/loja"),
            ft.NavigationRailDestination(icon=ft.Icons.LEADERBOARD, label="Ranking", data="/ranking"),
            ft.NavigationRailDestination(icon=ft.Icons.BUG_REPORT, label="Debug", data="/debug"),
            ft.NavigationRailDestination(icon=ft.Icons.SMART_TOY, label="Bots", data="/bots"),
            ft.NavigationRailDestination(icon=ft.Icons.SETTINGS, label="Manager", data="/manager"),
        ],
        on_change=navegar,
    )

    layout = ft.Row(
        controls=[
            sidebar,
            ft.VerticalDivider(width=1),
            content_area,
        ],
        expand=True,
    )

    page.add(layout, bottom_bar)

    def on_mount(e):
        page.run_task(blink_dot)
    page.on_mount = on_mount

    def on_route_change(e):
        route_change(page.route)

    page.on_route_change = on_route_change

    if not page.route or page.route == "/":
        page.go("/login")

ft.app(target=main)