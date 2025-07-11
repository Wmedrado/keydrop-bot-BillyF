# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop\\keydrop_bot_desktop.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop\\bot-icone.ico', '.')],
    hiddenimports=['tkinter', 'tkinter.ttk', 'tkinter.messagebox', 'tkinter.scrolledtext', 'tkinter.filedialog', 'threading', 'subprocess', 'json', 'requests', 'psutil', 'time', 'logging', 'traceback', 'datetime', 'pathlib'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['selenium', 'webdriver_manager'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='KeydropBot_v3.0.0_FINAL',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\William\\Desktop\\Projeto do zero\\bot_keydrop\\bot-icone.ico'],
)
