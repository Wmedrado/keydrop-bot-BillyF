import flet as ft

def build_sidebar(page: ft.Page):
    destinos = [
        {"label": "Login", "icon": "login", "rota": "/login"},
        {"label": "Perfil", "icon": "person", "rota": "/perfil"},
        {"label": "Loja", "icon": "store", "rota": "/loja"},
        {"label": "Ranking", "icon": "leaderboard", "rota": "/ranking"},
        {"label": "Debug", "icon": "bug_report", "rota": "/debug"},
        {"label": "Bots", "icon": "devices", "rota": "/bots"},
    ]

    def navegar(e):
        index = e.control.selected_index
        rota = destinos[index]["rota"]
        page.go(rota)

    return ft.NavigationRail(
        selected_index=0,
        on_change=navegar,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icon(name=dest["icon"]),
                label=dest["label"]
            )
            for dest in destinos
        ],
        extended=True,
        bgcolor="#23272F",
        height=600
    )
