import os
import shutil
import zipfile
from pathlib import Path

def create_portable_package():
    """Crée un package portable de l'application Vineland"""
    
    print("📦 CRÉATION DU PACKAGE PORTABLE VINELAND-II")
    print("="*50)
    
    # Dossiers à inclure
    project_dir = Path(".")
    package_dir = Path("VinelandII-Portable")
    
    # Nettoyer le dossier de destination
    if package_dir.exists():
        shutil.rmtree(package_dir)
    
    package_dir.mkdir()
    
    # Fichiers et dossiers à copier
    items_to_copy = [
        'mysite',
        'polls', 
        'vineland',
        'templates',  # Si il existe
        'static',     # Si il existe
        'db.sqlite3',
        'manage.py',
        'run_vineland.py'  # Notre nouveau lanceur
    ]
    
    # Copier les éléments
    for item in items_to_copy:
        source = project_dir / item
        dest = package_dir / item
        
        if source.exists():
            if source.is_dir():
                shutil.copytree(source, dest)
                print(f"✅ Dossier copié: {item}")
            else:
                shutil.copy2(source, dest)
                print(f"✅ Fichier copié: {item}")
        else:
            print(f"⚠️  Non trouvé (ignoré): {item}")
    
    # Créer le fichier batch Windows
    batch_content = '''@echo off
echo ================================
echo   VINELAND-II PORTABLE
echo ================================
echo Verification de Python...

python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe ou pas dans le PATH
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo Verification de Django...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo Installation de Django...
    pip install django reportlab python-dateutil django-crispy-forms
)

echo Lancement de l'application...
python run_vineland.py
pause
'''
    
    with open(package_dir / 'Lancer_Vineland.bat', 'w', encoding='utf-8') as f:
        f.write(batch_content)
    
    # Créer le script shell pour Mac/Linux  
    shell_content = '''#!/bin/bash
echo "================================"
echo "   VINELAND-II PORTABLE"
echo "================================"
echo "Vérification de Python..."

if ! command -v python3 &> /dev/null; then
    echo "ERREUR: Python3 n'est pas installé"
    echo "Installez Python3 depuis votre gestionnaire de paquets"
    read -p "Appuyez sur Entrée pour continuer..."
    exit 1
fi

echo "Vérification de Django..."
python3 -c "import django" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "Installation de Django..."
    pip3 install django reportlab python-dateutil django-crispy-forms
fi

echo "Lancement de l'application..."
python3 run_vineland.py
read -p "Appuyez sur Entrée pour fermer..."
'''
    
    shell_file = package_dir / 'lancer_vineland.sh'
    with open(shell_file, 'w', encoding='utf-8') as f:
        f.write(shell_content)
    
    # Rendre le script exécutable sur Unix
    shell_file.chmod(0o755)
    
    # Créer le README
    readme_content = '''# VINELAND-II PORTABLE

## Installation et utilisation

### Windows:
1. Double-cliquez sur `Lancer_Vineland.bat`
2. L'application s'ouvre dans votre navigateur

### Mac/Linux:
1. Ouvrez un terminal dans ce dossier
2. Exécutez: `./lancer_vineland.sh`
3. L'application s'ouvre dans votre navigateur

## Prérequis
- Python 3.8+ installé sur votre système
- Connexion internet (pour installer Django la première fois)

## Données
- Vos données sont sauvegardées automatiquement
- Windows: `%LOCALAPPDATA%/VinelandII/`
- Mac/Linux: `~/.vineland2/`

## Support
En cas de problème, vérifiez que Python est bien installé et accessible.
'''
    
    with open(package_dir / 'README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"\n✅ Package créé dans: {package_dir}")
    print("\n📋 CONTENU DU PACKAGE:")
    for item in package_dir.iterdir():
        print(f"  📁 {item.name}")
    
    # Créer une archive ZIP
    zip_name = "VinelandII-Portable.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arc_name = os.path.relpath(file_path, package_dir.parent)
                zipf.write(file_path, arc_name)
    
    print(f"\n📦 Archive créée: {zip_name}")
    print("\n🎯 POUR DISTRIBUER:")
    print(f"1. Envoyez le fichier {zip_name} à vos testeurs")
    print("2. Ils décompressent et lancent le script approprié")
    print("3. L'application fonctionne sans compilation!")

if __name__ == "__main__":
    create_portable_package()