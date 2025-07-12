#!/usr/bin/env python3
"""
Teste da Interface Principal sem automação
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import time

def test_main_interface():
    """Testar apenas a interface principal"""
    print("🎯 Testando interface principal...")
    
    try:
        # Criar janela principal
        root = tk.Tk()
        root.title("Keydrop Bot Professional v3.0.0 - Teste Interface")
        root.geometry("900x700")
        root.configure(bg='#2d2d2d')
        
        # Header
        header = tk.Frame(root, bg='#2d2d2d')
        header.pack(fill='x', padx=15, pady=10)
        
        tk.Label(header, text="🤖 Keydrop Bot Professional v3.0.0",
                font=('Arial', 18, 'bold'), bg='#2d2d2d', fg='#2196f3').pack()
        
        # Notebook para abas
        notebook = ttk.Notebook(root)
        notebook.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Aba de controle
        control_frame = ttk.Frame(notebook)
        notebook.add(control_frame, text="🎮 Controle")
        
        # Área de status
        status_frame = ttk.LabelFrame(control_frame, text="📊 Status", padding=15)
        status_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        status_text = scrolledtext.ScrolledText(status_frame, height=15, 
                                              font=('Consolas', 12), bg='#2d2d2d', fg='#ffffff')
        status_text.pack(fill=tk.BOTH, expand=True)
        
        # Adicionar mensagem de teste
        timestamp = time.strftime("%H:%M:%S")
        status_text.insert(tk.END, f"[{timestamp}] ✅ Interface principal carregada com sucesso!\n")
        status_text.insert(tk.END, f"[{timestamp}] 🎯 Sistema funcionando perfeitamente\n")
        status_text.insert(tk.END, f"[{timestamp}] 📱 Pronto para testes\n")
        
        # Aba de configurações
        config_frame = ttk.Frame(notebook)
        notebook.add(config_frame, text="⚙️ Configurações")
        
        tk.Label(config_frame, text="⚙️ Configurações funcionando!", 
                font=('Arial', 14), bg='white').pack(pady=50)
        
        # Aba de logs
        logs_frame = ttk.Frame(notebook)
        notebook.add(logs_frame, text="📝 Logs")
        
        tk.Label(logs_frame, text="📝 Sistema de logs funcionando!", 
                font=('Arial', 14), bg='white').pack(pady=50)
        
        # Footer
        footer = tk.Frame(root, bg='#2d2d2d')
        footer.pack(fill='x', padx=15, pady=5)
        
        status_label = tk.Label(footer, text="🟢 Interface Desktop Ativa • Teste OK",
                              bg='#2d2d2d', fg='#4caf50', font=('Arial', 11, 'bold'))
        status_label.pack(side='left')
        
        # Centralizar janela
        root.update_idletasks()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - 900) // 2
        y = (screen_height - 700) // 2
        root.geometry(f"900x700+{x}+{y}")
        
        # Mostrar janela
        root.lift()
        root.focus_force()
        
        print("✅ Interface criada! Iniciando loop...")
        
        # Executar loop
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Erro na interface: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_main_interface()
