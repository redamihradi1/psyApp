#!/usr/bin/env python3
import os
import sys
import time
import datetime
import socket
import threading
import webbrowser
import shutil
import signal

def get_app_dir():
    """Retourne le dossier où se trouve l'exécutable (adapté macOS)"""
    if getattr(sys, 'frozen', False):
        # Sur macOS, l'app peut être dans un bundle .app
        if sys.executable.endswith('MacOS/VinelandII-Evaluator'):
            return os.path.dirname(os.path.dirname(os.path.dirname(sys.executable)))
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def create_log(message):
    """Écrit dans un fichier log"""
    log_dir = os.path.expanduser("~/Library/Logs/VinelandII")
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "vineland_debug.log")
    
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

def signal_handler(sig, frame):
    """Gestionnaire pour fermeture propre"""
    create_log("Application fermée par l'utilisateur")
    print("\n👋 Fermeture de l'application...")
    sys.exit(0)

if __name__ == "__main__":
    # Gestionnaire de signal pour Cmd+C
    signal.signal(signal.SIGINT, signal_handler)
    
    try:
        create_log("🍎 Lancement de l'application Vineland-II sur macOS")

        # Import Django après les vérifications
        import django
        from django.core.management import execute_from_command_line

        # Obtenir le chemin de base
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        create_log(f"📁 Dossier de base : {base_dir}")

        # Base de données : dans le dossier utilisateur sur macOS
        app_support_dir = os.path.expanduser("~/Library/Application Support/VinelandII")
        os.makedirs(app_support_dir, exist_ok=True)
        
        source_db = os.path.join(base_dir, 'db.sqlite3')
        target_db = os.path.join(app_support_dir, 'db.sqlite3')
        
        if not os.path.exists(target_db) and os.path.exists(source_db):
            create_log("📊 Copie initiale de la base de données")
            shutil.copy2(source_db, target_db)

        os.environ['DJANGO_DB_PATH'] = target_db
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
        sys.path.insert(0, base_dir)

        # Dossier des templates
        os.environ['DJANGO_TEMPLATE_DIRS'] = os.path.join(base_dir, 'templates')

        # Trouver l'IP locale (adapté macOS)
        def get_local_ip():
            try:
                # Méthode principale
                s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
                s.close()
                return local_ip
            except:
                try:
                    # Méthode alternative pour macOS
                    import subprocess
                    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
                    for line in result.stdout.split('\n'):
                        if 'inet ' in line and '127.0.0.1' not in line and 'inet 169.254' not in line:
                            ip = line.split('inet ')[1].split(' ')[0]
                            if ip.count('.') == 3:
                                return ip
                except:
                    pass
                return '127.0.0.1'

        local_ip = get_local_ip()
        create_log(f"🌐 IP locale : {local_ip}")

        # Lancer le serveur Django
        def run_django_server():
            create_log("🚀 Démarrage du serveur Django")
            django.setup()
            
            # Migrations automatiques
            try:
                create_log("🔄 Exécution des migrations")
                execute_from_command_line(['', 'migrate', '--verbosity=0'])
            except Exception as e:
                create_log(f"⚠️  Erreur migrations : {str(e)}")
            
            execute_from_command_line(['', 'runserver', f'{local_ip}:8000', '--noreload'])

        # Ouvrir le navigateur automatiquement
        def open_browser():
            time.sleep(3)
            url = f'http://{local_ip}:8000/'
            create_log(f"🌐 Ouverture navigateur : {url}")
            webbrowser.open(url)

        # Interface utilisateur améliorée pour macOS
        print("\n" + "="*60)
        print("🧠 VINELAND-II - ÉVALUATION COMPORTEMENT ADAPTATIF")
        print("🍎 Version macOS")
        print("="*60)
        print(f"🌐 Application accessible à : http://{local_ip}:8000/")
        print(f"📊 Base de données : {app_support_dir}")
        print(f"📝 Logs : ~/Library/Logs/VinelandII/vineland_debug.log")
        print("⚠️  Utilisez Cmd+C pour arrêter proprement")
        print("="*60)

        # Démarrage des threads
        django_thread = threading.Thread(target=run_django_server, daemon=True)
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        
        django_thread.start()
        browser_thread.start()

        # Boucle principale avec gestion des signaux
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            signal_handler(signal.SIGINT, None)

    except Exception as e:
        error_dir = os.path.expanduser("~/Library/Logs/VinelandII")
        os.makedirs(error_dir, exist_ok=True)
        error_path = os.path.join(error_dir, "vineland_error.log")
        
        with open(error_path, "w") as f:
            f.write(f"❌ Erreur Vineland : {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
        
        print(f"❌ Erreur : {str(e)}")
        print(f"📝 Détails dans : {error_path}")
        time.sleep(10)
        sys.exit(1)