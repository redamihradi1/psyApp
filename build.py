import PyInstaller.__main__
import os
import sys

project_path = os.path.abspath(os.path.dirname(__file__))

# Adapter aux dossiers de votre projet Vineland-II
data_dirs = [
    ('mysite', 'mysite'),
    ('polls', 'polls'),
    ('vineland', 'vineland'),
    ('polls/templates', 'polls/templates'),
    ('vineland/templates', 'vineland/templates'),
    ('polls/static', 'polls/static'),
    ('vineland/static', 'vineland/static'),
    ('static', 'static'),
    ('db.sqlite3', '.'),
    ('manage.py', '.'),
]

args = [
    'launcher.py',
    '--onefile',
    '--name=VinelandII-Evaluator',
    '--clean',
    '--console',
    '--exclude-module=django.contrib.postgres',
    '--noupx',
]

# Ajouter les dossiers de données
for src, dst in data_dirs:
    src_path = os.path.join(project_path, src)
    if os.path.exists(src_path):
        separator = ';' if sys.platform == 'win32' else ':'
        args.append(f'--add-data={src_path}{separator}{dst}')

# Imports Django nécessaires + modules spécifiques Vineland
args.extend([
    '--hidden-import=django',
    '--hidden-import=django.template.loader_tags',
    '--hidden-import=django.template.defaulttags',
    '--hidden-import=django.contrib.admin',
    '--hidden-import=django.contrib.auth',
    '--hidden-import=django.contrib.contenttypes',
    '--hidden-import=django.contrib.sessions',
    '--hidden-import=django.contrib.messages',
    '--hidden-import=django.contrib.staticfiles',
    '--hidden-import=django.db.models.sql.compiler',
    '--hidden-import=django.views.generic.dates',
    '--hidden-import=threading',
    '--hidden-import=socket',
    '--hidden-import=webbrowser',
    '--hidden-import=datetime',
    '--hidden-import=traceback',
    '--hidden-import=time',
    '--hidden-import=pathlib',
    '--hidden-import=shutil',
    '--hidden-import=dateutil.relativedelta',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.lib.pagesizes',
    '--hidden-import=crispy_forms',
    # Vos modules spécifiques
    '--hidden-import=mysite',
    '--hidden-import=mysite.settings',
    '--hidden-import=mysite.urls',
    '--hidden-import=mysite.wsgi',
    '--hidden-import=polls',
    '--hidden-import=polls.apps',
    '--hidden-import=polls.models',
    '--hidden-import=polls.views',
    '--hidden-import=polls.urls',
    '--hidden-import=polls.admin',
    '--hidden-import=vineland',
    '--hidden-import=vineland.apps',
    '--hidden-import=vineland.models',
    '--hidden-import=vineland.views',
    '--hidden-import=vineland.urls',
    '--hidden-import=vineland.admin',
])

print("Demarrage de la compilation Vineland-II...")

try:
    PyInstaller.__main__.run(args)
    print("Compilation terminee avec succes!")
    print("Executable disponible dans le dossier 'dist/'")
except Exception as e:
    print(f"Erreur lors de la compilation: {str(e)}")
    print("\nCommande PyInstaller equivalente:")
    cmd = "pyinstaller " + " ".join([f'"{arg}"' if ' ' in arg else arg for arg in args])
    print(cmd)