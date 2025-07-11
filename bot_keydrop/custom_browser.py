
import sys
import os
import psutil
from PyQt5.QtCore import QUrl, Qt, QTimer
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel
)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineSettings

_qt_app = None
def ensure_qt_app():
    global _qt_app
    if _qt_app is None:
        _qt_app = QApplication.instance() or QApplication(sys.argv)
    return _qt_app

class BrowserTab(QWidget):
    def __init__(self, profile_path, url, parent=None):
        super().__init__(parent)
        self.profile = QWebEngineProfile(profile_path, self)
        self.page = QWebEnginePage(self.profile, self)
        self.view = QWebEngineView(self)
        self.view.setPage(self.page)
        self.address_bar = QLineEdit(url)
        self.address_bar.returnPressed.connect(self.load_url_from_bar)
        self.back_btn = QPushButton('←')
        self.forward_btn = QPushButton('→')
        self.reload_btn = QPushButton('⟳')
        self.close_btn = QPushButton('✖')
        self.back_btn.clicked.connect(self.view.back)
        self.forward_btn.clicked.connect(self.view.forward)
        self.reload_btn.clicked.connect(self.view.reload)
        self.close_btn.clicked.connect(self.close_tab)
        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.back_btn)
        nav_layout.addWidget(self.forward_btn)
        nav_layout.addWidget(self.reload_btn)
        nav_layout.addWidget(self.address_bar)
        nav_layout.addWidget(self.close_btn)
        layout = QVBoxLayout(self)
        layout.addLayout(nav_layout)
        layout.addWidget(self.view)
        self.setLayout(layout)
        self.view.load(QUrl(url))
        self.view.urlChanged.connect(self.update_address_bar)
        self.closed = False
    def load_url_from_bar(self):
        url = self.address_bar.text()
        self.view.load(QUrl(url))
    def update_address_bar(self, url):
        self.address_bar.setText(url.toString())
    def close_tab(self):
        self.closed = True
        self.setParent(None)
    def run_js(self, script, callback=None):
        # PyQt5 requires a callable for callback, or omit if None
        if callback is not None:
            self.page.runJavaScript(script, callback)
        else:
            self.page.runJavaScript(script)
    def get_resource_usage(self):
        # QWebEnginePage does not expose PID; fallback to current process
        proc = psutil.Process(os.getpid())
        ram = proc.memory_info().rss // (1024 * 1024)
        cpu = proc.cpu_percent(interval=0.1)
        return {'ram': ram, 'cpu': cpu}

class CustomBrowser(QMainWindow):
    def __init__(self, profile_path, window_size=(800,600), headless=False):
        ensure_qt_app()
        super().__init__()
        self.profile_path = profile_path
        self.headless = headless
        central_widget = QWidget(self)
        main_layout = QVBoxLayout(central_widget)
        self.resource_label = QLabel('RAM: 0 MB | CPU: 0%')
        main_layout.addWidget(self.resource_label)
        self.tabs = QTabWidget(self)
        main_layout.addWidget(self.tabs)
        self.setCentralWidget(central_widget)
        self.setWindowTitle('Keydrop Bot Browser')
        self.resize(*window_size)
        self.monitor_timer = QTimer(self)
        self.monitor_timer.timeout.connect(self.update_resource_stats)
        self.monitor_timer.start(2000)
        self.add_tab('https://key-drop.com/pt/giveaways/list')
        if self.headless:
            self.hide()
    def add_tab(self, url):
        tab = BrowserTab(self.profile_path, url)
        idx = self.tabs.addTab(tab, url)
        self.tabs.setCurrentIndex(idx)
        tab.close_btn.clicked.connect(lambda: self.close_tab(idx))
        return tab
    def close_tab(self, idx):
        tab = self.tabs.widget(idx)
        if tab:
            tab.close_tab()
            self.tabs.removeTab(idx)
    def load_url(self, url, tab_idx=None):
        if tab_idx is None:
            tab = self.tabs.currentWidget()
        else:
            tab = self.tabs.widget(tab_idx)
        if tab:
            tab.view.load(QUrl(url))
    def run_js(self, script, tab_idx=None, callback=None):
        if tab_idx is None:
            tab = self.tabs.currentWidget()
        else:
            tab = self.tabs.widget(tab_idx)
        if tab:
            tab.run_js(script, callback)
    def show(self):
        super().show()
    def hide(self):
        super().hide()
    # Removido método resize para evitar conflito com QMainWindow
    def update_resource_stats(self):
        total_ram = 0
        total_cpu = 0
        for i in range(self.tabs.count()):
            tab = self.tabs.widget(i)
            if tab is not None and hasattr(tab, 'get_resource_usage'):
                usage = tab.get_resource_usage()
                total_ram += usage['ram']
                total_cpu += usage['cpu']
        self.resource_label.setText(f'RAM: {total_ram} MB | CPU: {total_cpu:.1f}%')
    def get_profile_path(self):
        return self.profile_path
    def get_tab_count(self):
        return self.tabs.count()
    def is_headless(self):
        return self.headless

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Custom Keydrop Bot Browser')
    parser.add_argument('--profile', type=str, default='custom_profile', help='Profile directory')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode')
    args = parser.parse_args()
    app = ensure_qt_app()
    browser = CustomBrowser(profile_path=args.profile, headless=args.headless)
    browser.show()
    sys.exit(app.exec_())
        # nav_bar.addWidget(btn_settings)


