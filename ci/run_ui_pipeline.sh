#!/bin/bash
set -e
mkdir -p build_results

# Install dependencies for UI validation
pip install beautifulsoup4

# Compile Python interface modules
python -m py_compile user_interface.py bot_keydrop/keydrop_bot_desktop_v4.py

# Validate HTML interface components
python - <<'PY'
from bs4 import BeautifulSoup
from pathlib import Path
missing = []
html = Path('bot_keydrop/frontend/index.html').read_text(encoding='utf-8')
soup = BeautifulSoup(html, 'html.parser')

required_ids = ['stats', 'recordMacroBtn', 'saveMacroBtn', 'startBtn',
                'uptime', 'totalParticipations', 'contingencyList']
for rid in required_ids:
    if soup.find(id=rid) is None:
        missing.append(rid)
if missing:
    raise SystemExit('Missing UI components: ' + ', '.join(missing))
print('UI components validated')

# Check system tray helpers
code = Path('bot_keydrop/keydrop_bot_desktop_v4.py').read_text(encoding='utf-8')
if 'def setup_tray_icon' not in code:
    raise SystemExit('setup_tray_icon function missing')
if 'def on_minimize' not in code:
    raise SystemExit('on_minimize function missing')
print('System tray helpers validated')
PY

echo "UI pipeline succeeded" > build_results/ui_build_status.log
