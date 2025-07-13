import flet as ft
import logging
from flet_app.services.ranking_service import RankingService

def render(page: ft.Page):
    ranking_container = ft.Column(spacing=10, expand=True)
    loading_progress = ft.ProgressBar(width=400, color="blue", visible=False)
    error_text = ft.Text("", color="red", visible=False)

    def get_icon_and_color(pos):
        if pos == 1:
            return ft.Icons.DIAMOND, "#41dcff"
        elif pos == 2:
            return ft.Icons.STAR, "#FAFC7A"
        elif pos == 3:
            return ft.Icons.STAR, "#aa9682"
        else:
            return None, None

    def item(pos, nome, bots_ativos, lucro=None):
        icon_name, color = get_icon_and_color(pos)
        icon_control = (
            ft.Icon(icon_name, color=color, size=24) if icon_name else ft.Container(width=24)
        )
        nome_text = ft.Text(nome, weight=ft.FontWeight.BOLD, size=18)
        if color:
            nome_text.color = color
        lucro_text = ft.Text(f"Lucro: R$ {lucro}" if lucro is not None else "", size=16)
        row_content = ft.Row(
            [
                ft.Text(str(pos), size=18, width=24, text_align=ft.TextAlign.CENTER),
                icon_control,
                nome_text,
                ft.Text(str(bots_ativos), size=18, expand=True, text_align=ft.TextAlign.RIGHT),
                lucro_text
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

    async def carregar_ranking(e=None):
        logger = logging.getLogger("ranking")
        loading_progress.visible = True
        error_text.visible = False
        page.update()
        try:
            result = await RankingService.get_ranking()
            ranking_container.controls.clear()
            if "error" in result:
                error_text.value = result["error"]
                error_text.visible = True
            else:
                ranking = result.get("ranking", [])
                if not ranking:
                    ranking_container.controls.append(ft.Text("Nenhum dado de ranking encontrado", color=ft.colors.GREY))
                else:
                    for idx, user in enumerate(ranking, 1):
                        ranking_container.controls.append(
                            item(idx, user.get("nome", "N/A"), user.get("bots_ativos", 0), user.get("lucro"))
                        )
        except Exception as e:
            logger.exception("Erro ao carregar ranking")
            error_text.value = f"Erro inesperado: {str(e)}"
            error_text.visible = True
        finally:
            loading_progress.visible = False
            page.update()

    page.run_task(carregar_ranking)

    titulo = ft.Container(
        content=ft.Text("Ranking de Bots Ativos", size=24, weight=ft.FontWeight.BOLD),
        padding=ft.padding.symmetric(vertical=12)
    )

    return ft.Column(
        [
            titulo,
            loading_progress,
            error_text,
            ranking_container,
            ft.ElevatedButton(
                "Atualizar Ranking",
                on_click=lambda e: page.run_task(carregar_ranking),
                icon=ft.Icons.REFRESH
            )
        ],
        spacing=10,
        expand=True
    )
