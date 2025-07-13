import flet as ft
from typing import Optional

class TooltipWrapper(ft.UserControl):
    def __init__(self, control: ft.Control, message: str):
        super().__init__()
        self.control = control
        self.message = message

    def build(self):
        return ft.Column([
            self.control,
            ft.Text(self.message, visible=False, color=ft.Colors.GRAY)  # Simulação simples
        ])

def BotaoIcone(label: str, icon_name: str, on_click, tooltip: Optional[str] = None):
    btn = ft.ElevatedButton(
        text=label,
        icon=icon_name,
        on_click=on_click
    )
    if tooltip:
        return TooltipWrapper(btn, tooltip)
    return btn
