import flet as ft
from flet import Icons  # 👈 Corrige o uso dos ícones

import os
import random
def render(page: ft.Page):
    planos = [
        {
            "nome": "Plano Gratuito (Free)",
            "cor": ft.Colors.GREEN_600,
            "icone": "🟢",
            "preco": "Grátis",
            "beneficios": [
                "Acesso limitado a bots (ex: 20 bot ativo por vez)",
                "Sem suporte prioritário",
                "Limite de sorteios/drops por dia",
                "Sem personalização de skins ou filtros avançados",
                "Pode conter anúncios ou notificações do sistema"
            ]
        },
        {
            "nome": "Plano Profissional (Pro)",
            "cor": ft.Colors.PURPLE_600,
            "icone": "🟣",
            "preco": "R$ 49,90/mês",
            "beneficios": [
                "Até 100 bots ativos simultaneamente",
                "Acesso a API WebSocket (modo autônomo)",
                "Filtros avançados de skins, preferência por tipos específicos",
                "Participação automática em eventos e caixas promocionais",
                "Estatísticas detalhadas (lucro por dia, por bot, etc.)",
                "Interface personalizada para o usuário",
                "Suporte via Discord com prioridade",
                "Atualizações em tempo real"
            ]
        },
        {
            "nome": "Plano Elite (VIP)",
            "cor": ft.Colors.RED_600,
            "icone": "🔴",
            "preco": "R$ 129,90/mês",
            "beneficios": [
                "Bots ilimitados simultaneamente",
                "Integração com múltiplas contas e proxies dedicados",
                "Detecção automática de oportunidades raras",
                "Otimização de chances baseada em histórico de vitórias",
                "Acesso antecipado a novas funcionalidades",
                "Canal VIP para sugestões e relatórios semanais",
                "Acesso ao painel completo com visão macro de todos os bots e ganhos",
                "Suporte 1:1 via chamada (sob demanda)"
            ]
        },
    ]

    # Estado para exibir pagamento
    show_payment_dialog = ft.Ref[ft.AlertDialog]()
    payment_dialog = ft.AlertDialog(ref=show_payment_dialog, open=False)
    page.dialog = payment_dialog
    qr_code_img = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../keydrop-bot-BillyF/pay/qrcodepix.png'))
    pix_key = "00020126360014BR.GOV.BCB.PIX0114+55199875533535204000053039865802BR5925William Franck Medrado Ba6009SAO PAULO62140510IvFd8sKHUa6304E660"
    payment_token = ft.Ref[ft.Text]()
    # confetti_overlay removido, não é mais usado

    def gerar_token():
        return "PAY-" + ''.join(random.choices('ABCDEFGHJKLMNPQRSTUVWXYZ23456789', k=10))

    def show_qr_code(token):
        dialog_content = ft.Container(
            content=ft.Column([
                ft.Text("Pagamento via Pix", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900, tooltip="Modal de pagamento Pix para ativação do plano."),
                ft.Text(f"Token de pagamento: {token}", ref=payment_token, selectable=True, color=ft.Colors.BLACK, size=14, tooltip="Token único para identificar seu pagamento."),
                ft.Image(src=qr_code_img, width=220, height=220, fit=ft.ImageFit.CONTAIN, tooltip="Escaneie o QR Code no app do seu banco."),
                ft.Text("Chave Pix:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, tooltip="Chave Pix para pagamento manual."),
                ft.Text(pix_key, selectable=True, color=ft.Colors.BLACK, size=13, tooltip="Clique para copiar a chave Pix."),
                ft.ElevatedButton("Copiar chave Pix", icon=Icons.CONTENT_COPY, on_click=lambda e: page.set_clipboard(pix_key), tooltip="Copia a chave Pix para a área de transferência."),
                ft.Text("Após o pagamento, envie o comprovante para o suporte.", size=12, color=ft.Colors.GREY_700, tooltip="Envie o comprovante para liberar o plano.")
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=14),
            padding=30,
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            shadow=ft.BoxShadow(blur_radius=18, color=ft.Colors.BLUE_900+"22", offset=ft.Offset(0, 8)),
            expand=False,
            width=380,
            height=380
        )
        if show_payment_dialog.current is not None:
            show_payment_dialog.current.content = dialog_content
            show_payment_dialog.current.open = True
            page.dialog = show_payment_dialog.current
            page.update()

    cards = []
    def make_on_comprar(plano):
        def on_comprar(e):
            token = gerar_token()
            show_qr_code(token)
        return on_comprar

    for plano in planos:
        if "Gratuito" in plano["nome"]:
            btn = ft.ElevatedButton(
                "Ativo",
                icon=Icons.CHECK_CIRCLE,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.GREY_300,
                    color=ft.Colors.GREY_600,
                    padding=ft.Padding(15, 10, 15, 10),
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                expand=True,
                disabled=True,
                tooltip="Este plano já está ativo na sua conta."
            )
        else:
            btn = ft.ElevatedButton(
                "Comprar",
                icon=Icons.SHOPPING_CART,
                style=ft.ButtonStyle(
                    bgcolor=plano["cor"],
                    color=ft.Colors.WHITE,
                    padding=ft.Padding(15, 10, 15, 10),
                    shape=ft.RoundedRectangleBorder(radius=12)
                ),
                expand=True,
                on_click=make_on_comprar(plano),
                tooltip=f"Clique para comprar o {plano['nome']}."
            )
        cards.append(
            ft.Card(
                elevation=10,
                margin=12,
                content=ft.Container(
                    content=ft.Column([
                        ft.Text(plano["icone"], size=38, text_align=ft.TextAlign.CENTER, tooltip=f"Ícone do {plano['nome']}"),
                        ft.Text(plano["nome"], size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER, tooltip=f"Nome do plano: {plano['nome']}"),
                        ft.Text(plano["preco"], size=16, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER, tooltip=f"Preço do plano: {plano['preco']}"),
                        ft.Text("Benefícios:", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK, text_align=ft.TextAlign.CENTER, tooltip="Lista de benefícios inclusos no plano."),
                        ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.CHECK_CIRCLE, color=plano["cor"], size=18, tooltip="Benefício incluso."),
                                ft.Text(benef, size=13, tooltip=benef)
                            ], spacing=6)
                            for benef in plano["beneficios"]
                        ], spacing=2, expand=False),
                        btn
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                    padding=24,
                    width=270,
                    height=420,
                    bgcolor=ft.Colors.WHITE + "F2",
                    border_radius=18,
                    shadow=ft.BoxShadow(blur_radius=22, color=plano["cor"] + "22", offset=ft.Offset(0, 10)),
                    tooltip=f"Cartão do {plano['nome']}. Clique em comprar para adquirir este plano."
                )
            )
        )

    # Retorna o layout normalmente (dialog já foi adicionado ao page no início)
    return ft.Container(
        content=ft.Column([
            ft.Text("Planos Keydrop", size=30, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900, text_align=ft.TextAlign.CENTER, tooltip="Escolha um plano para ativar recursos avançados."),
            ft.Container(
                content=ft.Column([
                    ft.ResponsiveRow(
                        controls=cards,
                        spacing=22,
                        run_spacing=22,
                        alignment=ft.MainAxisAlignment.CENTER
                    )
                ], expand=True),
                expand=True,
                tooltip="Lista de planos disponíveis. Role para ver mais."
            )
        ], spacing=36, expand=True, scroll=ft.ScrollMode.ALWAYS),
        padding=36,
        gradient=ft.LinearGradient(
            begin=ft.Alignment(-1, 0),
            end=ft.Alignment(1, 1),
            colors=["#e0e7ff", "#f0f4ff", "#c7d2fe"]
        ),
        expand=True,
        tooltip="Tela da loja Keydrop."
    )
