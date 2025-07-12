import sys
import os
import types
import importlib
from pathlib import Path
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "bot_keydrop" / "backend"))

# --- helpers to create stubbed app ---

def create_test_client():
    # clear any previous imports
    sys.modules.pop('bot_keydrop.backend.main', None)
    # Stub external modules used by backend.main
    stubs = {}

    system_monitor = types.ModuleType('system_monitor')
    class Metrics:
        def to_human_readable(self):
            return {"cpu": 0}
    async def get_system_metrics():
        return Metrics()
    async def start_system_monitoring(cb):
        pass
    def stop_system_monitoring():
        pass
    system_monitor.SystemMonitor = lambda: None
    system_monitor.get_system_metrics = get_system_metrics
    system_monitor.start_system_monitoring = start_system_monitoring
    system_monitor.stop_system_monitoring = stop_system_monitoring
    stubs['system_monitor'] = system_monitor

    discord_integration = types.ModuleType('discord_integration')
    async def send_discord_notification(t, m, l):
        return True
    discord_integration.configure_discord_webhook = lambda url: None
    discord_integration.send_discord_notification = send_discord_notification
    stubs['discord_integration'] = discord_integration

    bot_logic = types.ModuleType('bot_logic')
    browser_manager = types.SimpleNamespace(
        is_running=False,
        get_tab_count=lambda: 0,
        get_all_tabs_info=lambda: [],
        close_tab=lambda tid: True,
        restart_tab=lambda tid: True,
        clear_cache=lambda keep: True,
        start_macro_recording=lambda tid: True,
        pause_macro_recording=lambda tid: True,
        resume_macro_recording=lambda tid: True,
        save_macro=lambda tid, use_first=False: '/tmp/file.json',
    )
    class DummyAutomation:
        URLS = {
            'keydrop_main': 'http://example.com',
            'keydrop_lotteries': 'http://example.com/lots',
        }
        def get_participation_stats(self):
            return {}
        def get_participation_history(self, limit=100):
            return []
        def record_winning(self, amt, lt):
            pass
        def get_winnings_history(self, limit=100):
            return []
    bot_logic.browser_manager = browser_manager
    bot_logic.create_keydrop_automation = lambda bm: DummyAutomation()
    class DummyScheduler:
        def __init__(self):
            self.status = types.SimpleNamespace(value='stopped')
        async def start_bot(self):
            self.status.value = 'running'
            return True
        async def stop_bot(self, emergency=False):
            self.status.value = 'stopped'
            return True
        async def pause_bot(self):
            self.status.value = 'paused'
            return True
        async def resume_bot(self):
            self.status.value = 'running'
            return True
        async def restart_tab(self, tid):
            return True
        async def clear_cache(self, keep):
            return True
        def get_status(self):
            return {'status': self.status.value}
        def get_tasks_status(self):
            return []
        def update_config(self):
            pass
    bot_logic.create_bot_scheduler = lambda *a, **k: DummyScheduler()
    bot_logic.BotStatus = types.SimpleNamespace(STOPPED='stopped')
    class TabWatchdog:
        def __init__(self, *a, **k):
            pass
        def start(self):
            pass
        async def stop(self):
            pass
        def update_config(self, **k):
            pass
    bot_logic.TabWatchdog = TabWatchdog
    stubs['bot_logic'] = bot_logic

    cloud_permissions = types.ModuleType('cloud.permissions')
    cloud_permissions.fetch_permissions = lambda uid: {}
    cloud_permissions.has_premium_access = lambda data: False
    cloud_permissions.has_telegram_access = lambda data: False
    cloud_permissions.subscription_active = lambda data: False
    cloud_permissions.update_permissions = lambda uid, data: None
    stubs['cloud.permissions'] = cloud_permissions

    cloud_hwid = types.ModuleType('cloud.hwid')
    cloud_hwid.validate_user_hwid = lambda uid: True
    cloud_hwid.generate_hwid = lambda: 'hwid'
    stubs['cloud.hwid'] = cloud_hwid

    cloud_fc = types.ModuleType('cloud.firebase_client')
    cloud_fc.registrar_log_suspeito = lambda *a, **k: None
    stubs['cloud.firebase_client'] = cloud_fc

    proxy_mgr = types.ModuleType('tools.proxy_manager')
    class ProxyManager:
        def __init__(self, pool, timeout):
            pass
    proxy_mgr.ProxyManager = ProxyManager
    stubs['tools.proxy_manager'] = proxy_mgr

    password_reset = types.ModuleType('password_reset')
    def request_reset(email):
        if email == 'missing@example.com':
            raise ValueError('E-mail não encontrado')
    def reset_password(token, pw):
        if token != 'valid':
            raise ValueError('token invalido')
    password_reset.request_reset = request_reset
    password_reset.reset_password = reset_password
    stubs['password_reset'] = password_reset

    stubs['uvicorn'] = types.ModuleType('uvicorn')

    for name, module in stubs.items():
        sys.modules[name] = module

    main = importlib.import_module('bot_keydrop.backend.main')
    main.app.router.on_startup.clear()
    main.app.router.on_shutdown.clear()
    main.bot_scheduler = bot_logic.create_bot_scheduler()
    main.automation_engine = bot_logic.create_keydrop_automation(None)

    return TestClient(main.app)


client = create_test_client()


def test_root_endpoint():
    resp = client.get('/')
    assert resp.status_code == 200
    data = resp.json()
    assert data['message'] == 'Keydrop Bot Professional API'
    assert 'version' in data


def test_health_endpoint():
    resp = client.get('/health')
    assert resp.status_code == 200
    data = resp.json()
    assert data['status'] == 'healthy'
    assert 'bot_status' in data


def test_get_config():
    resp = client.get('/config')
    assert resp.status_code == 200
    assert 'num_tabs' in resp.json()


def test_password_reset_flow():
    resp = client.post('/api/password-reset', json={'email': 'user@example.com'})
    assert resp.status_code == 200
    assert resp.json()['success']

    bad = client.post('/api/reset-password', json={'token': 'bad', 'password': 'x'})
    assert bad.status_code == 400

