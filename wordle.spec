# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec dosyası — Wordle Türkçe.

Kullanım:
    pyinstaller wordle.spec

Platforma göre otomatik davranır:
- Windows / Linux : tek dosyalık (onefile) çalıştırılabilir üretir.
- macOS           : PyInstaller'ın .app bundle + onefile'ı birlikte
                     desteklememesi nedeniyle onedir modunda derlenir,
                     sonucunda çift tıklanabilir WordleTurkce.app üretilir.
"""
import sys

is_macos = sys.platform == "darwin"

a = Analysis(
    ["src/wordle/__main__.py"],
    pathex=["src"],
    binaries=[],
    # Sözlük verisi paket dışı bir kaynak olduğu için elle dahil ediyoruz.
    # (kaynak_yolu, hedef_klasör) — hedef, çalışma zamanında
    # Path(__file__).parent / "data" ile bulunacak şekilde paket
    # yapısını birebir koruyor.
    datas=[("src/wordle/data", "wordle/data")],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=2,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [] if is_macos else a.binaries,
    [] if is_macos else a.datas,
    [],
    exclude_binaries=is_macos,
    name="WordleTurkce",
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
    icon=None,
)

if is_macos:
    coll = COLLECT(
        exe,
        a.binaries,
        a.datas,
        strip=False,
        upx=True,
        upx_exclude=[],
        name="WordleTurkce",
    )
    app = BUNDLE(
        coll,
        name="WordleTurkce.app",
        icon=None,
        bundle_identifier="com.yusufbayraktar.wordleturkce",
        info_plist={
            "CFBundleShortVersionString": "0.1.0",
            "NSHighResolutionCapable": True,
        },
    )