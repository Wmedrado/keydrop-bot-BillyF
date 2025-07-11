#!/usr/bin/env python3
"""
Sistema de Atualização Automática - KeyDrop Bot
Busca atualizações no GitHub e aplica automaticamente
"""
import requests
import json
import os
import zipfile
import shutil
import subprocess
import sys
from pathlib import Path
from datetime import datetime
import tempfile
import threading
from tkinter import messagebox
import tkinter as tk

class UpdateManager:
    """Gerenciador de atualizações via GitHub"""
    
    def __init__(self, repo_owner="seu-usuario", repo_name="keydrop-bot", current_version="2.0.0"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.github_api = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.download_url = f"https://github.com/{repo_owner}/{repo_name}"
        self.update_in_progress = False
        
    def check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        try:
            print("🔍 Verificando atualizações...")
            
            # Buscar última release no GitHub
            response = requests.get(f"{self.github_api}/releases/latest", timeout=10)
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data.get("tag_name", "").replace("v", "")
                
                if self.is_newer_version(latest_version, self.current_version):
                    return {
                        "available": True,
                        "version": latest_version,
                        "url": release_data.get("zipball_url"),
                        "changelog": release_data.get("body", "Sem changelog disponível"),
                        "release_date": release_data.get("published_at"),
                        "download_url": release_data.get("assets", [{}])[0].get("browser_download_url") if release_data.get("assets") else None
                    }
                else:
                    return {"available": False, "message": "Você já possui a versão mais recente"}
            
            elif response.status_code == 404:
                return {"available": False, "message": "Repositório não encontrado"}
            else:
                return {"available": False, "message": f"Erro ao verificar atualizações: {response.status_code}"}
                
        except requests.exceptions.RequestException as e:
            return {"available": False, "message": f"Erro de conexão: {e}"}
        except Exception as e:
            return {"available": False, "message": f"Erro inesperado: {e}"}
    
    def is_newer_version(self, latest, current):
        """Compara versões para verificar se há atualização"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Preenche com zeros se necessário
            max_len = max(len(latest_parts), len(current_parts))
            latest_parts.extend([0] * (max_len - len(latest_parts)))
            current_parts.extend([0] * (max_len - len(current_parts)))
            
            return latest_parts > current_parts
        except:
            return False
    
    def download_update(self, update_info, progress_callback=None):
        """Baixa a atualização"""
        try:
            self.update_in_progress = True
            
            # URL de download
            download_url = update_info.get("download_url") or update_info.get("url")
            if not download_url:
                return {"success": False, "message": "URL de download não encontrada"}
            
            # Criar diretório temporário
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")
            
            print(f"📥 Baixando atualização de {download_url}...")
            
            # Download do arquivo
            response = requests.get(download_url, stream=True, timeout=30)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            return {"success": True, "zip_path": zip_path, "temp_dir": temp_dir}
            
        except Exception as e:
            self.update_in_progress = False
            return {"success": False, "message": f"Erro no download: {e}"}
    
    def apply_update(self, zip_path, temp_dir):
        """Aplica a atualização"""
        try:
            print("📦 Extraindo atualização...")
            
            # Extrair ZIP
            extract_dir = os.path.join(temp_dir, "extracted")
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Encontrar diretório do projeto extraído
            extracted_items = os.listdir(extract_dir)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
                source_dir = os.path.join(extract_dir, extracted_items[0])
            else:
                source_dir = extract_dir
            
            # Backup dos arquivos atuais
            backup_dir = f"backup/update_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            print("💾 Criando backup...")
            
            # Arquivos importantes para backup
            important_files = [
                "bot_config.json",
                "profiles/",
                "data/",
                "logs/"
            ]
            
            for item in important_files:
                if os.path.exists(item):
                    if os.path.isdir(item):
                        shutil.copytree(item, os.path.join(backup_dir, item), dirs_exist_ok=True)
                    else:
                        shutil.copy2(item, backup_dir)
            
            print("🔄 Aplicando atualização...")
            
            # Aplicar atualização (exceto arquivos de configuração)
            exclude_items = {
                "bot_config.json",
                "profiles",
                "data", 
                "logs",
                "backup",
                ".git",
                "__pycache__"
            }
            
            for item in os.listdir(source_dir):
                if item not in exclude_items:
                    source_path = os.path.join(source_dir, item)
                    dest_path = item
                    
                    try:
                        if os.path.isdir(source_path):
                            if os.path.exists(dest_path):
                                shutil.rmtree(dest_path)
                            shutil.copytree(source_path, dest_path)
                        else:
                            shutil.copy2(source_path, dest_path)
                        print(f"✅ Atualizado: {item}")
                    except Exception as e:
                        print(f"⚠️ Erro ao atualizar {item}: {e}")
            
            # Limpeza
            shutil.rmtree(temp_dir)
            self.update_in_progress = False
            
            print("✅ Atualização aplicada com sucesso!")
            return {"success": True, "backup_dir": backup_dir}
            
        except Exception as e:
            self.update_in_progress = False
            return {"success": False, "message": f"Erro ao aplicar atualização: {e}"}
    
    def show_update_dialog(self, parent=None):
        """Mostra diálogo de atualização"""
        try:
            update_info = self.check_for_updates()
            
            if not update_info["available"]:
                messagebox.showinfo(
                    "Atualizações",
                    f"✅ {update_info.get('message', 'Nenhuma atualização disponível')}"
                )
                return
            
            # Criar janela de atualização
            update_window = tk.Toplevel(parent)
            update_window.title("🔄 Atualização Disponível")
            update_window.geometry("500x400")
            update_window.resizable(False, False)
            update_window.configure(bg="#2C2F33")
            
            # Centralizar janela
            update_window.transient(parent)
            update_window.grab_set()
            
            # Título
            title_label = tk.Label(
                update_window,
                text="🔄 Atualização Disponível",
                font=("Arial", 16, "bold"),
                fg="white",
                bg="#2C2F33"
            )
            title_label.pack(pady=10)
            
            # Informações da versão
            info_frame = tk.Frame(update_window, bg="#2C2F33")
            info_frame.pack(fill="x", padx=20, pady=10)
            
            tk.Label(
                info_frame,
                text=f"Versão atual: {self.current_version}",
                font=("Arial", 10),
                fg="#99AAB5",
                bg="#2C2F33"
            ).pack(anchor="w")
            
            tk.Label(
                info_frame,
                text=f"Nova versão: {update_info['version']}",
                font=("Arial", 12, "bold"),
                fg="#43B581",
                bg="#2C2F33"
            ).pack(anchor="w")
            
            # Changelog
            changelog_label = tk.Label(
                update_window,
                text="📋 Novidades:",
                font=("Arial", 12, "bold"),
                fg="white",
                bg="#2C2F33"
            )
            changelog_label.pack(anchor="w", padx=20, pady=(10, 5))
            
            changelog_text = tk.Text(
                update_window,
                height=8,
                bg="#23272A",
                fg="white",
                font=("Arial", 9),
                wrap="word",
                padx=10,
                pady=10
            )
            changelog_text.pack(fill="both", expand=True, padx=20, pady=(0, 10))
            changelog_text.insert("1.0", update_info.get('changelog', 'Sem changelog disponível'))
            changelog_text.config(state="disabled")
            
            # Barra de progresso
            progress_frame = tk.Frame(update_window, bg="#2C2F33")
            progress_frame.pack(fill="x", padx=20, pady=5)
            
            progress_label = tk.Label(
                progress_frame,
                text="",
                font=("Arial", 9),
                fg="#99AAB5",
                bg="#2C2F33"
            )
            progress_label.pack()
            
            # Botões
            button_frame = tk.Frame(update_window, bg="#2C2F33")
            button_frame.pack(fill="x", padx=20, pady=10)
            
            def start_update():
                """Inicia o processo de atualização"""
                update_btn.config(state="disabled", text="⏳ Atualizando...")
                cancel_btn.config(state="disabled")
                
                def update_thread():
                    def progress_callback(percent):
                        progress_label.config(text=f"📥 Download: {percent:.1f}%")
                        update_window.update()
                    
                    # Download
                    download_result = self.download_update(update_info, progress_callback)
                    
                    if download_result["success"]:
                        progress_label.config(text="📦 Aplicando atualização...")
                        update_window.update()
                        
                        # Aplicar atualização
                        apply_result = self.apply_update(
                            download_result["zip_path"], 
                            download_result["temp_dir"]
                        )
                        
                        if apply_result["success"]:
                            progress_label.config(text="✅ Atualização concluída!")
                            messagebox.showinfo(
                                "Sucesso",
                                "✅ Atualização aplicada com sucesso!\n\n"
                                "Reinicie o programa para usar a nova versão.\n\n"
                                f"Backup criado em: {apply_result['backup_dir']}"
                            )
                            update_window.destroy()
                        else:
                            progress_label.config(text="❌ Erro na atualização")
                            messagebox.showerror(
                                "Erro",
                                f"❌ Erro ao aplicar atualização:\n{apply_result['message']}"
                            )
                            update_btn.config(state="normal", text="🔄 Atualizar")
                            cancel_btn.config(state="normal")
                    else:
                        progress_label.config(text="❌ Erro no download")
                        messagebox.showerror(
                            "Erro",
                            f"❌ Erro no download:\n{download_result['message']}"
                        )
                        update_btn.config(state="normal", text="🔄 Atualizar")
                        cancel_btn.config(state="normal")
                
                threading.Thread(target=update_thread, daemon=True).start()
            
            update_btn = tk.Button(
                button_frame,
                text="🔄 Atualizar",
                command=start_update,
                bg="#43B581",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=20,
                pady=8,
                cursor="hand2"
            )
            update_btn.pack(side="left", padx=(0, 10))
            
            cancel_btn = tk.Button(
                button_frame,
                text="❌ Cancelar",
                command=update_window.destroy,
                bg="#F04747",
                fg="white",
                font=("Arial", 10, "bold"),
                padx=20,
                pady=8,
                cursor="hand2"
            )
            cancel_btn.pack(side="right")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao verificar atualizações: {e}")

def check_and_update():
    """Função standalone para verificar atualizações"""
    updater = UpdateManager()
    
    # Criar janela temporária se não houver parent
    root = tk.Tk()
    root.withdraw()
    
    updater.show_update_dialog(root)
    root.mainloop()

if __name__ == "__main__":
    check_and_update()
