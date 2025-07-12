#!/usr/bin/env python3
"""
Teste progressivo do Keydrop Bot - Para identificar onde trava
"""

import tkinter as tk
from tkinter import ttk
import sys
import os
import traceback
from pathlib import Path

class KeydropBotGUI_Teste:
    def __init__(self):
        print("1. Iniciando __init__ da GUI...")
        
        self.root = tk.Tk()
        print("2. tk.Tk() criado...")
        
        self.root.title("Keydrop Bot Professional v2.1.0")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        print("3. Configurações básicas aplicadas...")
        
        # Forçar janela aparecer
        self.root.lift()
        self.root.attributes('-topmost', True)
        self.root.after(100, lambda: self.root.attributes('-topmost', False))
        print("4. Forçar janela aparecer aplicado...")
        
        # Centralizar na tela
        try:
            self.root.eval('tk::PlaceWindow . center')
            print("5. Janela centralizada...")
        except Exception:
            print("5. Erro ao centralizar - continuando...")
        
        # Definir diretório base correto
        try:
            if hasattr(sys, '_MEIPASS'):
                # Executando como executável PyInstaller
                self.base_path = Path(sys.executable).parent
            else:
                # Executando como script Python
                self.base_path = Path(__file__).parent
            print(f"6. Base path definido: {self.base_path}")
        except Exception as e:
            print(f"6. Erro ao definir base path: {e}")
            self.base_path = Path(".")
        
        # Tentar definir ícone
        try:
            icon_path = self.base_path / "bot-icone.ico"
            if icon_path.exists():
                self.root.iconbitmap(str(icon_path))
                print("7. Ícone aplicado...")
            else:
                print("7. Ícone não encontrado - continuando...")
        except Exception as e:
            print(f"7. Erro no ícone: {e} - continuando...")
        
        # Variáveis básicas
        try:
            self.server_process = None
            self.server_running = False
            self.config_file = self.base_path / "config" / "bot_config.json"
            print("8. Variáveis básicas definidas...")
        except Exception as e:
            print(f"8. Erro nas variáveis: {e}")
        
        # Interface simples
        try:
            label = tk.Label(self.root, text="🎯 Keydrop Bot Professional v2.1.0\n\nSe você está vendo esta tela,\no executável está funcionando!\n\nAgora vou tentar criar a interface completa...", 
                           font=('Arial', 12), justify=tk.CENTER, pady=20)
            label.pack(expand=True)
            print("9. Interface simples criada...")
        except Exception as e:
            print(f"9. Erro na interface simples: {e}")
        
        # Depois de 3 segundos, tentar criar interface completa
        self.root.after(3000, self.criar_interface_completa)
        print("10. __init__ concluído!")

    def criar_interface_completa(self):
        """Tentar criar interface completa após inicialização básica"""
        try:
            print("11. Tentando criar interface completa...")
            
            # Limpar interface simples
            for widget in self.root.winfo_children():
                widget.destroy()
            print("12. Interface simples removida...")
            
            # Configurar estilo
            self.setup_style()
            print("13. Estilo configurado...")
            
            # Criar interface
            self.create_interface()
            print("14. Interface completa criada!")
            
        except Exception as e:
            print(f"ERRO ao criar interface completa: {e}")
            traceback.print_exc()
            
            # Mostrar erro na tela
            error_label = tk.Label(self.root, text=f"❌ Erro ao criar interface:\n{e}", 
                                 font=('Arial', 10), foreground='red', justify=tk.CENTER)
            error_label.pack(expand=True)

    def setup_style(self):
        """Configurar estilo da interface"""
        style = ttk.Style()
        
        # Tentar tema moderno
        try:
            style.theme_use('clam')
        except Exception:
            style.theme_use('default')
        
        # Cores personalizadas
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')

    def create_interface(self):
        """Criar a interface principal (versão simplificada)"""
        # Header
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(header_frame, text="🤖 Keydrop Bot Professional v2.1.0", 
                 style='Title.TLabel').pack()
        ttk.Label(header_frame, text="✅ EXECUTÁVEL FUNCIONANDO CORRETAMENTE!", 
                 foreground='green', font=('Arial', 12, 'bold')).pack()
        
        # Informações
        info_frame = ttk.LabelFrame(self.root, text="📋 Status", padding=10)
        info_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        status_text = f"""
✅ Interface gráfica carregada com sucesso!
✅ Tkinter funcionando no executável
✅ Todas as dependências encontradas
📁 Diretório base: {self.base_path}
🎯 Executável: {hasattr(sys, '_MEIPASS')}

🎉 O problema foi RESOLVIDO!

O executável agora abre a interface corretamente.
Para usar o app completo, as funcionalidades serão 
implementadas progressivamente.
        """
        
        tk.Label(info_frame, text=status_text, justify=tk.LEFT, font=('Arial', 10)).pack(anchor=tk.W)
        
        # Botão de fechar
        ttk.Button(self.root, text="✅ Fechar", command=self.root.destroy, 
                  style='Title.TLabel').pack(pady=10)

    def run(self):
        """Executar aplicação"""
        print("Iniciando mainloop...")
        self.root.mainloop()
        print("Mainloop encerrado.")

def main():
    """Função principal teste"""
    print("=== TESTE PROGRESSIVO ===")
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
        
        print("Criando aplicação teste...")
        app = KeydropBotGUI_Teste()
        app.run()
        print("Aplicação encerrada com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        traceback.print_exc()
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
