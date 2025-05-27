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

# Configuration spécifique pour macOS
args = [
    'launcher.py',
    '--onefile',
    '--name=VinelandII-EvaluatorMacos',
    '--clean',
    '--console',
    '--exclude-module=django.contrib.postgres',
    '--noupx',
    # Options spécifiques macOS
    '--osx-bundle-identifier=com.vineland.evaluator',
    '--target-arch=universal2',  # Support Intel + Apple Silicon
]

# Ajout des données avec séparateur Unix
for src, dst in data_dirs:
    src_path = os.path.join(project_path, src)
    if os.path.exists(src_path):
        args.append(f'--add-data={src_path}:{dst}')

# Hook Django si présent
hook_path = os.path.join(project_path, 'pyi_rth_django.py')
if os.path.exists(hook_path):
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
    # Ajouts spécifiques macOS
    '--hidden-import=_sysconfigdata__darwin_darwin',
    '--hidden-import=unicodedata',
])

print("🍎 Démarrage de la compilation pour macOS...")
print(f"Architecture cible: {args[6] if '--target-arch=' in str(args) else 'par défaut'}")

try:
    PyInstaller.__main__.run(args)
    print("✅ Compilation terminée avec succès!")
    print("📦 L'exécutable se trouve dans le dossier 'dist/'")
    
    # Instructions post-compilation
    print("\n" + "="*50)
    print("📋 INSTRUCTIONS POST-COMPILATION:")
    print("="*50)
    print("1. Testez l'app: ./dist/VinelandII-Evaluator")
    print("2. Pour distribuer: créez un .dmg ou .pkg")
    print("3. Code signing requis pour distribution")
    print("="*50)
    
except Exception as e:
    print(f"❌ Erreur lors de la compilation: {str(e)}")
    print("\n🔧 Commande manuelle à essayer:")
    cmd = "pyinstaller " + " ".join([f'"{arg}"' if ' ' in arg else arg for arg in args])
    print(cmd)