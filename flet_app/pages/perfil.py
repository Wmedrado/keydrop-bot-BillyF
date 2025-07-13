import flet as ft
import asyncio
import logging
from flet_app.services.auth_service import AuthService
from flet_app.services.token_service import TokenService  # Assuming a token management service

def render(page: ft.Page):
    # Visual elements with improved styling
    profile_container = ft.Column(spacing=15)
    loading_progress = ft.ProgressBar(width=400, color="blue", visible=False)
    error_text = ft.Text("", color="red", visible=False)

    async def atualizar_dados(e=None):
        logger = logging.getLogger("perfil")
        loading_progress.visible = True
        error_text.visible = False
        page.update()
        try:
            token = TokenService.get_token()
            if not token:
                return
            response = await AuthService.get_profile(token)
            if not response or "error" in response:
                # erro_msg = response.get("error", "Erro ao carregar dados do perfil")
                # error_text.value = erro_msg
                # error_text.visible = True
                # logger.error(f"Profile fetch error: {erro_msg}")
                pass
            else:
                profile_container.controls.clear()
                profile_container.controls.extend([
                    ft.Text(f"Nome: {response.get('nome', 'N/A')}", size=18, weight=ft.FontWeight.BOLD, tooltip="Seu nome de usuário cadastrado."),
                    ft.Text(f"Lucro Total: R$ {response.get('lucro', 'N/A')}", size=16, tooltip="Soma de todos os lucros obtidos com os bots."),
                    ft.Text(f"Tempo de Uso: {response.get('tempo_uso', 'N/A')} dias", size=16, tooltip="Quantidade de dias utilizando o sistema."),
                    ft.Text(f"Bots Ativos: {response.get('bots_ativos', 'N/A')}", size=16, tooltip="Total de bots ativos atualmente na sua conta.")
                ])
                logger.info("Profile data successfully retrieved")
        except Exception as e:
            pass
        finally:
            loading_progress.visible = False
            page.update()

    # Executar atualização ao carregar usando o método correto do Flet
    page.run_task(atualizar_dados)

    return ft.Container(
        content=ft.Column(
            [
                loading_progress,
                error_text,
                profile_container,
                ft.ElevatedButton(
                    "Atualizar Dados",
                    on_click=lambda e: page.run_task(atualizar_dados),
                    icon=ft.Icons.REFRESH,
                    tooltip="Clique para atualizar os dados do perfil."
                )
            ],
            spacing=15,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        padding=20,
        expand=True,
        tooltip="Tela de perfil do usuário. Veja seus dados e estatísticas."
    )
