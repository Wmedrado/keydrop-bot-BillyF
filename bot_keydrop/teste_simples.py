#!/usr/bin/env python3
"""
Versão ultra simplificada para teste
"""

import tkinter as tk
import sys


def criar_interface_simples():
    """Criar interface super simples sem complicações"""
    print("Iniciando interface simples...")
    
    # Criar janela
    root = tk.Tk()
    root.title("Keydrop Bot v2.1.0 - TESTE")
    root.geometry("600x400")
    
    # Forçar aparecer
    root.lift()
    root.attributes('-topmost', True)
    root.after(100, lambda: root.attributes('-topmost', False))
    
    # Conteúdo
    label = tk.Label(root, text="🎉 KEYDROP BOT FUNCIONANDO!\n\nVersão Simplificada para Teste", 
                    font=('Arial', 16, 'bold'), pady=50)
    label.pack(expand=True)
    
    btn = tk.Button(root, text="✅ Aplicação Funciona!", 
                   font=('Arial', 12), command=root.quit, 
                   bg='green', fg='white', pady=10)
    btn.pack(pady=20)
    
    print("Interface criada, iniciando mainloop...")
    root.mainloop()
    print("Mainloop encerrado")

def main():
    try:
        print("=== KEYDROP BOT TESTE ===")
        print(f"Python: {sys.version}")
        print(f"Executável: {hasattr(sys, '_MEIPASS')}")
        
        # Importar dependências
        print("Importando tkinter...")
        import tkinter as tk_test  # noqa: F401
        print("✅ tkinter OK")
        
        print("Importando psutil...")
        import psutil  # noqa: F401
        print("✅ psutil OK")
        
        print("Criando interface...")
        criar_interface_simples()
        
        print("✅ Aplicação finalizada com sucesso!")
        
    except Exception as e:
        print(f"❌ ERRO: {e}")
        import traceback
        traceback.print_exc()
        
        try:
            import tkinter.messagebox as mb
            mb.showerror("Erro", f"Erro na aplicação:\n{e}")
        except:
            print("Erro ao mostrar messagebox também")

if __name__ == "__main__":
    main()
