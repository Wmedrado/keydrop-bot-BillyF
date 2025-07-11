#!/usr/bin/env python3
"""
Configuração de ícones para a interface moderna
"""

# Mapeamento de ícones por funcionalidade
ICONS = {
    # Interface Principal
    'title': '🔑',
    'status_running': '🟢',
    'status_stopped': '🔴',
    'status_warning': '🟡',
    'status_initializing': '⚪',
    
    # Configurações
    'config': '⚙️',
    'config_advanced': '🔧',
    'windows': '🪟',
    'speed': '⚡',
    'save': '💾',
    'load': '📂',
    
    # Modos
    'modes': '🎮',
    'headless': '👁️',
    'login': '🔐',
    'contender': '🏆',
    'amateur': '🎯',
    'help': '❓',
    
    # Controles
    'start': '▶️',
    'stop': '⏹️',
    'pause': '⏸️',
    'restart': '🔄',
    'clean': '🧹',
    
    # Estatísticas
    'stats': '📊',
    'money': '💰',
    'gain': '📈',
    'loss': '📉',
    'error': '❌',
    'success': '✅',
    'warning': '⚠️',
    
    # Performance
    'performance': '⚡',
    'cpu': '🖥️',
    'ram': '🐏',
    'disk': '💾',
    'network': '🌐',
    
    # Integração
    'discord': '📱',
    'webhook': '🔗',
    'reports': '📋',
    'notification': '🔔',
    
    # Logs
    'logs': '📄',
    'debug': '🐛',
    'info': 'ℹ️',
    'launch': '🚀',
    
    # Navegador
    'browser': '🌐',
    'chrome': '🌍',
    'cache': '🗂️',
    'cookies': '🍪',
    
    # Sorteios
    'giveaway': '🎁',
    'ticket': '🎟️',
    'winner': '🏆',
    'participate': '🎯',
    
    # Sistema
    'system': '💻',
    'folder': '📁',
    'file': '📄',
    'backup': '💾',
    'restore': '↩️',
    
    # Estados
    'loading': '⏳',
    'waiting': '⌛',
    'active': '🟢',
    'inactive': '🔴',
    'paused': '🟡',
    
    # Ações
    'edit': '✏️',
    'delete': '🗑️',
    'add': '➕',
    'remove': '➖',
    'update': '🔄',
    'refresh': '🔄',
    
    # Qualidade
    'quality': '⭐',
    'excellent': '🌟',
    'good': '👍',
    'bad': '👎',
    'critical': '🚨',
    
    # Tempo
    'time': '⏰',
    'schedule': '📅',
    'timer': '⏱️',
    'countdown': '⏳',
    
    # Setas e Direções
    'up': '⬆️',
    'down': '⬇️',
    'left': '⬅️',
    'right': '➡️',
    'expand': '🔽',
    'collapse': '🔼',
    
    # Segurança
    'security': '🔒',
    'key': '🔑',
    'lock': '🔐',
    'unlock': '🔓',
    'shield': '🛡️',
    
    # Comunicação
    'message': '💬',
    'mail': '📧',
    'phone': '📞',
    'chat': '💭',
    'comment': '💬',
    
    # Ferramentas
    'tools': '🔧',
    'wrench': '🔧',
    'hammer': '🔨',
    'screwdriver': '🪚',
    'gear': '⚙️',
    
    # Cores para Estados
    'green': '🟢',
    'red': '🔴',
    'yellow': '🟡',
    'blue': '🔵',
    'purple': '🟣',
    'orange': '🟠',
    'white': '⚪',
    'black': '⚫'
}

# Cores para diferentes estados
COLORS = {
    'success': '#4CAF50',
    'error': '#F44336',
    'warning': '#FF9800',
    'info': '#2196F3',
    'primary': '#1976D2',
    'secondary': '#424242',
    'background': '#121212',
    'surface': '#1E1E1E',
    'text': '#FFFFFF',
    'text_secondary': '#AAAAAA'
}

# Configurações de tema
THEME_CONFIG = {
    'appearance_mode': 'dark',
    'color_theme': 'blue',
    'corner_radius': 10,
    'button_corner_radius': 8,
    'progressbar_corner_radius': 1000,
    'slider_corner_radius': 1000,
    'switch_corner_radius': 1000,
    'checkbox_corner_radius': 3,
    'textbox_corner_radius': 6,
    'scrollbar_corner_radius': 1000,
    'dropdown_corner_radius': 6,
    'combobox_corner_radius': 6,
    'optionmenu_corner_radius': 6,
    'entry_corner_radius': 6,
    'frame_corner_radius': 10,
    'label_corner_radius': 0,
    'toplevel_corner_radius': 10,
    'window_corner_radius': 10
}

def get_icon(name):
    """Retorna o ícone correspondente ao nome"""
    return ICONS.get(name, '❓')

def get_color(name):
    """Retorna a cor correspondente ao nome"""
    return COLORS.get(name, '#FFFFFF')

def get_status_icon(status):
    """Retorna ícone baseado no status"""
    status_map = {
        'running': get_icon('status_running'),
        'stopped': get_icon('status_stopped'),
        'warning': get_icon('status_warning'),
        'initializing': get_icon('status_initializing'),
        'error': get_icon('error'),
        'success': get_icon('success')
    }
    return status_map.get(status, get_icon('status_stopped'))

def get_performance_color(percentage):
    """Retorna cor baseada na porcentagem de performance"""
    if percentage < 50:
        return get_color('success')
    elif percentage < 80:
        return get_color('warning')
    else:
        return get_color('error')

def format_with_icon(text, icon_name):
    """Formata texto com ícone"""
    icon = get_icon(icon_name)
    return f"{icon} {text}"

def get_mode_description(mode):
    """Retorna descrição completa do modo com ícone"""
    descriptions = {
        'headless': f"{get_icon('headless')} Headless (Oculto)",
        'login': f"{get_icon('login')} Login Automático", 
        'contender': f"{get_icon('contender')} CONTENDER (1h)",
        'amateur': f"{get_icon('amateur')} AMATEUR (3min)",
        'reports': f"{get_icon('reports')} Relatórios (12h)"
    }
    return descriptions.get(mode, mode)

def get_control_button_config(action):
    """Retorna configuração completa do botão de controle"""
    configs = {
        'start': {
            'text': f"{get_icon('start')} Iniciar Bots",
            'fg_color': get_color('success'),
            'hover_color': '#45A049'
        },
        'stop': {
            'text': f"{get_icon('stop')} Parar Bots",
            'fg_color': get_color('error'),
            'hover_color': '#E53935'
        },
        'clean': {
            'text': f"{get_icon('clean')} Limpar Cache",
            'fg_color': get_color('warning'),
            'hover_color': '#FB8C00'
        },
        'save': {
            'text': f"{get_icon('save')} Salvar Config",
            'fg_color': get_color('primary'),
            'hover_color': '#1565C0'
        },
        'advanced': {
            'text': f"{get_icon('config_advanced')} Avançadas",
            'fg_color': get_color('secondary'),
            'hover_color': '#616161'
        },
        'help': {
            'text': f"{get_icon('help')} Ajuda",
            'fg_color': get_color('info'),
            'hover_color': '#1976D2'
        }
    }
    return configs.get(action, {})

# Configuração de tooltips
TOOLTIPS = {
    'num_bots': 'Número de janelas do navegador para executar simultaneamente',
    'velocidade_navegacao': 'Velocidade de navegação (1-10): maior = mais rápido',
    'headless': 'Executa navegador sem interface gráfica (economia de recursos)',
    'login_mode': 'Detecta automaticamente quando precisa fazer login',
    'contender_mode': 'Participa de sorteios especiais de 1 hora',
    'discord_webhook': 'URL do webhook do Discord para notificações',
    'relatorios_automaticos': 'Envia relatórios automáticos a cada 12 horas',
    'limpar_cache': 'Remove arquivos temporários preservando login',
    'salvar_config': 'Salva todas as configurações no arquivo JSON'
}

def get_tooltip(element):
    """Retorna tooltip para o elemento"""
    return TOOLTIPS.get(element, 'Sem informações disponíveis')
