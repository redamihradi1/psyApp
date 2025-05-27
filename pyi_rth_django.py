# pyi_rth_django.py - Runtime hook pour Django
import os
import sys

# Configurer Django avant qu'il ne soit utilisé
if not os.environ.get('DJANGO_SETTINGS_MODULE'):
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

# Ajouter le chemin du projet
if hasattr(sys, '_MEIPASS'):
    sys.path.insert(0, sys._MEIPASS)