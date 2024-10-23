# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['OSC Countdown.py'],
    pathex=[],
    binaries=[],
    datas=[('/Library/Frameworks/Python.framework/Versions/3.12/lib/python3.12/site-packages/customtkinter', 'customtkinter/'), ('localSettings.json', '.'), ('Oceanix.json', '.'), ('TrojanBlue.json', '.')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='OSC Countdown',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['timerIcns.icns'],
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='OSC Countdown',
)
app = BUNDLE(
    coll,
    name='OSC Countdown.app',
    icon='timerIcns.icns',
    bundle_identifier=None,
)
