#!/usr/bin/env python3
"""
Sistema de Atualização Automática - KeyDrop Bot (Versão Melhorada)
Busca atualizações no GitHub usando token de autenticação com melhor tratamento de erros
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
from tkinter import ttk
import time

class ImprovedUpdateManager:
    """Gerenciador de atualizações via GitHub com melhor tratamento de erros"""
    
    def __init__(self, repo_owner="wmedrado", repo_name="bot-keydrop", current_version="2.0.7"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.github_api = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.update_in_progress = False
        
        # Token de acesso pessoal do GitHub
        self.github_token = self.get_github_token()
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "KeyDrop-Bot-Updater"
        } if self.github_token else {}
        
    def get_github_token(self):
        """Obtém o token do GitHub de diferentes fontes"""
        # Método 1: Variável de ambiente
        token = os.getenv('GITHUB_TOKEN')
        if token:
            print("✅ Token do GitHub encontrado via variável de ambiente")
            return token
            
        # Método 2: Arquivo local - múltiplos caminhos para compatibilidade
        possible_paths = [
            # Diretório raiz do projeto (quando executado como script)
            Path(__file__).parent.parent / 'github_token.txt',
            
            # Diretório atual (quando executado como executável)
            Path.cwd() / 'github_token.txt',
            
            # Diretório do executável (para PyInstaller)
            Path(sys.executable).parent / 'github_token.txt',
            
            # Diretório temporário do PyInstaller
            Path(getattr(sys, '_MEIPASS', Path.cwd())) / 'github_token.txt',
            
            # Caminhos relativos
            Path('./github_token.txt'),
            Path('../github_token.txt'),
            
            # Pasta startup (caso seja executado de lá)
            Path('./startup/github_token.txt'),
            Path('../startup/github_token.txt')
        ]
        
        for token_file in possible_paths:
            if token_file.exists():
                try:
                    token = token_file.read_text(encoding='utf-8').strip()
                    if token and len(token) > 10:  # Validação básica
                        print(f"✅ Token do GitHub encontrado em: {token_file}")
                        return token
                except Exception as e:
                    print(f"❌ Erro ao ler arquivo de token {token_file}: {e}")
                    continue
                
        # Método 3: Arquivo de configuração
        config_paths = [
            Path(__file__).parent.parent / 'bot_config.json',
            Path.cwd() / 'bot_config.json',
            Path('./bot_config.json')
        ]
        
        for config_file in config_paths:
            if config_file.exists():
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                        token = config.get('github_token', '')
                        if token:
                            print("✅ Token do GitHub encontrado no bot_config.json")
                            return token
                except Exception as e:
                    print(f"❌ Erro ao ler configuração {config_file}: {e}")
                    continue
        
        print("❌ Token do GitHub não encontrado!")
        return None
        
    def check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        if not self.github_token:
            return {
                "available": False,
                "error": "Token do GitHub não configurado. Verifique o arquivo github_token.txt"
            }
            
        try:
            print("🔍 Verificando atualizações...")
            print(f"📂 Repositório: {self.repo_owner}/{self.repo_name}")
            
            # Buscar última release no GitHub
            url = f"{self.github_api}/releases/latest"
            print(f"🌐 URL da API: {url}")
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=15
            )
            
            print(f"📡 Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data.get("tag_name", "").replace("v", "")
                
                print(f"📋 Versão atual: {self.current_version}")
                print(f"📋 Versão disponível: {latest_version}")
                
                if self.is_newer_version(latest_version, self.current_version):
                    # Buscar asset do ZIP (múltiplos formatos)
                    assets = release_data.get("assets", [])
                    zip_asset = None
                    
                    # Prioridade: KeyDrop_Bot_v*.zip, depois qualquer .zip
                    for asset in assets:
                        name = asset.get("name", "")
                        if name.startswith("KeyDrop_Bot_v") and name.endswith(".zip"):
                            zip_asset = asset
                            break
                    
                    if not zip_asset:
                        for asset in assets:
                            if asset.get("name", "").endswith(".zip"):
                                zip_asset = asset
                                break
                    
                    return {
                        "available": True,
                        "version": latest_version,
                        "changelog": release_data.get("body", "Sem changelog disponível"),
                        "release_date": release_data.get("published_at"),
                        "download_url": zip_asset.get("browser_download_url") if zip_asset else None,
                        "asset_name": zip_asset.get("name") if zip_asset else None,
                        "asset_size": zip_asset.get("size", 0) if zip_asset else 0
                    }
                else:
                    return {
                        "available": False,
                        "message": f"Versão atual ({self.current_version}) está atualizada"
                    }
            elif response.status_code == 401:
                return {
                    "available": False,
                    "error": "Token do GitHub inválido ou expirado"
                }
            elif response.status_code == 404:
                return {
                    "available": False,
                    "error": "Repositório não encontrado ou sem permissão"
                }
            else:
                return {
                    "available": False,
                    "error": f"Erro HTTP {response.status_code}: {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {
                "available": False,
                "error": f"Erro de conexão: {str(e)}"
            }
        except Exception as e:
            return {
                "available": False,
                "error": f"Erro inesperado: {str(e)}"
            }
    
    def is_newer_version(self, version1, version2):
        """Compara versões (version1 > version2)"""
        try:
            v1_parts = [int(x) for x in version1.split('.')]
            v2_parts = [int(x) for x in version2.split('.')]
            
            # Preencher com zeros se necessário
            max_len = max(len(v1_parts), len(v2_parts))
            v1_parts.extend([0] * (max_len - len(v1_parts)))
            v2_parts.extend([0] * (max_len - len(v2_parts)))
            
            return v1_parts > v2_parts
        except:
            return False
    
    def download_update(self, update_info, progress_callback=None):
        """Baixa a atualização com melhor tratamento de erros"""
        if not update_info.get("available"):
            return {"success": False, "message": "Nenhuma atualização disponível"}
            
        download_url = update_info.get("download_url")
        if not download_url:
            return {"success": False, "message": "URL de download não encontrada"}
            
        try:
            self.update_in_progress = True
            
            # Criar diretório temporário
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, "update.zip")
            
            print(f"📥 Baixando atualização de {download_url}...")
            
            # Download do arquivo com timeout aumentado
            response = requests.get(
                download_url,
                headers=self.headers,
                stream=True,
                timeout=60
            )
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            downloaded = 0
            
            print(f"📦 Tamanho do arquivo: {total_size / (1024*1024):.2f} MB")
            
            with open(zip_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if progress_callback and total_size > 0:
                            progress = (downloaded / total_size) * 100
                            progress_callback(progress)
            
            # Verificar se o arquivo foi baixado completamente
            if os.path.getsize(zip_path) == 0:
                return {"success": False, "message": "Arquivo baixado está vazio"}
            
            # Verificar se é um arquivo ZIP válido
            try:
                with zipfile.ZipFile(zip_path, 'r') as test_zip:
                    test_zip.testzip()
            except zipfile.BadZipFile:
                return {"success": False, "message": "Arquivo ZIP corrompido"}
            
            return {"success": True, "zip_path": zip_path, "temp_dir": temp_dir}
            
        except requests.exceptions.RequestException as e:
            self.update_in_progress = False
            return {"success": False, "message": f"Erro no download: {e}"}
        except Exception as e:
            self.update_in_progress = False
            return {"success": False, "message": f"Erro inesperado no download: {e}"}
    
    def apply_update(self, zip_path, temp_dir):
        """Aplica a atualização com backup automático"""
        try:
            print("📦 Extraindo atualização...")
            
            # Extrair ZIP
            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Encontrar diretório do projeto extraído
            extracted_items = os.listdir(extract_dir)
            if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_dir, extracted_items[0])):
                source_dir = os.path.join(extract_dir, extracted_items[0])
            else:
                source_dir = extract_dir
            
            # Verificar se contém arquivos essenciais
            essential_files = ["keydrop_bot.py", "modern_gui.py", "requirements.txt"]
            missing_files = []
            for file in essential_files:
                if not os.path.exists(os.path.join(source_dir, file)):
                    missing_files.append(file)
            
            if missing_files:
                return {
                    "success": False,
                    "message": f"Arquivos essenciais não encontrados: {', '.join(missing_files)}"
                }
            
            # Criar backup dos arquivos atuais
            backup_dir = f"backup/update_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            print("💾 Criando backup...")
            
            # Arquivos importantes para backup
            important_files = [
                "bot_config.json",
                "profiles/",
                "data/",
                "logs/",
                "github_token.txt"
            ]
            
            for item in important_files:
                if os.path.exists(item):
                    try:
                        if os.path.isdir(item):
                            shutil.copytree(item, os.path.join(backup_dir, item), dirs_exist_ok=True)
                        else:
                            shutil.copy2(item, backup_dir)
                    except Exception as e:
                        print(f"⚠️ Erro ao fazer backup de {item}: {e}")
            
            print("🔄 Aplicando atualização...")
            
            # Aplicar atualização (exceto arquivos de configuração)
            exclude_items = {
                "bot_config.json",
                "profiles",
                "data", 
                "logs",
                "backup",
                ".git",
                "__pycache__",
                "github_token.txt",
                ".gitignore"
            }
            
            success_count = 0
            error_count = 0
            
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
                        success_count += 1
                    except Exception as e:
                        print(f"❌ Erro ao atualizar {item}: {e}")
                        error_count += 1
            
            # Atualizar versão no arquivo de configuração
            self.update_version_file(self.current_version)
            
            # Limpeza
            try:
                shutil.rmtree(temp_dir)
            except:
                pass
            
            self.update_in_progress = False
            
            if error_count == 0:
                print("✅ Atualização aplicada com sucesso!")
                return {
                    "success": True,
                    "backup_dir": backup_dir,
                    "updated_files": success_count,
                    "message": f"Atualização concluída! {success_count} arquivos atualizados."
                }
            else:
                return {
                    "success": False,
                    "message": f"Atualização parcial: {success_count} sucessos, {error_count} erros",
                    "backup_dir": backup_dir
                }
            
        except Exception as e:
            self.update_in_progress = False
            return {"success": False, "message": f"Erro ao aplicar atualização: {e}"}
    
    def update_version_file(self, new_version):
        """Atualiza o arquivo de versão"""
        try:
            version_file = Path("version.json")
            if version_file.exists():
                with open(version_file, 'r', encoding='utf-8') as f:
                    version_data = json.load(f)
                
                version_data["version"] = new_version
                version_data["updated_at"] = datetime.now().isoformat()
                
                with open(version_file, 'w', encoding='utf-8') as f:
                    json.dump(version_data, f, indent=4, ensure_ascii=False)
                
                print(f"✅ Versão atualizada para {new_version}")
        except Exception as e:
            print(f"⚠️ Erro ao atualizar arquivo de versão: {e}")
    
    def show_update_dialog(self, parent=None):
        """Mostra diálogo de atualização melhorado"""
        try:
            update_info = self.check_for_updates()
            
            if update_info.get("error"):
                messagebox.showerror(
                    "Erro",
                    f"❌ Erro ao verificar atualizações:\n{update_info['error']}"
                )
                return
            
            if not update_info["available"]:
                messagebox.showinfo(
                    "Atualizações",
                    f"✅ {update_info.get('message', 'Nenhuma atualização disponível')}"
                )
                return
            
            # Verificar se há URL de download
            if not update_info.get("download_url"):
                messagebox.showerror(
                    "Erro",
                    "❌ Nenhum arquivo de atualização disponível para download"
                )
                return
            
            # Criar janela de atualização
            update_window = tk.Toplevel(parent)
            update_window.title("🔄 Atualização Disponível")
            update_window.geometry("600x500")
            update_window.resizable(False, False)
            update_window.configure(bg="#2C2F33")
            
            # Centralizar janela
            if parent:
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
            
            # Informações do arquivo
            if update_info.get("asset_name"):
                tk.Label(
                    info_frame,
                    text=f"Arquivo: {update_info['asset_name']}",
                    font=("Arial", 9),
                    fg="#99AAB5",
                    bg="#2C2F33"
                ).pack(anchor="w")
            
            if update_info.get("asset_size"):
                size_mb = update_info["asset_size"] / (1024 * 1024)
                tk.Label(
                    info_frame,
                    text=f"Tamanho: {size_mb:.2f} MB",
                    font=("Arial", 9),
                    fg="#99AAB5",
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
                height=10,
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
            
            progress_var = tk.DoubleVar()
            progress_bar = ttk.Progressbar(
                progress_frame,
                variable=progress_var,
                maximum=100,
                length=300
            )
            progress_bar.pack(fill="x", pady=5)
            
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
                        progress_var.set(percent)
                        progress_label.config(text=f"📥 Download: {percent:.1f}%")
                        update_window.update()
                    
                    # Download
                    progress_label.config(text="📥 Iniciando download...")
                    update_window.update()
                    
                    download_result = self.download_update(update_info, progress_callback)
                    
                    if download_result["success"]:
                        progress_var.set(100)
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
                                f"✅ Atualização aplicada com sucesso!\n\n"
                                f"{apply_result.get('message', '')}\n\n"
                                "Reinicie o programa para usar a nova versão.\n\n"
                                f"Backup criado em: {apply_result.get('backup_dir', 'N/A')}"
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
    updater = ImprovedUpdateManager()
    
    # Criar janela temporária se não houver parent
    root = tk.Tk()
    root.withdraw()
    
    updater.show_update_dialog(root)
    root.mainloop()

if __name__ == "__main__":
    check_and_update()
