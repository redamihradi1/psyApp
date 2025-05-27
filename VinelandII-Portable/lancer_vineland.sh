#!/bin/bash
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
