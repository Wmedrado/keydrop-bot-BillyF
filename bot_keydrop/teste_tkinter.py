#!/usr/bin/env python3
"""
Teste simples do executável - Verificar se tkinter funciona
"""

import tkinter as tk
from tkinter import messagebox
import sys
import traceback

def teste_simples():
    try:
        # Criar janela simples
        root = tk.Tk()
        root.title("TESTE - Keydrop Bot")
        root.geometry("400x200")
        
        # Centralizar na tela
        root.eval('tk::PlaceWindow . center')
        
        # Trazer para frente
        root.lift()
        root.attributes('-topmost', True)
        root.after(100, lambda: root.attributes('-topmost', False))
        
        # Mensagem
        label = tk.Label(root, text="✅ TESTE FUNCIONANDO!\n\nSe você vê esta janela,\no executável está correto.", 
                        font=('Arial', 12), justify=tk.CENTER, pady=20)
        label.pack(expand=True)
        
        # Botão
        btn = tk.Button(root, text="OK - Fechar", command=root.quit, 
                       font=('Arial', 10), bg='lightgreen')
        btn.pack(pady=10)
        
        # Mostrar janela
        root.mainloop()
        
    except Exception as e:
        # Se der erro, mostrar messagebox
        error_msg = f"Erro no teste: {e}\n\nStack trace:\n{traceback.format_exc()}"
        print(error_msg)
        try:
            messagebox.showerror("Erro no Teste", error_msg)
        except:
            print("Erro ao mostrar messagebox também!")

if __name__ == "__main__":
    teste_simples()
