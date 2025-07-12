"""
Tarefas de automação
Contém a lógica para interagir com o Keydrop e executar participações em sorteios
"""

import asyncio
import logging
import random
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ParticipationResult(Enum):
    """Resultado de uma tentativa de participação"""
    SUCCESS = "success"
    FAILED = "failed" 
    RETRY = "retry"
    BUTTON_NOT_FOUND = "button_not_found"
    PAGE_ERROR = "page_error"
    TIMEOUT = "timeout"
    ALREADY_PARTICIPATED = "already_participated"


@dataclass
class ParticipationAttempt:
    """Informações de uma tentativa de participação"""
    tab_id: int
    attempt_number: int
    timestamp: datetime
    result: ParticipationResult
    error_message: Optional[str] = None
    lottery_type: Optional[str] = None
    lottery_title: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Converte para dicionário"""
        return {
            'tab_id': self.tab_id,
            'attempt_number': self.attempt_number,
            'timestamp': self.timestamp.isoformat(),
            'result': self.result.value,
            'error_message': self.error_message,
            'lottery_type': self.lottery_type,
            'lottery_title': self.lottery_title
        }


@dataclass
class WinningRecord:
    """Informações de um ganho obtido"""
    timestamp: datetime
    amount: float
    lottery_type: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            'timestamp': self.timestamp.isoformat(),
            'amount': self.amount,
            'lottery_type': self.lottery_type
        }


class KeydropAutomation:
    """Classe para automação específica do Keydrop"""
    
    # Seletores CSS para elementos do Keydrop
    SELECTORS = {
        # Página de listagem de sorteios
        'giveaway_card': '[data-testid="div-active-giveaways-list-single-card"]',
        'join_link': '[data-testid="btn-single-card-giveaway-join"]',
        # Página do sorteio específico
        'join_button': '[data-testid="btn-giveaway-join-the-giveaway"]',
        # Outros seletores utilitários
        'amateur_lottery': '.lottery-card[data-type="amateur"], .amateur-lottery, [data-lottery-type="amateur"]',
        'lottery_title': '.lottery-title, .lottery-name, h3, h4',
        'already_participated': '.already-participated, .participated, [class*="disabled"]',
        'loading': '.loading, .spinner, [class*="loading"]',
        'error_message': '.error, .alert-danger, .error-message',
        'login_required': '.login-required, .auth-required, [href*="login"]'
    }
    
    # URLs importantes
    URLS = {
        'keydrop_main': 'https://key-drop.com/pt/',
        'keydrop_lotteries': 'https://key-drop.com/pt/lotteries',
        'steam_login': 'https://steamcommunity.com/login/home/?goto='
    }
    
    def __init__(self, browser_manager):
        """
        Inicializa a automação do Keydrop
        
        Args:
            browser_manager: Instância do gerenciador de navegador
        """
        self.browser_manager = browser_manager
        self.participation_history: List[ParticipationAttempt] = []
        self.winnings_history: List[WinningRecord] = []
        self.max_history_size = 1000
        
        logger.info("Automação Keydrop inicializada")
    
    async def participate_in_lottery(self, tab_id: int, max_retries: int = 3) -> ParticipationAttempt:
        """
        Participa de um sorteio em uma guia específica
        
        Args:
            tab_id: ID da guia
            max_retries: Número máximo de tentativas
            
        Returns:
            Resultado da tentativa de participação
        """
        tab_info = self.browser_manager.get_tab_info(tab_id)
        if not tab_info or not tab_info.page:
            return ParticipationAttempt(
                tab_id=tab_id,
                attempt_number=1,
                timestamp=datetime.now(),
                result=ParticipationResult.FAILED,
                error_message="Guia não disponível"
            )
        
        page = tab_info.page
        attempt_number = 1
        
        while attempt_number <= max_retries:
            try:
                logger.info(f"Tentativa {attempt_number} de participação na guia {tab_id}")
                
                # Atualizar status da guia
                tab_info.status = 'participating'
                tab_info.last_activity = datetime.now()
                
                # Garantir que estamos na página de sorteios
                await page.goto(
                    self.URLS['keydrop_lotteries'],
                    wait_until='domcontentloaded',
                    timeout=30000
                )
                
                # Verificar se requer login
                if await self._check_login_required(page):
                    return ParticipationAttempt(
                        tab_id=tab_id,
                        attempt_number=attempt_number,
                        timestamp=datetime.now(),
                        result=ParticipationResult.FAILED,
                        error_message="Login necessário"
                    )
                
                # Procurar sorteios disponíveis
                lotteries = await self._find_available_lotteries(page)
                
                if not lotteries:
                    return ParticipationAttempt(
                        tab_id=tab_id,
                        attempt_number=attempt_number,
                        timestamp=datetime.now(),
                        result=ParticipationResult.BUTTON_NOT_FOUND,
                        error_message="Nenhum sorteio disponível encontrado"
                    )
                
                # Tentar participar do primeiro sorteio encontrado
                for lottery in lotteries:
                    result = await self._attempt_participation(page, lottery, tab_id, attempt_number)
                    
                    if result.result == ParticipationResult.SUCCESS:
                        tab_info.participation_count += 1
                        tab_info.status = 'waiting'
                        self._add_to_history(result)
                        return result
                    elif result.result == ParticipationResult.ALREADY_PARTICIPATED:
                        # Continuar para próximo sorteio
                        continue
                
                # Se chegou aqui, não conseguiu participar de nenhum sorteio
                attempt_number += 1
                if attempt_number <= max_retries:
                    await asyncio.sleep(random.uniform(2, 5))  # Aguardar antes de tentar novamente
                
            except Exception as e:
                logger.error(f"Erro na tentativa {attempt_number} de participação na guia {tab_id}: {e}")
                attempt_number += 1
                if attempt_number <= max_retries:
                    await asyncio.sleep(random.uniform(3, 7))
        
        # Todas as tentativas falharam
        tab_info.error_count += 1
        tab_info.status = 'error'
        
        result = ParticipationAttempt(
            tab_id=tab_id,
            attempt_number=max_retries,
            timestamp=datetime.now(),
            result=ParticipationResult.FAILED,
            error_message=f"Falhou após {max_retries} tentativas"
        )
        
        self._add_to_history(result)
        return result
    
    async def _check_login_required(self, page) -> bool:
        """
        Verifica se a página requer login
        
        Args:
            page: Página do Playwright
            
        Returns:
            True se requer login
        """
        try:
            login_element = await page.query_selector(self.SELECTORS['login_required'])
            return login_element is not None
        except Exception:
            return False
    
    async def _find_available_lotteries(self, page) -> List[Dict[str, Any]]:
        """
        Encontra sorteios disponíveis na página
        
        Args:
            page: Página do Playwright
            
        Returns:
            Lista de sorteios encontrados
        """
        lotteries = []
        
        try:
            # Aguardar um momento para carregamento
            await asyncio.sleep(random.uniform(1, 3))
            
            # Procurar cards de sorteio disponíveis
            cards = await page.query_selector_all(self.SELECTORS['giveaway_card'])

            for card in cards:
                try:
                    link = await card.query_selector(self.SELECTORS['join_link'])
                    if link and await link.is_enabled():
                        lottery_info = await self._extract_lottery_info(card)
                        lotteries.append({'card': card, 'link': link, 'info': lottery_info})
                except Exception as e:
                    logger.debug(f"Erro ao processar card de sorteio: {e}")
                    continue
            
            logger.info(f"Encontrados {len(lotteries)} sorteios disponíveis")
            return lotteries
            
        except Exception as e:
            logger.error(f"Erro ao procurar sorteios: {e}")
            return []
    
    async def _extract_lottery_info(self, card) -> Dict[str, Any]:
        """
        Extrai informações de um sorteio
        
        Args:
            card: Elemento do card de sorteio
            
        Returns:
            Informações do sorteio
        """
        info = {
            'title': '',
            'type': 'unknown',
            'is_amateur': False
        }
        
        try:
            # Procurar título dentro do card
            title_element = await card.query_selector(self.SELECTORS['lottery_title'])
            if title_element:
                info['title'] = await title_element.inner_text()

            # Verificar se é sorteio AMATEUR
            amateur_element = await card.query_selector(self.SELECTORS['amateur_lottery'])
            if amateur_element or 'amateur' in info['title'].lower():
                info['type'] = 'amateur'
                info['is_amateur'] = True
        
        except Exception as e:
            logger.debug(f"Erro ao extrair informações do sorteio: {e}")
        
        return info
    
    async def _attempt_participation(self, page, lottery: Dict[str, Any], tab_id: int, attempt_number: int) -> ParticipationAttempt:
        """
        Tenta participar de um sorteio específico
        
        Args:
            page: Página do Playwright
            lottery: Informações do sorteio
            tab_id: ID da guia
            attempt_number: Número da tentativa
            
        Returns:
            Resultado da tentativa
        """
        try:
            link = lottery['link']
            lottery_info = lottery['info']
            
            # Abrir página do sorteio
            await link.click()
            await page.wait_for_load_state('domcontentloaded', timeout=15000)

            # Procurar botão final de participação
            join_button = await page.wait_for_selector(self.SELECTORS['join_button'], timeout=10000)

            if not join_button:
                await page.go_back()
                return ParticipationAttempt(
                    tab_id=tab_id,
                    attempt_number=attempt_number,
                    timestamp=datetime.now(),
                    result=ParticipationResult.BUTTON_NOT_FOUND,
                    error_message='Botão de participação não encontrado',
                    lottery_type=lottery_info['type'],
                    lottery_title=lottery_info['title']
                )

            # Verificar se já participou
            button_text = await join_button.inner_text()
            if any(word in button_text.lower() for word in ['já aderiu', 'já participou', 'participando']):
                await page.go_back()
                return ParticipationAttempt(
                    tab_id=tab_id,
                    attempt_number=attempt_number,
                    timestamp=datetime.now(),
                    result=ParticipationResult.ALREADY_PARTICIPATED,
                    lottery_type=lottery_info['type'],
                    lottery_title=lottery_info['title']
                )

            # Mover o mouse para o botão (simular comportamento humano)
            await join_button.hover()
            await asyncio.sleep(random.uniform(0.5, 1.5))

            # Clicar no botão
            await join_button.click()

            # Aguardar resultado da participação
            await asyncio.sleep(random.uniform(2, 4))

            # Verificar se a participação foi bem-sucedida
            success = await self._verify_participation_success(page, join_button)

            result = ParticipationResult.SUCCESS if success else ParticipationResult.FAILED

            logger.info(f"Participação na guia {tab_id}: {result.value}")

            # Voltar para a página de sorteios
            await page.go_back()

            return ParticipationAttempt(
                tab_id=tab_id,
                attempt_number=attempt_number,
                timestamp=datetime.now(),
                result=result,
                lottery_type=lottery_info['type'],
                lottery_title=lottery_info['title']
            )
            
        except Exception as e:
            logger.error(f"Erro ao tentar participar: {e}")
            return ParticipationAttempt(
                tab_id=tab_id,
                attempt_number=attempt_number,
                timestamp=datetime.now(),
                result=ParticipationResult.FAILED,
                error_message=str(e)
            )
    
    async def _verify_participation_success(self, page, button) -> bool:
        """
        Verifica se a participação foi bem-sucedida
        
        Args:
            page: Página do Playwright
            button: Botão que foi clicado
            
        Returns:
            True se a participação foi bem-sucedida
        """
        try:
            # Aguardar um momento para a página processar
            await asyncio.sleep(2)
            
            # Verificar mudança no texto do botão
            new_button_text = await button.inner_text()
            success_keywords = [
                'participando', 'participated', 'sucesso', 'success',
                'j\xc3\xa1 aderiu', 'j\xc3\xa1 participou'
            ]
            
            if any(keyword in new_button_text.lower() for keyword in success_keywords):
                return True
            
            # Verificar se o botão ficou desabilitado
            if not await button.is_enabled():
                return True
            
            # Procurar mensagens de sucesso na página
            success_selectors = [
                '.success-message',
                '.alert-success',
                '[class*="success"]',
                '.notification[class*="success"]'
            ]
            
            for selector in success_selectors:
                element = await page.query_selector(selector)
                if element and await element.is_visible():
                    return True
            
            return False
            
        except Exception as e:
            logger.debug(f"Erro ao verificar sucesso da participação: {e}")
            return False
    
    async def navigate_to_lotteries(self, tab_id: int) -> bool:
        """
        Navega para a página de sorteios
        
        Args:
            tab_id: ID da guia
            
        Returns:
            True se navegou com sucesso
        """
        try:
            tab_info = self.browser_manager.get_tab_info(tab_id)
            if not tab_info or not tab_info.page:
                return False
            
            page = tab_info.page
            
            # Navegar para página de sorteios
            await page.goto(self.URLS['keydrop_lotteries'], wait_until='domcontentloaded', timeout=30000)
            
            # Aguardar carregamento
            await asyncio.sleep(random.uniform(3, 6))
            
            tab_info.url = self.URLS['keydrop_lotteries']
            tab_info.status = 'ready'
            
            logger.info(f"Guia {tab_id} navegou para página de sorteios")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao navegar para sorteios na guia {tab_id}: {e}")
            return False
    
    async def setup_login_tabs(self) -> Tuple[bool, List[int]]:
        """
        Configura guias para login manual
        
        Returns:
            Tupla (sucesso, lista de IDs das guias de login)
        """
        try:
            login_tab_ids = []
            
            # Criar guia para Keydrop
            keydrop_tab = await self.browser_manager.create_tab(-1, self.URLS['keydrop_main'])
            if keydrop_tab:
                login_tab_ids.append(-1)
                logger.info("Guia de login Keydrop criada")
            
            # Criar guia para Steam
            steam_tab = await self.browser_manager.create_tab(-2, self.URLS['steam_login'])
            if steam_tab:
                login_tab_ids.append(-2)
                logger.info("Guia de login Steam criada")
            
            if login_tab_ids:
                logger.info(f"Aguardando login manual nas guias: {login_tab_ids}")
                return True, login_tab_ids
            else:
                return False, []
                
        except Exception as e:
            logger.error(f"Erro ao configurar guias de login: {e}")
            return False, []
    
    def _add_to_history(self, attempt: ParticipationAttempt):
        """
        Adiciona tentativa ao histórico
        
        Args:
            attempt: Tentativa de participação
        """
        self.participation_history.append(attempt)
        
        # Manter apenas os últimos registros
        if len(self.participation_history) > self.max_history_size:
            self.participation_history.pop(0)
    
    def get_participation_stats(self, hours: int = 24) -> Dict[str, Any]:
        """
        Obtém estatísticas de participação
        
        Args:
            hours: Número de horas para considerar
            
        Returns:
            Estatísticas de participação
        """
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        recent_attempts = [
            attempt for attempt in self.participation_history
            if attempt.timestamp >= cutoff_time
        ]
        
        total_attempts = len(recent_attempts)
        successful = len([a for a in recent_attempts if a.result == ParticipationResult.SUCCESS])
        failed = len([a for a in recent_attempts if a.result == ParticipationResult.FAILED])
        
        success_rate = (successful / total_attempts * 100) if total_attempts > 0 else 0
        
        return {
            'total_attempts': total_attempts,
            'successful_participations': successful,
            'failed_participations': failed,
            'success_rate': success_rate,
            'period_hours': hours,
            'last_attempt': recent_attempts[-1].timestamp.isoformat() if recent_attempts else None
        }
    
    def get_participation_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Obtém histórico de participações
        
        Args:
            limit: Limite de registros (opcional)
            
        Returns:
            Lista de tentativas de participação
        """
        history = self.participation_history
        if limit:
            history = history[-limit:]

        return [attempt.to_dict() for attempt in history]

    def record_winning(self, amount: float, lottery_type: str) -> None:
        """Registra um ganho obtido"""
        record = WinningRecord(
            timestamp=datetime.now(),
            amount=amount,
            lottery_type=lottery_type
        )
        self.winnings_history.append(record)
        if len(self.winnings_history) > self.max_history_size:
            self.winnings_history.pop(0)

    def get_winnings_history(self, limit: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retorna histórico de ganhos"""
        history = self.winnings_history
        if limit:
            history = history[-limit:]
        return [record.to_dict() for record in history]


# Função utilitária para criar instância da automação
def create_keydrop_automation(browser_manager) -> KeydropAutomation:
    """
    Cria instância da automação Keydrop
    
    Args:
        browser_manager: Gerenciador de navegador
        
    Returns:
        Instância da automação
    """
    return KeydropAutomation(browser_manager)
