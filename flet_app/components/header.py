import flet as ft

def build_header(page: ft.Page):
    # Dicionário de títulos por rota
    titulos = {
        "/login": "Área de Login",
        "/perfil": "Perfil do Usuário",
        "/loja": "Loja de Itens",
        "/ranking": "Ranking Global",
        "/debug": "Modo Debug"
    }

    # Recupera o nome da rota atual
    titulo_atual = titulos.get(page.route, "Página")

    return ft.Container(
        content=ft.Text(titulo_atual, size=24, weight=ft.FontWeight.BOLD),
        padding=20,
        bgcolor="#1E1E1E",
        border_radius=ft.border_radius.only(top_left=10, top_right=10)
    )
