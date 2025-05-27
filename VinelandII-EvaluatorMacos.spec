# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[('C:\\Users\\PC\\Desktop\\djangotutorial\\mysite', 'mysite'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\polls', 'polls'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\vineland', 'vineland'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\polls/templates', 'polls/templates'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\vineland/templates', 'vineland/templates'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\static', 'static'), ('C:\\Users\\PC\\Desktop\\djangotutorial\\db.sqlite3', '.')],
    hiddenimports=['django', 'django.template.loader_tags', 'django.template.defaulttags', 'django.contrib.admin', 'django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions', 'django.contrib.messages', 'django.contrib.staticfiles', 'django.db.models.sql.compiler', 'django.views.generic.dates', 'threading', 'socket', 'webbrowser', 'datetime', 'traceback', 'time', 'pathlib', 'shutil', 'dateutil.relativedelta', 'reportlab.platypus', 'reportlab.lib.pagesizes', 'crispy_forms', '_sysconfigdata__darwin_darwin', 'unicodedata'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=['C:\\Users\\PC\\Desktop\\djangotutorial\\pyi_rth_django.py'],
    excludes=['django.contrib.postgres'],
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
    name='VinelandII-EvaluatorMacos',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch='universal2',
    codesign_identity=None,
    entitlements_file=None,
)
