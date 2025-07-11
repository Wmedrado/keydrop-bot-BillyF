#!/usr/bin/env python3
"""
Versão de debug do Keydrop Bot - Para diagnosticar problemas no executável
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import time
from pathlib import Path

def main():
    """Versão de debug simples"""
    print("=== DEBUG KEYDROP BOT ===")
    print(f"Python: {sys.version}")
    print(f"Executável: {hasattr(sys, '_MEIPASS')}")
    print(f"Diretório atual: {os.getcwd()}")
    
    try:
        # Configurar ambiente básico
        if hasattr(sys, '_MEIPASS'):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent
        
        os.chdir(base_path)
        print(f"Base path: {base_path}")
        
        # Testar dependências críticas
        print("Testando dependências...")
        
        try:
            import psutil
            print("✅ psutil OK")
        except Exception as e:
            print(f"❌ psutil: {e}")
            return
        
        try:
            import requests
            print("✅ requests OK")
        except Exception as e:
            print(f"❌ requests: {e}")
            return
        
        # Testar tkinter
        print("Testando tkinter...")
        try:
            root = tk.Tk()
            root.title("Debug Test")
            root.geometry("400x300")
            
            # Forçar aparecer
            root.lift()
            root.attributes('-topmost', True)
            root.after(100, lambda: root.attributes('-topmost', False))
            
            # Adicionar conteúdo
            label = tk.Label(root, text="🎯 DEBUG: Keydrop Bot\n\nSe você está vendo esta janela,\no executável está funcionando!\n\nClique 'OK' para fechar.", 
                           font=('Arial', 12), justify=tk.CENTER, pady=20)
            label.pack(expand=True)
            
            def fechar():
                print("✅ Interface funcionando - fechando")
                root.destroy()
            
            btn = tk.Button(root, text="OK - Fechar", command=fechar, font=('Arial', 12))
            btn.pack(pady=10)
            
            print("✅ Tkinter configurado - iniciando mainloop")
            root.mainloop()
            print("✅ Mainloop encerrado")
            
        except Exception as e:
            print(f"❌ Erro tkinter: {e}")
            return
        
        print("✅ Debug concluído com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
