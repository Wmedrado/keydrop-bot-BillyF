#!/usr/bin/env python3
"""
Conversor de Ícone PNG para ICO
Converte bot-icone.png para bot-icone.ico
"""

import os
import sys
from pathlib import Path

# Adicionar o diretório raiz ao sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def converter_icone():
    """Converte o ícone PNG para ICO"""
    print("🔄 CONVERTENDO ÍCONE PNG PARA ICO")
    print("=" * 50)
    
    try:
        from PIL import Image
        print("✅ PIL/Pillow disponível")
    except ImportError:
        print("❌ PIL/Pillow não disponível")
        print("🔧 Instalando Pillow...")
        
        import subprocess
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"], 
                         check=True, capture_output=True, text=True)
            print("✅ Pillow instalado com sucesso!")
            from PIL import Image
        except Exception as e:
            print(f"❌ Erro ao instalar Pillow: {e}")
            return False
    
    # Caminhos dos arquivos
    png_path = project_root / 'bot-icone.png'
    ico_path = project_root / 'bot-icone.ico'
    
    print(f"📄 Arquivo PNG: {png_path}")
    print(f"📄 Arquivo ICO: {ico_path}")
    
    if not png_path.exists():
        print("❌ Arquivo PNG não encontrado!")
        return False
    
    try:
        # Abrir imagem PNG
        with Image.open(png_path) as img:
            print(f"🖼️ Imagem original: {img.size} pixels, modo: {img.mode}")
            
            # Converter para RGBA se necessário
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Redimensionar para tamanhos padrão de ícone
            icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
            
            # Salvar como ICO
            img.save(ico_path, format='ICO', sizes=icon_sizes)
            
            print(f"✅ Ícone convertido com sucesso!")
            print(f"📏 Tamanho do arquivo ICO: {ico_path.stat().st_size} bytes")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro na conversão: {e}")
        return False

def testar_icone_ico():
    """Testa o ícone ICO"""
    print("\n🎨 TESTANDO ÍCONE ICO")
    print("=" * 50)
    
    import tkinter as tk
    
    ico_path = project_root / 'bot-icone.ico'
    
    if not ico_path.exists():
        print("❌ Arquivo ICO não encontrado!")
        return False
    
    try:
        # Criar janela de teste
        root = tk.Tk()
        root.title("Teste de Ícone ICO - KeyDrop Bot")
        root.geometry("400x300")
        
        # Carregar ícone
        root.iconbitmap(str(ico_path))
        print("✅ Ícone ICO carregado com sucesso!")
        
        # Label de teste
        label = tk.Label(
            root,
            text="🎨 Teste de Ícone ICO\n\nVerifique se o ícone aparece\nna barra de título",
            font=("Arial", 14)
        )
        label.pack(expand=True)
        
        # Mostrar janela por 3 segundos
        root.after(3000, root.destroy)
        root.mainloop()
        
        return True
        
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

if __name__ == "__main__":
    print("🚀 INICIANDO CONVERSÃO DE ÍCONE\n")
    
    # Converter PNG para ICO
    sucesso_conversao = converter_icone()
    
    if sucesso_conversao:
        # Testar ícone ICO
        sucesso_teste = testar_icone_ico()
        
        print("\n📊 RESULTADO:")
        print(f"✅ Conversão PNG → ICO: {'OK' if sucesso_conversao else 'ERRO'}")
        print(f"✅ Teste do ícone ICO: {'OK' if sucesso_teste else 'ERRO'}")
        
        if sucesso_conversao and sucesso_teste:
            print("\n🎉 Ícone convertido e testado com sucesso!")
            print("📝 Agora você pode usar 'bot-icone.ico' nas aplicações")
        else:
            print("\n❌ Houve problemas na conversão ou teste")
    else:
        print("\n❌ Falha na conversão do ícone")
