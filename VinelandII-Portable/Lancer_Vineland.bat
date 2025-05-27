@echo off
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
