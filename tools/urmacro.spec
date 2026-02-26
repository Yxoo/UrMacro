# -*- mode: python ; coding: utf-8 -*-
# SPECPATH = dossier contenant ce fichier (tools/)
import os
import certifi

block_cipher = None

a = Analysis(
    [os.path.join(SPECPATH, '..', 'main.py')],
    pathex=[os.path.join(SPECPATH, '..')],
    binaries=[],
    datas=[
        (certifi.where(), 'certifi'),
    ],
    hiddenimports=[
        'pynput',
        'pynput.keyboard',
        'pynput.mouse',
        'pydirectinput',
        'win32gui',
        'win32con',
        'win32api',
        'urmacro',
        'urmacro._input_api',
        'urmacro._utils',
        'src',
        'src.core',
        'src.ui',
        'requests',
        'certifi',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='UrMacro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=os.path.join(SPECPATH, 'icon.ico'),
)
