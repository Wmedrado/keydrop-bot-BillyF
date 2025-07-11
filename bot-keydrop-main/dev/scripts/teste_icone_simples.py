#!/usr/bin/env python3
"""
Teste do Ícone - Versão Simplificada
Testa se o ícone está carregando corretamente
"""

import tkinter as tk
import customtkinter as ctk
import os
import sys

def testar_icone_interface():
    """Testa o ícone na interface de forma simplificada"""
    print("🎨 Testando ícone na interface...")
    
    # Configurar tema
    ctk.set_appearance_mode("dark")
    
    # Criar janela
    root = ctk.CTk()
    root.title("🔑 Teste de Ícone - KeyDrop Bot")
    root.geometry("400x300")
    
    # Configurar ícone
    def configurar_icone():
        try:
            # Lista de possíveis localizações do ícone
            possiveis_caminhos = [
                # Mesmo diretório do script/executável
                os.path.join(os.path.dirname(__file__), 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), 'bot-icone.png'),
                
                # Diretório atual
                os.path.join(os.getcwd(), 'bot-icone.ico'),
                os.path.join(os.getcwd(), 'bot-icone.png'),
                
                # Diretório pai (3 níveis acima)
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'bot-icone.ico'),
                os.path.join(os.path.dirname(__file__), '..', '..', '..', 'bot-icone.png'),
                
                # Para executáveis PyInstaller
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.ico'),
                os.path.join(sys._MEIPASS if hasattr(sys, '_MEIPASS') else '.', 'bot-icone.png'),
            ]
            
            print("🔍 Procurando ícone nos seguintes locais:")
            for caminho in possiveis_caminhos:
                existe = os.path.exists(caminho)
                print(f"  {'✅' if existe else '❌'} {caminho}")
                
                if existe:
                    try:
                        if caminho.endswith('.ico'):
                            root.iconbitmap(caminho)
                            print(f"✅ Ícone ICO carregado de: {caminho}")
                            return True
                        elif caminho.endswith('.png'):
                            icon_image = tk.PhotoImage(file=caminho)
                            root.iconphoto(True, icon_image)
                            print(f"✅ Ícone PNG carregado de: {caminho}")
                            return True
                    except Exception as e:
                        print(f"⚠️ Erro ao carregar ícone de {caminho}: {e}")
                        continue
            
            print("⚠️ Nenhum ícone encontrado, usando ícone padrão")
            return False
            
        except Exception as e:
            print(f"❌ Erro na configuração do ícone: {e}")
            return False
    
    # Configurar ícone
    icone_carregado = configurar_icone()
    
    # Criar interface de teste
    label = ctk.CTkLabel(
        root,
        text=f"🎨 Teste de Ícone\n\n{'✅ Ícone carregado!' if icone_carregado else '❌ Ícone não carregado'}\n\nVerifique a barra de título",
        font=ctk.CTkFont(size=16),
        justify="center"
    )
    label.pack(expand=True)
    
    # Botão para fechar
    btn_fechar = ctk.CTkButton(
        root,
        text="✅ Fechar",
        command=root.destroy,
        width=120
    )
    btn_fechar.pack(pady=20)
    
    # Mostrar janela
    root.mainloop()
    
    return icone_carregado

if __name__ == "__main__":
    print("🚀 TESTE DE ÍCONE")
    print("=" * 40)
    
    # Informações do ambiente
    print(f"📁 Diretório do script: {os.path.dirname(__file__)}")
    print(f"📁 Diretório atual: {os.getcwd()}")
    print(f"🐍 Executável PyInstaller: {hasattr(sys, '_MEIPASS')}")
    if hasattr(sys, '_MEIPASS'):
        print(f"📦 MEIPASS: {sys._MEIPASS}")
    print()
    
    # Testar ícone
    sucesso = testar_icone_interface()
    
    print("\n📊 RESULTADO:")
    print(f"{'✅ SUCESSO' if sucesso else '❌ FALHA'} - Ícone {'carregado' if sucesso else 'não carregado'}")
