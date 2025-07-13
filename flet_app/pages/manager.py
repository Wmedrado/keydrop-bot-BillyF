import flet as ft
import logging
from flet_app.services.manager_service import ManagerService

def render(page: ft.Page):
    headless_switch = ft.Switch(label="Modo Headless (Chrome invisível)", value=False)
    sorteio_1h_switch = ft.Switch(label="Participar apenas de sorteios de 1h", value=False)
    auto_restart_switch = ft.Switch(label="Reiniciar bots automaticamente em caso de falha", value=False)
    notificacoes_switch = ft.Switch(label="Receber notificações por email", value=False)
    mensagem = ft.Text("")
    loading = ft.ProgressBar(width=400, color="blue", visible=False)

    async def carregar_configuracoes(e=None):
        logger = logging.getLogger("manager")
        loading.visible = True
        mensagem.value = ""
        page.update()
        try:
            result = await ManagerService.get_config()
            if "error" in result:
                mensagem.value = result["error"]
                mensagem.color = ft.Colors.RED
            else:
                # Ajuste os nomes dos campos conforme o backend
                headless_switch.value = result.get("headless", False)
                sorteio_1h_switch.value = result.get("sorteio_1h", False)
                auto_restart_switch.value = result.get("auto_restart", False)
                notificacoes_switch.value = result.get("notificacoes", False)
                mensagem.value = "Configurações carregadas."
                mensagem.color = ft.Colors.GREEN
        except Exception as ex:
            logger.exception("Erro ao carregar configurações")
            mensagem.value = f"Erro inesperado: {str(ex)}"
            mensagem.color = ft.Colors.RED
        finally:
            loading.visible = False
            page.update()

    async def salvar_configuracoes(e=None):
        logger = logging.getLogger("manager")
        loading.visible = True
        mensagem.value = ""
        page.update()
        try:
            config = {
                "headless": bool(headless_switch.value),
                "sorteio_1h": bool(sorteio_1h_switch.value),
                "auto_restart": bool(auto_restart_switch.value),
                "notificacoes": bool(notificacoes_switch.value),
            }
            result = await ManagerService.update_config(config)
            if "error" in result:
                mensagem.value = result["error"]
                mensagem.color = ft.Colors.RED
                page.snack_bar = ft.SnackBar(ft.Text(result["error"], color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
                page.snack_bar.open = True
            else:
                mensagem.value = result.get("mensagem") or "Configurações salvas com sucesso!"
                mensagem.color = ft.Colors.GREEN
                page.snack_bar = ft.SnackBar(ft.Text(mensagem.value, color=ft.Colors.WHITE), bgcolor=ft.Colors.GREEN)
                page.snack_bar.open = True
                # Forçar recarregamento para garantir que switches reflitam o backend
                await carregar_configuracoes()
        except Exception as ex:
            logger.exception("Erro ao salvar configurações")
            mensagem.value = f"Erro inesperado: {str(ex)}"
            mensagem.color = ft.Colors.RED
            page.snack_bar = ft.SnackBar(ft.Text(mensagem.value, color=ft.Colors.WHITE), bgcolor=ft.Colors.RED)
            page.snack_bar.open = True
        finally:
            loading.visible = False
            page.update()

    page.run_task(carregar_configuracoes)

    return ft.Container(
        content=ft.Column([
            ft.Text("Gerenciador de Configurações do Bot", size=24, weight=ft.FontWeight.BOLD),
            headless_switch,
            sorteio_1h_switch,
            auto_restart_switch,
            notificacoes_switch,
            ft.ElevatedButton(
                "Salvar Configurações",
                icon=ft.Icons.SAVE,
                on_click=lambda e: page.run_task(salvar_configuracoes)
            ),
            loading,
            mensagem
        ], spacing=15),
        padding=20,
        expand=True
    )
