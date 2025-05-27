# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['django', 'django.template.loader_tags', 'django.template.defaulttags', 'django.template.defaultfilters', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.db.models.sql.compiler', 'django.views.generic.dates', 'threading', 'socket', 'webbrowser', 'datetime', 'traceback', 'time', 'pathlib', 'shutil', 'json', 'csv', 'io', 'dateutil.relativedelta', 'reportlab.lib.pagesizes', 'reportlab.lib.colors', 'reportlab.platypus', 'reportlab.lib.styles', 'reportlab.lib.units', 'crispy_forms', 'polls', 'polls.models', 'vineland', 'vineland.models', 'vineland.views', 'vineland.utils.scoring', 'mysite', 'mysite.settings'],
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
    a.binaries,
    a.datas,
    [],
    name='VinelandII-Evaluator.exe',
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
)
