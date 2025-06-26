@echo off
echo Installation de l'application Adresses MSSante pour Windows
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

if not exist "requirements.txt" (
    echo ERREUR: Fichier requirements.txt manquant
    pause
    exit /b 1
)

echo requirements.txt trouve

echo Creation de l'environnement virtuel...
python -m venv venv

echo Installation des dependances...
call venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt

echo Installation de Playwright...
python -m playwright install

echo.
echo Installation terminee !
echo Pour demarrer : scripts-windows\lancer_base_mssante.bat
echo Pour mettre a jour : scripts-windows\mise_a_jour_base_mssante.bat
pause 