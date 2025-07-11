#!/usr/bin/env python3
"""
Sistema de Atualização Automática - KeyDrop Bot (Repositório Privado)
Busca atualizações no GitHub usando token de autenticação
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

class PrivateUpdateManager:
    """Gerenciador de atualizações via GitHub (Repositório Privado)"""
    
    def __init__(self, repo_owner="wmedrado", repo_name="bot-keydrop", current_version="2.0.0"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.current_version = current_version
        self.github_api = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        self.update_in_progress = False
        
        # Token de acesso pessoal do GitHub (deve ser configurado)
        self.github_token = self.get_github_token()
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        } if self.github_token else {}
        
    def get_github_token(self):
        """Obtém o token do GitHub de diferentes fontes"""
        # Método 1: Variável de ambiente
        token = os.getenv('GITHUB_TOKEN')
        if token:
            print("✅ Token do GitHub encontrado via variável de ambiente")
            return token
            
        # Método 2: Arquivo local - múltiplos caminhos para compatibilidade com executáveis
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
        print("📝 Verifique se existe o arquivo 'github_token.txt' na raiz do projeto")
        print("🔧 Ou configure a variável de ambiente GITHUB_TOKEN")
        print("🔍 Caminhos verificados:")
        for path in possible_paths:
            print(f"   - {path} ({'✅' if path.exists() else '❌'})")
        return None
        
    def check_for_updates(self):
        """Verifica se há atualizações disponíveis"""
        if not self.github_token:
            print("❌ Token do GitHub não configurado!")
            return {
                "available": False,
                "error": "Token do GitHub não configurado. Verifique o arquivo github_token.txt"
            }
            
        try:
            print("🔍 Verificando atualizações (repositório privado)...")
            print(f"📂 Repositório: {self.repo_owner}/{self.repo_name}")
            
            # Buscar última release no GitHub
            url = f"{self.github_api}/releases/latest"
            print(f"🌐 URL da API: {url}")
            
            response = requests.get(
                url,
                headers=self.headers,
                timeout=10
            )
            
            print(f"📡 Status da resposta: {response.status_code}")
            
            if response.status_code == 200:
                release_data = response.json()
                latest_version = release_data.get("tag_name", "").replace("v", "")
                
                if self.is_newer_version(latest_version, self.current_version):
                    return {
                        "available": True,
                        "version": latest_version,
                        "changelog": release_data.get("body", "Sem changelog disponível"),
                        "release_date": release_data.get("published_at"),
                        "assets": release_data.get("assets", [])
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
    
    def download_update(self, update_info):
        """Baixa a atualização"""
        if not update_info.get("available"):
            return False
            
        try:
            # Verificar se há assets disponíveis
            assets = update_info.get("assets", [])
            if not assets:
                print("❌ Nenhum asset disponível para download")
                return False
            
            # Procurar por arquivo ZIP
            download_url = None
            for asset in assets:
                if asset.get("name", "").endswith('.zip'):
                    download_url = asset.get("url")
                    break
            
            if not download_url:
                print("❌ Arquivo ZIP não encontrado nos assets")
                return False
            
            print(f"📥 Baixando atualização v{update_info['version']}...")
            
            # Baixar arquivo
            response = requests.get(
                download_url,
                headers={**self.headers, "Accept": "application/octet-stream"},
                stream=True
            )
            
            if response.status_code == 200:
                # Salvar arquivo temporário
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.zip')
                
                for chunk in response.iter_content(chunk_size=8192):
                    temp_file.write(chunk)
                
                temp_file.close()
                
                # Extrair e aplicar atualização
                return self.apply_update(temp_file.name)
                
            else:
                print(f"❌ Erro ao baixar: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante download: {e}")
            return False
    
    def apply_update(self, zip_path):
        """Aplica a atualização baixada"""
        try:
            print("🔄 Aplicando atualização...")
            
            # Criar backup
            backup_dir = f"backup/backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Arquivos importantes para backup
            important_files = [
                'bot_config.json',
                'profiles/',
                'logs/',
                'github_token.txt'
            ]
            
            for file_path in important_files:
                if os.path.exists(file_path):
                    if os.path.isdir(file_path):
                        shutil.copytree(file_path, f"{backup_dir}/{file_path}")
                    else:
                        shutil.copy2(file_path, f"{backup_dir}/{file_path}")
            
            # Extrair atualização
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall('temp_update')
            
            # Encontrar pasta raiz da atualização
            update_root = None
            for item in os.listdir('temp_update'):
                if os.path.isdir(f'temp_update/{item}'):
                    update_root = f'temp_update/{item}'
                    break
            
            if not update_root:
                print("❌ Estrutura de atualização inválida")
                return False
            
            # Aplicar arquivos da atualização
            for root, dirs, files in os.walk(update_root):
                for file in files:
                    src = os.path.join(root, file)
                    rel_path = os.path.relpath(src, update_root)
                    dst = rel_path
                    
                    # Pular arquivos de configuração
                    if file in ['bot_config.json', 'github_token.txt']:
                        continue
                    
                    # Criar diretório se necessário
                    dst_dir = os.path.dirname(dst)
                    if dst_dir:
                        os.makedirs(dst_dir, exist_ok=True)
                    
                    # Copiar arquivo
                    shutil.copy2(src, dst)
            
            # Limpar arquivos temporários
            shutil.rmtree('temp_update')
            os.unlink(zip_path)
            
            print("✅ Atualização aplicada com sucesso!")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao aplicar atualização: {e}")
            return False
    
    def update_with_gui(self, parent_window=None):
        """Atualiza com interface gráfica"""
        update_info = self.check_for_updates()
        
        if update_info.get("error"):
            messagebox.showerror("Erro", f"Erro ao verificar atualizações:\n{update_info['error']}")
            return False
        
        if not update_info.get("available"):
            messagebox.showinfo("Atualização", update_info.get("message", "Nenhuma atualização disponível"))
            return False
        
        # Perguntar se deseja atualizar
        response = messagebox.askyesno(
            "Atualização Disponível",
            f"Nova versão disponível: v{update_info['version']}\n\n"
            f"Changelog:\n{update_info['changelog'][:200]}...\n\n"
            "Deseja atualizar agora?"
        )
        
        if response:
            # Iniciar atualização em thread separada
            def update_thread():
                success = self.download_update(update_info)
                if success:
                    messagebox.showinfo("Sucesso", "Atualização concluída!\nReinicie o bot para aplicar.")
                else:
                    messagebox.showerror("Erro", "Falha ao aplicar atualização")
            
            thread = threading.Thread(target=update_thread, daemon=True)
            thread.start()
            
            return True
        
        return False

# Exemplo de uso
if __name__ == "__main__":
    updater = PrivateUpdateManager()
    
    # Verificar atualizações
    update_info = updater.check_for_updates()
    
    if update_info.get("available"):
        print(f"✅ Atualização disponível: v{update_info['version']}")
        print(f"📋 Changelog: {update_info['changelog']}")
        
        # Baixar e aplicar
        if updater.download_update(update_info):
            print("🎉 Atualização aplicada com sucesso!")
        else:
            print("❌ Falha na atualização")
    else:
        print("ℹ️ Nenhuma atualização disponível")
        if update_info.get("error"):
            print(f"❌ Erro: {update_info['error']}")
