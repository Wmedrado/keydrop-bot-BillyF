"""
Gerenciador de navegador
Responsável por iniciar, fechar e gerenciar instâncias do Chrome usando Playwright
"""

import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from .macro_recorder import MacroRecorder
from datetime import datetime
from pathlib import Path
import json
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TabInfo:
    """Informações de uma guia do navegador"""
    tab_id: int
    page: Optional[Page]
    context: Optional[BrowserContext]
    url: str
    status: str  # 'loading', 'ready', 'participating', 'waiting', 'error', 'closed'
    last_activity: datetime
    error_count: int = 0
    participation_count: int = 0
    proxy: str = ""
    macro_recorder: Optional[MacroRecorder] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'tab_id': self.tab_id,
            'url': self.url,
            'status': self.status,
            'last_activity': self.last_activity.isoformat(),
            'error_count': self.error_count,
            'participation_count': self.participation_count,
            'proxy': self.proxy
        }


class BrowserManager:
    """Gerenciador de navegador usando Playwright"""
    
    def __init__(self):
        """Inicializa o gerenciador de navegador"""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.tabs: Dict[int, TabInfo] = {}
        self.contexts: Dict[int, BrowserContext] = {}  # Contexts por tab_id
        self.user_profiles_dir = Path("profiles")  # Diretório base para perfis
        self.macro_dir = Path("macros")
        self.is_running = False
        self.headless_mode = False
        self.mini_window_mode = False
        self.enable_stealth = True
        self.keep_cookies = True
        self.optimize_resources = True
        self.user_data_dir = None
        self.browser_args = []
        
        # Configurações do navegador
        self.default_viewport = {'width': 1280, 'height': 720}
        self.mini_viewport = {'width': 200, 'height': 300}

        # Criar diretório de perfis se não existir
        self.user_profiles_dir.mkdir(exist_ok=True)
        self.macro_dir.mkdir(exist_ok=True)
        
        logger.info("Browser Manager inicializado com suporte a perfis distintos")
    
    async def start_browser(
        self,
        headless: bool = False,
        mini_window: bool = False,
        user_data_dir: Optional[str] = None,
        stealth: bool = True,
    ) -> bool:
        """
        Inicia o navegador Chrome
        
        Args:
            headless: Executar em modo headless
            mini_window: Usar janelas em modo mini
            user_data_dir: Diretório de dados do usuário (para manter login)
            
        Returns:
            True se iniciou com sucesso
        """
        try:
            self.headless_mode = headless
            self.mini_window_mode = mini_window
            self.user_data_dir = user_data_dir
            self.enable_stealth = stealth
            
            # Inicializar Playwright
            self.playwright = await async_playwright().start()
            
            # Configurar argumentos do navegador
            browser_args = [
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-gpu',
                '--disable-extensions',
                '--disable-plugins',
                '--disable-images',  # Para economizar banda
                '--disable-javascript-harmony-shipping',
                '--disable-background-timer-throttling',
                '--disable-backgrounding-occluded-windows',
                '--disable-renderer-backgrounding',
                '--disable-field-trial-config',
                '--disable-ipc-flooding-protection',
                '--disable-default-apps'
            ]
            
            # Adicionar argumentos para economizar recursos
            if self.mini_window_mode:
                browser_args.extend([
                    f'--window-size={self.mini_viewport["width"]},{self.mini_viewport["height"]}',
                    '--force-device-scale-factor=0.5'
                ])
            
            # Configurar contexto do navegador
            launch_options = {
                'headless': self.headless_mode,
                'args': browser_args,
                'ignore_default_args': ['--enable-blink-features=IdleDetection']  # Evitar detecção de automação
            }
            
            if self.user_data_dir:
                launch_options['user_data_dir'] = self.user_data_dir
            
            # Iniciar navegador Google Chrome
            launch_options["channel"] = "chrome"  # garantir uso do Chrome estável
            self.browser = await self.playwright.chromium.launch(**launch_options)
            self.is_running = True
            
            logger.info(f"Navegador iniciado - Headless: {headless}, Mini: {mini_window}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao iniciar navegador: {e}")
            await self.stop_browser()
            return False
    
    def _get_profile_path(self, tab_id: int) -> Path:
        """
        Obtém o caminho do perfil específico para uma guia
        
        Args:
            tab_id: ID da guia
            
        Returns:
            Caminho do perfil
        """
        return self.user_profiles_dir / f"profile_{tab_id}"
    
    def _create_user_profile(self, tab_id: int) -> Path:
        """
        Cria um perfil de usuário único para uma guia
        
        Args:
            tab_id: ID da guia
            
        Returns:
            Caminho do perfil criado
        """
        profile_path = self._get_profile_path(tab_id)
        
        # Criar diretório do perfil se não existir
        profile_path.mkdir(parents=True, exist_ok=True)
        
        # Criar estrutura básica do perfil Chrome
        (profile_path / "Default").mkdir(exist_ok=True)
        
        logger.info(f"Perfil de usuário criado para guia {tab_id}: {profile_path}")
        return profile_path
    
    async def _setup_stealth_mode(self, page: Page) -> None:
        """
        Configura modo stealth para evitar detecção de bot
        
        Args:
            page: Página do navegador
        """
        try:
            # Remover propriedades do webdriver
            await page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            
            # Modificar user agent
            await page.set_extra_http_headers({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            })
            
            # Simular plugins
            await page.add_init_script("""
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5],
                });
            """)
            
            # Simular linguagens
            await page.add_init_script("""
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['pt-BR', 'pt', 'en'],
                });
            """)
            
        except Exception as e:
            logger.warning(f"Erro ao configurar modo stealth: {e}")

    async def save_session_data(self, tab_id: int) -> bool:
        """
        Salva dados de sessão (cookies, localStorage) para um perfil
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se salvou com sucesso
        """
        try:
            if tab_id not in self.contexts:
                logger.warning(f"Contexto não encontrado para guia {tab_id}")
                return False
            
            context = self.contexts[tab_id]
            profile_path = self._get_profile_path(tab_id)
            session_file = profile_path / "session.json"
            
            # Salvar estado da sessão
            storage_state = await context.storage_state()
            
            with open(session_file, 'w', encoding='utf-8') as f:
                json.dump(storage_state, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Dados de sessão salvos para guia {tab_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao salvar sessão da guia {tab_id}: {e}")
            return False

    async def clear_cache_keep_login(self, tab_id: Optional[int] = None) -> bool:
        """
        Limpa cache do navegador mantendo dados de login
        
        Args:
            tab_id: ID da guia específica ou None para todas
            
        Returns:
            True se limpou com sucesso
        """
        try:
            if tab_id is not None:
                # Limpar cache de uma guia específica
                if tab_id in self.contexts:
                    context = self.contexts[tab_id]
                    
                    # Salvar dados de login antes de limpar
                    await self.save_session_data(tab_id)
                    
                    # Limpar apenas dados temporários
                    await context.clear_cookies(domain=None)
                    
                    logger.info(f"Cache limpo para guia {tab_id}, mantendo login")
                    return True
                else:
                    logger.warning(f"Guia {tab_id} não encontrada")
                    return False
            else:
                # Limpar cache de todas as guias
                success_count = 0
                for tid in list(self.contexts.keys()):
                    if await self.clear_cache_keep_login(tid):
                        success_count += 1
                
                logger.info(f"Cache limpo para {success_count} guias, mantendo logins")
                return success_count > 0
                
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False

    async def create_tab(self, tab_id: int, url: str = "about:blank", proxy: Optional[str] = None) -> Optional[TabInfo]:
        """
        Cria uma nova guia com perfil de usuário único
        
        Args:
            tab_id: ID único da guia
            url: URL para navegar (opcional)
            
        Returns:
            Informações da guia criada ou None se falhou
        """
        if not self.is_running or not self.browser:
            logger.error("Navegador não está rodando")
            return None
        
        try:
            # Criar perfil único para esta guia
            profile_path = self._create_user_profile(tab_id)
            
            # Configurar opções do contexto com perfil persistente
            context_options = {
                'viewport': self.mini_viewport if self.mini_window_mode else self.default_viewport,
                'ignore_https_errors': True,
                'java_script_enabled': True,
                'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }

            if proxy:
                context_options['proxy'] = {"server": proxy}
            
            # Adicionar dados de sessão se existirem
            if self.keep_cookies:
                session_file = profile_path / "session.json"
                if session_file.exists():
                    try:
                        with open(session_file, 'r', encoding='utf-8') as f:
                            storage_state = json.load(f)
                        context_options['storage_state'] = storage_state
                        logger.info(f"Dados de sessão carregados para guia {tab_id}")
                    except Exception as e:
                        logger.warning(f"Erro ao carregar sessão para guia {tab_id}: {e}")
            
            # Criar contexto isolado
            context = await self.browser.new_context(**context_options)
            
            # Configurar timeout
            context.set_default_timeout(30000)  # 30 segundos
            
            # Criar nova página
            page = await context.new_page()
            
            # Aplicar modo stealth se habilitado
            if self.enable_stealth:
                await self._setup_stealth_mode(page)
            
            # Configurar eventos da página
            await self._setup_page_events(page, tab_id)
            
            # Criar informações da guia
            tab_info = TabInfo(
                tab_id=tab_id,
                page=page,
                context=context,
                url=url,
                status='loading',
                last_activity=datetime.now(),
                proxy=proxy or ""
            )
            
            self.tabs[tab_id] = tab_info
            self.contexts[tab_id] = context
            
            # Navegar para URL se fornecida
            if url and url != "about:blank":
                await self.navigate_tab(tab_id, url)
            else:
                tab_info.status = 'ready'
            
            logger.info(f"Guia {tab_id} criada com sucesso")
            return tab_info
            
        except Exception as e:
            logger.error(f"Erro ao criar guia {tab_id}: {e}")
            return None
    
    async def _setup_page_events(self, page: Page, tab_id: int):
        """
        Configura eventos da página
        
        Args:
            page: Página do Playwright
            tab_id: ID da guia
        """
        try:
            # Event handler para console
            page.on("console", lambda msg: logger.debug(f"Tab {tab_id} Console: {msg.text}"))
            
            # Event handler para erros
            page.on("pageerror", lambda error: logger.error(f"Tab {tab_id} Page Error: {error}"))
            
            # Event handler para requests
            async def handle_request(request):
                # Bloquear recursos desnecessários para economizar banda
                if request.resource_type in ['image', 'font', 'media']:
                    await request.abort()
                else:
                    await request.continue_()
            
            await page.route("**/*", handle_request)
            
        except Exception as e:
            logger.error(f"Erro ao configurar eventos da página {tab_id}: {e}")
    
    async def navigate_tab(self, tab_id: int, url: str) -> bool:
        """
        Navega uma guia para uma URL
        
        Args:
            tab_id: ID da guia
            url: URL de destino
            
        Returns:
            True se navegou com sucesso
        """
        if tab_id not in self.tabs:
            logger.error(f"Guia {tab_id} não encontrada")
            return False
        
        tab_info = self.tabs[tab_id]
        if not tab_info.page:
            logger.error(f"Página da guia {tab_id} não disponível")
            return False
        
        try:
            tab_info.status = 'loading'
            tab_info.last_activity = datetime.now()
            
            # Navegar para URL
            await tab_info.page.goto(url, wait_until='domcontentloaded', timeout=30000)
            
            tab_info.url = url
            tab_info.status = 'ready'
            
            logger.info(f"Guia {tab_id} navegou para {url}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao navegar guia {tab_id} para {url}: {e}")
            tab_info.status = 'error'
            tab_info.error_count += 1
            return False
    
    async def close_tab(self, tab_id: int) -> bool:
        """
        Fecha uma guia específica
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se fechou com sucesso
        """
        if tab_id not in self.tabs:
            logger.warning(f"Guia {tab_id} não encontrada para fechar")
            return False
        
        try:
            tab_info = self.tabs[tab_id]
            
            if tab_info.page:
                await tab_info.page.close()
            
            if tab_info.context:
                await tab_info.context.close()
            
            tab_info.status = 'closed'
            del self.tabs[tab_id]
            
            logger.info(f"Guia {tab_id} fechada com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao fechar guia {tab_id}: {e}")
            return False
    
    async def restart_tab(self, tab_id: int) -> bool:
        """
        Reinicia uma guia específica
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se reiniciou com sucesso
        """
        if tab_id not in self.tabs:
            logger.error(f"Guia {tab_id} não encontrada para reiniciar")
            return False
        
        try:
            tab_info = self.tabs[tab_id]
            original_url = tab_info.url
            
            # Fechar guia atual
            await self.close_tab(tab_id)
            
            # Criar nova guia
            new_tab = await self.create_tab(tab_id, original_url, tab_info.proxy)
            
            if new_tab:
                logger.info(f"Guia {tab_id} reiniciada com sucesso")
                return True
            else:
                logger.error(f"Falha ao reiniciar guia {tab_id}")
                return False
                
        except Exception as e:
            logger.error(f"Erro ao reiniciar guia {tab_id}: {e}")
            return False
    
    async def clear_cache(self, preserve_login: bool = True) -> bool:
        """
        Limpa cache do navegador
        
        Args:
            preserve_login: Manter informações de login
            
        Returns:
            True se limpou com sucesso
        """
        try:
            if not self.browser:
                return False
            
            # Para cada contexto ativo
            for tab_info in self.tabs.values():
                if tab_info.context:
                    # Limpar cache sem afetar cookies se preserve_login for True
                    await tab_info.context.clear_cookies() if not preserve_login else None
                    
                    # Recarregar página para aplicar limpeza
                    if tab_info.page and tab_info.url != "about:blank":
                        await tab_info.page.reload()
            
            logger.info(f"Cache limpo - Login preservado: {preserve_login}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao limpar cache: {e}")
            return False
    
    async def stop_browser(self) -> bool:
        """
        Para o navegador e fecha todas as guias
        
        Returns:
            True se parou com sucesso
        """
        try:
            # Fechar todas as guias
            tabs_to_close = list(self.tabs.keys())
            for tab_id in tabs_to_close:
                await self.close_tab(tab_id)
            
            # Fechar navegador
            if self.browser:
                await self.browser.close()
                self.browser = None
            
            # Parar Playwright
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            
            self.is_running = False
            self.tabs.clear()
            
            logger.info("Navegador parado com sucesso")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao parar navegador: {e}")
            return False
    
    async def emergency_stop(self):
        """Parada de emergência - fecha todas as instâncias imediatamente"""
        try:
            logger.warning("🚨 PARADA DE EMERGÊNCIA ATIVADA")
            
            # Parar tarefas em execução
            for task in list(self.active_tasks):
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            
            self.active_tasks.clear()
            
            # Fechar todas as instâncias
            for browser_id in list(self.browsers.keys()):
                await self.close_browser(browser_id)
            
            logger.info("Parada de emergência concluída")
            return True
            
        except Exception as e:
            logger.error(f"Erro na parada de emergência: {e}")
            return False

    async def clear_cache_keep_login(self):
        """Limpa cache do navegador mantendo cookies de login"""
        try:
            logger.info("Iniciando limpeza de cache...")
            cache_cleared = False
            
            for browser_id, browser_info in self.browsers.items():
                try:
                    context = browser_info['context']
                    
                    # Limpar apenas cache, mantendo cookies
                    await context.clear_cookies(domain_filter=lambda domain: 
                        not any(login_domain in domain.lower() 
                               for login_domain in ['keydrop', 'steam', 'steamcommunity']))
                    
                    # Limpar storage exceto dados de login
                    pages = context.pages
                    for page in pages:
                        try:
                            # Limpar sessionStorage e localStorage, exceto dados de login
                            await page.evaluate("""
                                () => {
                                    // Salvar dados importantes de login
                                    const loginData = {};
                                    for (let i = 0; i < localStorage.length; i++) {
                                        const key = localStorage.key(i);
                                        if (key && (key.includes('login') || key.includes('auth') || key.includes('token'))) {
                                            loginData[key] = localStorage.getItem(key);
                                        }
                                    }
                                    
                                    // Limpar tudo
                                    localStorage.clear();
                                    sessionStorage.clear();
                                    
                                    // Restaurar dados de login
                                    Object.entries(loginData).forEach(([key, value]) => {
                                        localStorage.setItem(key, value);
                                    });
                                }
                            """)
                        except Exception as e:
                            logger.warning(f"Erro ao limpar storage da página: {e}")
                    
                    cache_cleared = True
                    logger.info(f"Cache limpo para navegador {browser_id}")
                    
                except Exception as e:
                    logger.error(f"Erro ao limpar cache do navegador {browser_id}: {e}")
            
            if cache_cleared:
                logger.info("Limpeza de cache concluída com sucesso")
            else:
                logger.warning("Nenhum cache foi limpo")
                
            return cache_cleared
            
        except Exception as e:
            logger.error(f"Erro na limpeza de cache: {e}")
            return False

    def get_tab_info(self, tab_id: int) -> Optional[TabInfo]:
        """
        Obtém informações de uma guia
        
        Args:
            tab_id: ID da guia
            
        Returns:
            Informações da guia ou None se não encontrada
        """
        return self.tabs.get(tab_id)
    
    def get_all_tabs_info(self) -> List[Dict[str, Any]]:
        """
        Obtém informações de todas as guias
        
        Returns:
            Lista com informações de todas as guias
        """
        return [tab_info.to_dict() for tab_info in self.tabs.values()]
    
    def get_tab_count(self) -> int:
        """
        Retorna o número de guias ativas
        
        Returns:
            Número de guias ativas
        """
        return len(self.tabs)
    
    def is_tab_ready(self, tab_id: int) -> bool:
        """
        Verifica se uma guia está pronta para uso
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se a guia está pronta
        """
        tab_info = self.tabs.get(tab_id)
        return tab_info is not None and tab_info.status in ['ready', 'waiting']

    # ------------------------------------------------------------------
    # Macro recording utilities
    # ------------------------------------------------------------------
    async def start_macro_recording(self, tab_id: int) -> bool:
        tab = self.get_tab_info(tab_id)
        if not tab or not tab.page:
            return False
        tab.macro_recorder = MacroRecorder(tab.page)
        await tab.macro_recorder.start()
        return True

    async def pause_macro_recording(self, tab_id: int) -> bool:
        tab = self.get_tab_info(tab_id)
        if tab and tab.macro_recorder:
            await tab.macro_recorder.pause()
            return True
        return False

    async def resume_macro_recording(self, tab_id: int) -> bool:
        tab = self.get_tab_info(tab_id)
        if tab and tab.macro_recorder:
            await tab.macro_recorder.resume()
            return True
        return False

    async def save_macro(self, tab_id: int, use_first: bool = False) -> Optional[Path]:
        tab = self.get_tab_info(tab_id)
        if not tab or not tab.macro_recorder:
            return None
        await tab.macro_recorder.stop()
        path = self.macro_dir / f"participation_macro_{tab_id}.json"
        tab.macro_recorder.save(path)
        return path


# Instância global do gerenciador de navegador
browser_manager = BrowserManager()

async def start_browser(
    headless: bool = False,
    mini_window: bool = False,
    user_data_dir: Optional[str] = None,
    stealth: bool = True,
) -> bool:
    """
    Função utilitária para iniciar o navegador
    
    Args:
        headless: Modo headless
        mini_window: Modo mini window
        user_data_dir: Diretório de dados do usuário
        
    Returns:
        True se iniciou com sucesso
    """
    return await browser_manager.start_browser(headless, mini_window, user_data_dir, stealth)

async def stop_browser() -> bool:
    """
    Função utilitária para parar o navegador
    
    Returns:
        True se parou com sucesso
    """
    return await browser_manager.stop_browser()

async def emergency_stop_browser() -> bool:
    """
    Função utilitária para parada de emergência
    
    Returns:
        True se parou com sucesso
    """
    return await browser_manager.emergency_stop()
