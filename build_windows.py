import PyInstaller.__main__
import os
import sys

project_path = os.path.abspath(os.path.dirname(__file__))

data_dirs = [
    ('mysite', 'mysite'),
    ('polls', 'polls'),
    ('vineland', 'vineland'),
    ('polls/templates', 'polls/templates'),
    ('vineland/templates', 'vineland/templates'),
    ('static', 'static'),
    ('db.sqlite3', '.'),
]

args = [
    'launcher.py',
    '--onefile',
    '--name=VinelandII-Evaluator',
    '--clean',
    '--console',
    '--exclude-module=django.contrib.postgres',  # Évite l'erreur psycopg2
    '--noupx',  # Évite les problèmes de compression
]

for src, dst in data_dirs:
    src_path = os.path.join(project_path, src)
    if os.path.exists(src_path):
        separator = ';' if sys.platform == 'win32' else ':'
        args.append(f'--add-data={src_path}{separator}{dst}')

# Ajouter le hook runtime Django
hook_path = os.path.join(project_path, 'pyi_rth_django.py')
if os.path.exists(hook_path):
    separator = ';' if sys.platform == 'win32' else ':'
    args.append(f'--runtime-hook={hook_path}')

# Imports Django nécessaires
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
])

print("Démarrage de la compilation...")

try:
    PyInstaller.__main__.run(args)
    print("Compilation terminée avec succès!")
except Exception as e:
    print(f"Erreur lors de la compilation: {str(e)}")
    print("\nEssayez d'exécuter cette commande directement:")
    cmd = "pyinstaller " + " ".join([f'"{arg}"' if ' ' in arg else arg for arg in args])
    print(cmd)