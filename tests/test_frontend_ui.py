from pathlib import Path
from bs4 import BeautifulSoup

HTML_FILE = Path('bot_keydrop/frontend/index.html')


def test_ui_components_exist():
    soup = BeautifulSoup(HTML_FILE.read_text(encoding='utf-8'), 'html.parser')
    assert soup.find(id='stats'), 'Aba de Estatisticas ausente'
    assert soup.find(id='recordMacroBtn'), 'Botao Gravar Macro ausente'
    assert soup.find(id='saveMacroBtn'), 'Botao Salvar Macro ausente'
    assert soup.find(id='startBtn'), 'Botao Iniciar Bot ausente'
    assert soup.find(id='uptime'), 'Elemento de tempo ativo ausente'
    assert soup.find(id='totalParticipations'), 'Elemento de participacoes ausente'
    assert soup.find(id='contingencyList'), 'Lista de contingencias ausente'


def test_system_tray_helpers():
    code = Path('bot_keydrop/keydrop_bot_desktop_v4.py').read_text(encoding='utf-8')
    assert 'def setup_tray_icon' in code
    assert 'def on_minimize' in code
