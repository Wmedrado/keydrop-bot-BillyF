#!/usr/bin/env python3
"""
Sistema de verificação para Keydrop Bot Professional
Testa todos os componentes principais do sistema
"""

from __future__ import annotations

import sys
import importlib.util
from pathlib import Path
from typing import List


class SystemVerifier:
    def __init__(self) -> None:
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.issues: List[str] = []
        self.passed: int = 0
        self.total: int = 0

    def check(self, description: str, condition: bool) -> None:
        """Helper para verificar condições"""
        if not description:
            raise ValueError("Descrição não pode ser vazia")
        self.total += 1
        if condition:
            print(f"✅ {description}")
            self.passed += 1
        else:
            print(f"❌ {description}")
            self.issues.append(description)

    def verify_structure(self) -> None:
        """Verificar estrutura de diretórios"""
        print("🔍 Verificando estrutura do projeto...")

        required_dirs = ["backend", "frontend", "profiles", "resources"]

        for dir_name in required_dirs:
            dir_path = self.project_root / dir_name
            self.check(f"Diretório {dir_name}/", dir_path.exists())

    def verify_backend_files(self) -> None:
        """Verificar arquivos do backend"""
        print("\n🐍 Verificando backend...")

        required_files = [
            "main.py",
            "requirements.txt",
            "config/config_manager.py",
            "bot_logic/browser_manager.py",
            "bot_logic/automation_tasks.py",
            "bot_logic/scheduler.py",
            "system_monitor/monitor.py",
            "discord_integration/notifier.py",
        ]

        for file_path in required_files:
            full_path = self.backend_dir / file_path
            self.check(f"Backend: {file_path}", full_path.exists())

    def verify_frontend_files(self) -> None:
        """Verificar arquivos do frontend"""
        print("\n🎨 Verificando frontend...")

        required_files = [
            "index.html",
            "package.json",
            "src/js/main.js",
            "src/js/api.js",
            "src/js/ui.js",
            "src/styles/main.css",
        ]

        for file_path in required_files:
            full_path = self.frontend_dir / file_path
            self.check(f"Frontend: {file_path}", full_path.exists())

    def verify_python_dependencies(self) -> None:
        """Verificar dependências Python"""
        print("\n📦 Verificando dependências Python...")

        required_packages = ["fastapi", "uvicorn", "playwright", "psutil"]

        for package in required_packages:
            try:
                spec = importlib.util.find_spec(package)
                self.check(f"Pacote: {package}", spec is not None)
            except ImportError:
                self.check(f"Pacote: {package}", False)

    def verify_startup_scripts(self) -> None:
        """Verificar scripts de inicialização"""
        print("\n🚀 Verificando scripts de inicialização...")

        scripts = [
            "startup.py",
            "run_bot.bat",
            "build_executable.py",
            "production_launcher.py",
        ]

        for script in scripts:
            script_path = self.project_root / script
            self.check(f"Script: {script}", script_path.exists())

    def verify_documentation(self) -> None:
        """Verificar documentação"""
        print("\n📚 Verificando documentação...")

        docs = [
            "README.md",
            "REQUIREMENTS_CHECKLIST.md",
            "INSTALLATION_GUIDE.md",
            ".gitignore",
        ]

        for doc in docs:
            doc_path = self.project_root / doc
            self.check(f"Documentação: {doc}", doc_path.exists())

    def test_backend_import(self) -> None:
        """Testar importação do backend"""
        print("\n🧪 Testando importação do backend...")

        try:
            sys.path.insert(0, str(self.backend_dir))
            import main

            self.check("Importação main.py", True)

            # Verificar se a app FastAPI existe
            app = getattr(main, "app", None)
            self.check("FastAPI app definida", app is not None)

        except Exception as e:
            self.check(f"Importação main.py (erro: {e})", False)

    def verify_config_files(self) -> None:
        """Verificar arquivos de configuração"""
        print("\n⚙️ Verificando configurações...")

        # Verificar se requirements.txt tem conteúdo
        req_file = self.backend_dir / "requirements.txt"
        if req_file.exists():
            content = req_file.read_text()
            self.check("requirements.txt não vazio", len(content.strip()) > 0)
            self.check("FastAPI em requirements", "fastapi" in content.lower())
            self.check("Playwright em requirements", "playwright" in content.lower())

    def show_summary(self) -> None:
        """Mostrar resumo da verificação"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DA VERIFICAÇÃO")
        print("=" * 60)

        success_rate = (self.passed / self.total * 100) if self.total > 0 else 0

        print(f"✅ Verificações Passaram: {self.passed}/{self.total}")
        print(f"📈 Taxa de Sucesso: {success_rate:.1f}%")

        if self.issues:
            print(f"\n❌ Problemas Encontrados ({len(self.issues)}):")
            for i, issue in enumerate(self.issues, 1):
                print(f"   {i}. {issue}")

        if success_rate >= 90:
            print("\n🎉 SISTEMA VERIFICADO COM SUCESSO!")
            print("💡 O projeto está pronto para uso.")
        elif success_rate >= 70:
            print("\n⚠️  SISTEMA PARCIALMENTE FUNCIONAL")
            print("💡 Corrija os problemas listados acima.")
        else:
            print("\n❌ SISTEMA COM PROBLEMAS CRÍTICOS")
            print("💡 Verifique a instalação e dependências.")


def main() -> None:
    """Função principal de verificação"""
    print("🔍 Keydrop Bot Professional - Verificação do Sistema")
    print("=" * 60)

    verifier = SystemVerifier()

    # Executar todas as verificações
    verifier.verify_structure()
    verifier.verify_backend_files()
    verifier.verify_frontend_files()
    verifier.verify_python_dependencies()
    verifier.verify_startup_scripts()
    verifier.verify_documentation()
    verifier.verify_config_files()
    verifier.test_backend_import()

    # Mostrar resumo
    verifier.show_summary()


if __name__ == "__main__":
    main()
