from __future__ import annotations

from typing import List, Dict
import customtkinter as ctk
from tkinter import messagebox

from cloud.firebase_client import registrar_compra


class StoreFrame(ctk.CTkFrame):
    """Interface de loja para itens premium."""

    PIX_KEY = "00020126360014BR.GOV.BCB.PIX0114+55199875533535204000053039865802BR5925William Franck Medrado Ba6009SAO PAULO62140510i2Xyt24EJY63040EB7"

    PRODUCTS = [
        {
            "id": "premium",
            "nome": "Acesso Premium",
            "preco": 29.9,
            "descricao": "Desbloqueia recursos profissionais",
        },
        {
            "id": "tema_extra",
            "nome": "Tema Extra",
            "preco": 9.9,
            "descricao": "Tema visual adicional",
        },
    ]

    def __init__(self, master: ctk.CTk, user_id: str | None = None, **kwargs):
        super().__init__(master, **kwargs)
        self.user_id = user_id or "anon"
        self.cart: List[Dict] = []
        self._build()

    def _build(self) -> None:
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.products_frame = ctk.CTkScrollableFrame(self)
        self.products_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        self.cart_frame = ctk.CTkFrame(self)
        self.cart_frame.grid(row=0, column=1, sticky="ns", padx=5, pady=5)

        self.cart_list = ctk.CTkFrame(self.cart_frame)
        self.cart_list.pack(fill="both", expand=True)
        self.total_var = ctk.StringVar(value="Total: R$ 0.00")
        ctk.CTkLabel(self.cart_frame, textvariable=self.total_var).pack(pady=5)
        ctk.CTkButton(
            self.cart_frame, text="Finalizar Pagamento", command=self._checkout
        ).pack(pady=5)

        for prod in self.PRODUCTS:
            card = ctk.CTkFrame(self.products_frame)
            card.pack(fill="x", pady=5, padx=5)
            ctk.CTkLabel(card, text=prod["nome"], font=("Arial", 14)).pack(anchor="w")
            ctk.CTkLabel(card, text=prod["descricao"], wraplength=180).pack(anchor="w")
            ctk.CTkLabel(card, text=f"R$ {prod['preco']:.2f}").pack(anchor="w")
            ctk.CTkButton(
                card,
                text="Adicionar ao carrinho",
                command=lambda p=prod: self._add_to_cart(p),
            ).pack(anchor="e", pady=5)

    def _add_to_cart(self, prod: Dict) -> None:
        self.cart.append(prod)
        self._update_cart()

    def _remove_item(self, index: int) -> None:
        self.cart.pop(index)
        self._update_cart()

    def _update_cart(self) -> None:
        for child in self.cart_list.winfo_children():
            child.destroy()
        total = 0.0
        for idx, item in enumerate(self.cart):
            row = ctk.CTkFrame(self.cart_list)
            row.pack(fill="x")
            ctk.CTkLabel(row, text=item["nome"]).pack(side="left")
            ctk.CTkButton(
                row,
                text="Remover",
                width=60,
                command=lambda i=idx: self._remove_item(i),
            ).pack(side="right")
            total += item["preco"]
        self.total_var.set(f"Total: R$ {total:.2f}")

    def _checkout(self) -> None:
        if not self.cart:
            messagebox.showinfo("Carrinho", "Adicione itens ao carrinho primeiro.")
            return
        PaymentWindow(self, self.user_id, self.cart, self.PIX_KEY)


class PaymentWindow(ctk.CTkToplevel):
    def __init__(self, master: ctk.CTk, user_id: str, itens: List[Dict], pix_key: str):
        super().__init__(master)
        self.user_id = user_id
        self.itens = itens
        self.pix_key = pix_key
        self.title("Pagamento")
        self._build()

    def _build(self) -> None:
        ctk.CTkLabel(self, text="Chave Pix:").pack(pady=5)
        entry = ctk.CTkEntry(self, width=300)
        entry.insert(0, self.pix_key)
        entry.configure(state="readonly")
        entry.pack(pady=5)

        ctk.CTkButton(
            self, text="Copiar", command=lambda: self.clipboard_append(self.pix_key)
        ).pack()

        try:
            import qrcode
            from PIL import ImageTk

            img = qrcode.make(self.pix_key)
            img = img.resize((180, 180))
            photo = ImageTk.PhotoImage(img)
            label = ctk.CTkLabel(self, image=photo, text="")
            label.image = photo
            label.pack(pady=5)
        except Exception:
            pass

        ctk.CTkButton(self, text="Já paguei", command=self._confirm).pack(pady=10)

    def _confirm(self) -> None:
        try:
            registrar_compra(self.user_id, self.itens)
        except Exception as exc:  # pragma: no cover - network errors
            messagebox.showerror("Erro", f"Falha ao registrar compra.\n{exc}")
        finally:
            messagebox.showinfo(
                "Pagamento",
                "Compra em validação, será liberado em até 10 minutos.",
            )
            self.destroy()
