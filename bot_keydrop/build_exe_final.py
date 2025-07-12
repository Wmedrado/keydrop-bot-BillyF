#!/usr/bin/env python3
"""
Script para gerar executável final do Keydrop Bot v3.0.0
"""
import PyInstaller.__main__

def build_executable():
    """Gerar executável otimizado"""
    try:
        print("🚀 Gerando executável Keydrop Bot v3.0.0...")
        
        # Argumentos do PyInstaller
        args = [
            r'C:\Users\William\Desktop\Projeto do zero\bot_keydrop\keydrop_bot_desktop.py',
            '--onefile',
            '--windowed',
            '--name=KeydropBot_v3.0.0_FINAL',
            '--icon=C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop\\bot-icone.ico',
            '--distpath=C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop',
            '--workpath=build_temp',
            '--clean',
            '--add-data=C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop\\bot-icone.ico;.',
            '--hidden-import=tkinter',
            '--hidden-import=tkinter.ttk',
            '--hidden-import=tkinter.messagebox',
            '--hidden-import=tkinter.scrolledtext',
            '--hidden-import=tkinter.filedialog',
            '--hidden-import=threading',
            '--hidden-import=subprocess',
            '--hidden-import=json',
            '--hidden-import=requests',
            '--hidden-import=psutil',
            '--hidden-import=time',
            '--hidden-import=logging',
            '--hidden-import=traceback',
            '--hidden-import=datetime',
            '--hidden-import=pathlib',
            '--exclude-module=selenium',
            '--exclude-module=webdriver_manager',
            '--noconsole'
        ]
        
        # Executar PyInstaller
        PyInstaller.__main__.run(args)
        
        print("✅ Executável gerado com sucesso!")
        print("📁 Local: KeydropBot_v3.0.0_FINAL.exe")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao gerar executável: {e}")
        return False

if __name__ == "__main__":
    build_executable()
