import os
import sys
import time
import datetime
import socket
import threading
import webbrowser
import shutil

def get_app_dir():
    """Retourne le dossier où se trouve l'exécutable"""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

def create_log(message):
    """Écrit dans un fichier log"""
    log_path = os.path.join(get_app_dir(), "vineland_debug_log.txt")
    with open(log_path, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"[{timestamp}] {message}\n")

if __name__ == "__main__":
    try:
        create_log("Lancement de l'application Vineland-II")

        # Import Django après les vérifications
        import django
        from django.core.management import execute_from_command_line

        # Obtenir le chemin de base
        if getattr(sys, 'frozen', False):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        create_log(f"Dossier de base : {base_dir}")

        # Base de données : copie locale si elle n'existe pas encore
        source_db = os.path.join(base_dir, 'db.sqlite3')
        target_db = os.path.join(get_app_dir(), 'db.sqlite3')
        if not os.path.exists(target_db) and os.path.exists(source_db):
            create_log("Copie initiale de la base de données")
            shutil.copy2(source_db, target_db)

        os.environ['DJANGO_DB_PATH'] = target_db
        os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
        sys.path.insert(0, base_dir)

        # Dossier des templates
        os.environ['DJANGO_TEMPLATE_DIRS'] = os.path.join(base_dir, 'templates')

        # Trouver l'IP locale
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
        except:
            local_ip = '127.0.0.1'

        create_log(f"IP locale : {local_ip}")

        # Lancer le serveur Django
        def run_django_server():
            create_log("Démarrage du serveur Django")
            django.setup()
            
            # Migrations automatiques
            try:
                create_log("Exécution des migrations")
                execute_from_command_line(['', 'migrate', '--verbosity=0'])
            except Exception as e:
                create_log(f"Erreur migrations : {str(e)}")
            
            execute_from_command_line(['', 'runserver', f'{local_ip}:8000', '--noreload'])

        # Ouvrir le navigateur automatiquement
        def open_browser():
            time.sleep(3)
            url = f'http://{local_ip}:8000/'
            create_log(f"Ouverture navigateur : {url}")
            webbrowser.open(url)

        print("="*50)
        print("🧠 VINELAND-II - ÉVALUATION COMPORTEMENT ADAPTATIF")
        print("="*50)
        print(f"📱 Application accessible à : http://{local_ip}:8000/")
        print("📋 Logs : vineland_debug_log.txt")
        print("⚠️  Fermez cette fenêtre pour arrêter")
        print("="*50)

        threading.Thread(target=run_django_server, daemon=True).start()
        open_browser()

        # Boucle infinie
        while True:
            time.sleep(1)

    except Exception as e:
        error_path = os.path.join(get_app_dir(), "vineland_error_log.txt")
        with open(error_path, "w") as f:
            f.write(f"Erreur Vineland : {str(e)}\n")
            import traceback
            f.write(traceback.format_exc())
        print(f"Erreur : {str(e)} (voir {error_path})")
        time.sleep(10)
        sys.exit(1)