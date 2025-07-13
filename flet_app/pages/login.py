import flet as ft

def render(page: ft.Page):
    email = ft.TextField(label="Email", width=300)
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True, width=300)
    mensagem = ft.Text("", color=ft.Colors.RED)  # type: ignore[attr-defined]

    def entrar(e):
        if email.value == "admin@teste.com" and senha.value == "123456":
            mensagem.value = "Login realizado com sucesso!"
            mensagem.color = ft.Colors.GREEN  # type: ignore[attr-defined]
            page.go("/perfil")
        else:
            mensagem.value = "Credenciais inválidas."
            mensagem.color = ft.Colors.RED  # type: ignore[attr-defined]
        page.update()

    return ft.Column(
        [
            ft.Text("Login", size=32, weight=ft.FontWeight.BOLD),
            email,
            senha,
            ft.ElevatedButton("Entrar", on_click=entrar),
            mensagem
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
