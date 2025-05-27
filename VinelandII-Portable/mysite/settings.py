import PyInstaller.__main__
import os
import sys
import platform

project_path = os.path.abspath(os.path.dirname(__file__))

# Adapte ces chemins selon la structure de ton projet
data_dirs = [
    # Ton projet principal
    ('mysite', 'mysite'),  # settings.py, urls.py, etc.
    
    # Tes applications Django
    ('polls', 'polls'),
    ('vineland', 'vineland'),
    
    # Templates
    ('templates', 'templates'),
    
    # Fichiers statiques
    ('static', 'static'),
    
    # Base de données (sera copiée au premier lancement)
    ('db.sqlite3', '.'),
]

# Nom de l'exécutable selon l'OS
app_name = 'VinelandII-Evaluator'
if platform.system() == 'Windows':
    app_name += '.exe'

args = [
    'launcher.py',
    '--onefile',
    f'--name={app_name}',
    '--clean',
    '--console',  # Retire cette ligne si tu veux pas de console
    '--noconfirm',
]

# Ajouter les dossiers de données
for src, dst in data_dirs:
    src_path = os.path.join(project_path, src)
    if os.path.exists(src_path):
        separator = ';' if sys.platform == 'win32' else ':'
        args.append(f'--add-data={src_path}{separator}{dst}')
        print(f"✅ Ajout : {src} -> {dst}")
    else:
        print(f"⚠️  Ignoré (non trouvé) : {src}")

# Imports Django et autres dépendances
hidden_imports = [
    # Django core
    'django',
    'django.template.loader_tags',
    'django.template.defaulttags',
    'django.template.defaultfilters',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.db.models.sql.compiler',
    'django.views.generic.dates',
    
    # Modules système
    'threading',
    'socket',
    'webbrowser',
    'datetime',
    'traceback',
    'time',
    'pathlib',
    'shutil',
    'json',
    'csv',
    'io',
    
    # Spécifique à ton projet
    'dateutil.relativedelta',
    'reportlab.lib.pagesizes',
    'reportlab.lib.colors',
    'reportlab.platypus',
    'reportlab.lib.styles',
    'reportlab.lib.units',
    'crispy_forms',
    
    # Tes apps Django
    'polls',
    'polls.models',
    'vineland',
    'vineland.models',
    'vineland.views',
    'vineland.utils.scoring',
    'mysite',
    'mysite.settings',
]

for import_name in hidden_imports:
    args.append(f'--hidden-import={import_name}')

print("🔨 COMPILATION VINELAND-II")
print("="*50)
print(f"📂 Projet : {project_path}")
print(f"🎯 Cible : {app_name}")
print(f"💻 OS : {platform.system()}")
print("="*50)

try:
    PyInstaller.__main__.run(args)
    print("\n✅ COMPILATION RÉUSSIE!")
    print(f"📁 Exécutable créé dans : dist/{app_name}")
    
    # Instructions pour les testeurs
    print("\n📋 INSTRUCTIONS POUR LES TESTEURS:")
    print("="*50)
    print("1. Copiez le fichier dans dist/ vers votre ordinateur")
    print("2. Double-cliquez sur l'exécutable")
    print("3. L'application s'ouvrira automatiquement dans votre navigateur")
    print("4. Vos données sont sauvegardées localement")
    print("5. Fermez la fenêtre noire pour arrêter l'application")
    print("="*50)
    
except Exception as e:
    print(f"\n❌ ERREUR LORS DE LA COMPILATION: {str(e)}")
    print("\n🔧 Commande PyInstaller équivalente:")
    cmd = "pyinstaller " + " ".join([f'"{arg}"' if ' ' in arg else arg for arg in args])
    print(cmd)
    
    print("\n💡 SOLUTIONS POSSIBLES:")
    print("- Installez PyInstaller : pip install pyinstaller")
    print("- Vérifiez que tous les modules sont installés")
    print("- Adaptez les chemins dans build.py selon votre structure")

input("\nAppuyez sur Entrée pour continuer...")