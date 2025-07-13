import flet as ft
import asyncio
from flet_app.services.auth_service import AuthService
import webbrowser

def render(page: ft.Page):
    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    mensagem = ft.Text("", color=ft.Colors.RED)  # type: ignore[attr-defined]

    async def entrar_async():
        email_value = email.value or ""
        senha_value = senha.value or ""
        response = await AuthService.login(email_value, senha_value)
        if "error" in response:
            mensagem.value = f"Erro: {response['error']}"
            mensagem.color = ft.Colors.RED  # type: ignore[attr-defined]
        elif response.get("success"):
            mensagem.value = "Login realizado com sucesso!"
            mensagem.color = ft.Colors.GREEN  # type: ignore[attr-defined]
            page.go("/perfil")
        else:
            mensagem.value = "Credenciais inválidas."
            mensagem.color = ft.Colors.RED  # type: ignore[attr-defined]
        page.update()

    def entrar(e):
        asyncio.create_task(entrar_async())

    def login_discord(e):
        # URL do endpoint SSO do backend (ajuste conforme necessário)
        discord_url = "http://localhost:8000/sso/discord/login"
        webbrowser.open(discord_url)
        mensagem.value = "Aguarde o login via Discord no navegador."
        mensagem.color = ft.Colors.GREEN
        page.update()

    return ft.Column(
        [
            ft.Text("Login", size=32, weight=ft.FontWeight.BOLD),
            email,
            senha,
            ft.ElevatedButton("Entrar", on_click=entrar),
            ft.ElevatedButton(
                "Entrar com Discord",
                icon=ft.Icons.DISCORD,
                on_click=login_discord,
                bgcolor=ft.Colors.BLUE_GREY_900,
                color=ft.Colors.WHITE,
            ),
            mensagem
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
