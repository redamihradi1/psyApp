#!/usr/bin/env python
"""
VINELAND-II PORTABLE SERVER
Serveur Django portable sans compilation PyInstaller
"""

import os
import sys
import socket
import webbrowser
import time
import threading
import shutil
from pathlib import Path

def setup_environment():
    """Configure l'environnement Django"""
    # Dossier de base
    base_dir = Path(__file__).parent
    
    # Créer le dossier de données utilisateur
    if sys.platform == 'win32':
        data_dir = Path.home() / 'AppData' / 'Local' / 'VinelandII'
    else:
        data_dir = Path.home() / '.vineland2'
    
    data_dir.mkdir(parents=True, exist_ok=True)
    
    # Copier la base de données si nécessaire
    source_db = base_dir / 'db.sqlite3'
    target_db = data_dir / 'db.sqlite3'
    
    if source_db.exists() and not target_db.exists():
        print("📋 Initialisation de la base de données...")
        shutil.copy2(source_db, target_db)
        print(f"✅ Base copiée vers: {target_db}")
    
    # Variables d'environnement
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    os.environ['DJANGO_DB_PATH'] = str(target_db)
    
    # Ajouter le projet au path Python
    sys.path.insert(0, str(base_dir))
    
    return str(target_db), str(data_dir)

def get_free_port():
    """Trouve un port libre"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def run_server():
    """Lance le serveur Django"""
    try:
        import django
        from django.core.management import execute_from_command_line
        
        # Configuration Django
        django.setup()
        
        # Migrations automatiques
        print("🔄 Vérification des migrations...")
        execute_from_command_line(['manage.py', 'migrate', '--verbosity=0'])
        
        # Trouver un port libre
        port = get_free_port()
        
        print(f"🚀 Démarrage sur le port {port}...")
        execute_from_command_line(['manage.py', 'runserver', f'127.0.0.1:{port}', '--noreload'])
        
    except Exception as e:
        print(f"❌ Erreur serveur: {e}")
        input("Appuyez sur Entrée pour fermer...")

def open_browser(port):
    """Ouvre le navigateur après un délai"""
    time.sleep(2)
    url = f'http://127.0.0.1:{port}/'
    print(f"🌐 Ouverture: {url}")
    webbrowser.open(url)

def main():
    print("="*60)
    print("🧠 VINELAND-II - ÉVALUATION DU COMPORTEMENT ADAPTATIF")
    print("="*60)
    
    try:
        # Configuration
        db_path, data_dir = setup_environment()
        
        print(f"📁 Données sauvées dans: {data_dir}")
        print(f"💾 Base de données: {db_path}")
        
        # Vérifier Django
        try:
            import django
            print(f"✅ Django {django.get_version()} détecté")
        except ImportError:
            print("❌ Django non trouvé!")
            print("Installez avec: pip install django")
            input("Appuyez sur Entrée...")
            return
        
        # Obtenir un port libre
        port = get_free_port()
        
        print(f"🔗 Application disponible sur: http://127.0.0.1:{port}/")
        print("⚠️  Fermez cette fenêtre pour arrêter l'application")
        print("="*60)
        
        # Ouvrir le navigateur dans un thread séparé
        threading.Thread(target=open_browser, args=(port,), daemon=True).start()
        
        # Lancer le serveur (bloquant)
        os.environ['DJANGO_PORT'] = str(port)
        run_server()
        
    except KeyboardInterrupt:
        print("\n🛑 Arrêt de l'application...")
    except Exception as e:
        print(f"❌ Erreur fatale: {e}")
        import traceback
        traceback.print_exc()
        input("Appuyez sur Entrée pour fermer...")

if __name__ == "__main__":
    main()