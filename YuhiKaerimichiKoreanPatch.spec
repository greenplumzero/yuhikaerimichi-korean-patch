# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_data_files


a = Analysis(
    ['patch_and_run.py'],
    pathex=[],
    binaries=[],
    datas=[('korean_font.ttf', '.')] + collect_data_files('certifi'),
    hiddenimports=['lz4.block', 'certifi', 'ssl'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='YuhiKaerimichiKoreanPatch',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=True,
)
