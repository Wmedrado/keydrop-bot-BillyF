import flet as ft
from pages import login, perfil, loja, ranking, debug, bots

def main(page: ft.Page):
    page.title = "Keydrop Bot"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1000
    page.window_height = 700

    saldo_total_skins = 12345.67
    bots_ativos = 17

    saldo_text = ft.Text(f"Saldo total em skins: R$ {saldo_total_skins:,.2f}", size=14)
    bots_text = ft.Text(f"Total de bots ativos: {bots_ativos}", size=14)

    bottom_bar = ft.Container(
        content=ft.Row(
            [saldo_text, ft.Container(expand=True), bots_text],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        height=40,
        bgcolor=ft.Colors.GREY_900,
        padding=ft.padding.symmetric(horizontal=20),
    )

    titulo_text = ft.Text("Login", size=24, weight=ft.FontWeight.BOLD)
    content_area = ft.Column(
        controls=[
            titulo_text,
            login.render(page)
        ],
        expand=True
    )

    def route_change(route):
        rotas = {
            "/login": ("Login", login.render),
            "/perfil": ("Perfil", perfil.render),
            "/loja": ("Loja", loja.render),
            "/ranking": ("Ranking", ranking.render),
            "/debug": ("Debug", debug.render),
            "/bots": ("Bots", bots.render),
        }
        titulo, render_func = rotas.get(route, ("Login", login.render))
        titulo_text.value = titulo
        content_area.controls[1] = render_func(page)
        page.update()

    def navegar(e):
        index = e.control.selected_index
        destino = e.control.destinations[index].data
        page.go(destino)

    sidebar = ft.NavigationRail(
        selected_index=0,
        extended=True,
        destinations=[
            ft.NavigationRailDestination(icon=ft.Icons.LOGIN, label="Login", data="/login"),
            ft.NavigationRailDestination(icon=ft.Icons.PERSON, label="Perfil", data="/perfil"),
            ft.NavigationRailDestination(icon=ft.Icons.STORE, label="Loja", data="/loja"),
            ft.NavigationRailDestination(icon=ft.Icons.LEADERBOARD, label="Ranking", data="/ranking"),
            ft.NavigationRailDestination(icon=ft.Icons.BUG_REPORT, label="Debug", data="/debug"),
            ft.NavigationRailDestination(icon=ft.Icons.DEVICE_HUB, label="Bots", data="/bots"),
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

    def on_route_change(e):
        route_change(page.route)

    page.on_route_change = on_route_change

    if not page.route or page.route == "/":
        page.go("/login")

ft.app(target=main)