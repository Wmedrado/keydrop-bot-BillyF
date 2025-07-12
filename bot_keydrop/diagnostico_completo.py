#!/usr/bin/env python3
"""
Diagnóstico completo do executável - Versão de debug extremo
"""

import tkinter as tk
from tkinter import messagebox
import sys
import os
import time
import traceback
from pathlib import Path

def criar_log_debug():
    """Criar sistema de log robusto"""
    try:
        # Determinar diretório base
        if hasattr(sys, '_MEIPASS'):
            base_path = Path(sys.executable).parent
        else:
            base_path = Path(__file__).parent
        
        # Criar pasta de logs
        logs_dir = base_path / "logs"
        logs_dir.mkdir(exist_ok=True)
        
        # Arquivo de log único
        log_file = logs_dir / f"diagnostico_{time.strftime('%Y%m%d_%H%M%S')}.log"
        
        def log(msg):
            try:
                timestamp = time.strftime("%H:%M:%S")
                log_msg = f"[{timestamp}] {msg}\n"
                with open(log_file, 'a', encoding='utf-8') as f:
                    f.write(log_msg)
                    f.flush()
                print(log_msg.strip())  # Também no console
            except Exception as e:
                print(f"ERRO NO LOG: {e}")
        
        return log, log_file
    except Exception:
        def dummy_log(msg):
            print(f"[LOG] {msg}")
        return dummy_log, None

def teste_interface_minima():
    """Teste com interface mínima possível"""
    log, log_file = criar_log_debug()
    
    try:
        log("=== INÍCIO DIAGNÓSTICO COMPLETO ===")
        log(f"Python: {sys.version}")
        log(f"Plataforma: {sys.platform}")
        log(f"Executável: {hasattr(sys, '_MEIPASS')}")
        log(f"Diretório atual: {os.getcwd()}")
        
        # Teste 1: Verificar imports
        log("TESTE 1: Verificando imports...")
        try:
            import tkinter as tk_test  # noqa: F401
            log("✅ tkinter importado")
        except Exception as e:
            log(f"❌ Erro tkinter: {e}")
            return
        
        try:
            import psutil  # noqa: F401
            log("✅ psutil importado")
        except Exception as e:
            log(f"❌ Erro psutil: {e}")
        
        # Teste 2: Criar janela super simples
        log("TESTE 2: Criando janela mínima...")
        
        root = tk.Tk()
        log("✅ tk.Tk() criado")
        
        # Configurações básicas
        root.title("TESTE DIAGNÓSTICO")
        root.geometry("300x200")
        log("✅ Configurações básicas aplicadas")
        
        # Forçar aparecer com múltiplas técnicas
        log("TESTE 3: Forçando janela aparecer...")
        
        # Técnica 1: lift e focus
        root.lift()
        root.focus_force()
        log("✅ lift() e focus_force() aplicados")
        
        # Técnica 2: topmost temporário
        root.attributes('-topmost', True)
        root.update()
        root.after(500, lambda: root.attributes('-topmost', False))
        log("✅ topmost temporário aplicado")
        
        # Técnica 3: centralizar
        try:
            root.eval('tk::PlaceWindow . center')
            log("✅ Janela centralizada")
        except Exception as e:
            log(f"⚠️  Erro ao centralizar: {e}")
        
        # Técnica 4: posição manual
        x = (root.winfo_screenwidth() // 2) - 150
        y = (root.winfo_screenheight() // 2) - 100
        root.geometry(f"300x200+{x}+{y}")
        log(f"✅ Posição manual: {x},{y}")
        
        # Técnica 5: iconify/deiconify
        root.iconify()
        root.update()
        root.deiconify()
        log("✅ iconify/deiconify aplicado")
        
        # Conteúdo da janela
        label = tk.Label(root, text="🔍 DIAGNÓSTICO\n\nSe você vê esta janela,\no problema não é do tkinter!", 
                        font=('Arial', 12), justify=tk.CENTER, bg='yellow', pady=20)
        label.pack(expand=True, fill='both')
        log("✅ Label adicionado")
        
        # Botão de teste
        def fechar_teste():
            log("✅ Botão clicado - Interface funcionando!")
            root.quit()
        
        btn = tk.Button(root, text="INTERFACE FUNCIONA!", command=fechar_teste, 
                       font=('Arial', 14, 'bold'), bg='green', fg='white', pady=10)
        btn.pack(pady=10)
        log("✅ Botão adicionado")
        
        # Atualizar múltiplas vezes
        for i in range(5):
            root.update()
            time.sleep(0.1)
        log("✅ Updates múltiplos aplicados")
        
        # Callback para quando janela aparecer
        def on_map(event):
            log("✅ JANELA MAPEADA - VISÍVEL!")
        
        root.bind('<Map>', on_map)
        
        # Timer de timeout
        def timeout():
            log("⏰ TIMEOUT - Fechando por timeout")
            root.quit()
        
        root.after(10000, timeout)  # 10 segundos
        
        log("TESTE 4: Iniciando mainloop...")
        root.mainloop()
        log("✅ mainloop encerrado")
        
        # Resultado final
        if log_file:
            log(f"📄 Log completo salvo em: {log_file}")
            
            # Mostrar messagebox com resultado
            try:
                messagebox.showinfo("Diagnóstico Completo", 
                                  f"Teste concluído!\n\nLog salvo em:\n{log_file}\n\nVerifique se a janela amarela apareceu.")
            except Exception as e:
                log(f"⚠️  Erro ao mostrar messagebox: {e}")
        
    except Exception as e:
        error_msg = f"ERRO FATAL: {e}"
        stack_trace = traceback.format_exc()
        
        # Registrar no log ANTES de tentar a messagebox
        log("=== ERRO FATAL ===")
        log(f"❌ {error_msg}")
        log(f"Stack trace:\n{stack_trace}")
        
        try:
            messagebox.showerror("Erro no Diagnóstico", 
                                f"{error_msg}\n\nLog salvo em: {log_file}")
        except Exception:
            # Se a messagebox falhar, pelo menos mostrar no console
            print("ERRO FATAL (messagebox falhou):")
            print(f"❌ {error_msg}")

if __name__ == "__main__":
    teste_interface_minima()
