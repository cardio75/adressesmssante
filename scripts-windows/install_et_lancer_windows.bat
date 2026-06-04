@echo off
echo Installation et lancement automatique - Adresses MSSante
echo ========================================================

cd ..

python --version >nul 2>&1
if errorlevel 1 (
    echo ERREUR: Python n'est pas installe
    echo Installez Python depuis https://python.org
    pause
    exit /b 1
)

echo Python detecte
python --version

if exist "venv" (
    echo Suppression de l'ancien environnement virtuel...
    rmdir /s /q venv
)

echo Creation de l'environnement virtuel...
python -m venv venv

echo Installation des dependances...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install "Flask>=2.3.3"

echo Creation de la base de donnees...
python creer_bd_mssante.py

if not exist "adresses.db" (
    echo ERREUR: La base de donnees n'a pas ete creee
    pause
    exit /b 1
)

echo Base de donnees creee avec succes

echo.
echo Lancement de l'application...
echo L'application sera accessible sur le reseau local
echo.
echo Appuyez sur Ctrl+C pour arreter l'application
echo.

python app.py 
