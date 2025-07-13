import flet as ft
import logging
from flet_app.services.sorteio_service import SorteioService

def render(page: ft.Page):
    headless_checkbox = ft.Checkbox(label="Modo Headless (Chrome invisível)", value=False)
    sorteio_1h_checkbox = ft.Checkbox(label="Participar apenas de sorteios de 1h", value=False)
    mensagem = ft.Text("")
    loading = ft.ProgressBar(width=400, color="blue", visible=False)

    async def participar_sorteio(e=None):
        logger = logging.getLogger("sorteios")
        loading.visible = True
        mensagem.value = ""
        page.update()
        try:
            # Garante que os argumentos nunca sejam None
            headless_value = headless_checkbox.value if headless_checkbox.value is not None else False
            sorteio_1h_value = sorteio_1h_checkbox.value if sorteio_1h_checkbox.value is not None else False
            result = await SorteioService.participar(
                headless=headless_value,
                sorteio_1h=sorteio_1h_value
            )
            if "error" in result:
                mensagem.value = f"Erro: {result['error']}"
                mensagem.color = ft.colors.RED
            else:
                mensagem.value = result.get("mensagem", "Participação realizada com sucesso!")
                mensagem.color = ft.colors.GREEN
        except Exception as ex:
            logger.exception("Erro ao participar do sorteio")
            mensagem.value = f"Erro inesperado: {str(ex)}"
            mensagem.color = ft.colors.RED
        finally:
            loading.visible = False
            page.update()

    return ft.Container(
        content=ft.Column([
            ft.Text("Participar de Sorteios", size=24, weight=ft.FontWeight.BOLD),
            headless_checkbox,
            sorteio_1h_checkbox,
            ft.ElevatedButton(
                "Participar",
                icon=ft.Icons.PLAY_ARROW,
                on_click=lambda e: page.run_task(participar_sorteio)
            ),
            loading,
            mensagem
        ], spacing=15),
        padding=20,
        expand=True
    )
