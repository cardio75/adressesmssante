@echo off
echo Lancement de l'application Adresses MSSante

cd ..

if not exist "venv" (
    echo ERREUR: Lancez d'abord l'installation : scripts-windows\install_windows.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

if not exist "adresses.db" (
    echo ATTENTION: Base de donnees manquante. Lancez d'abord la mise a jour :
    echo    scripts-windows\mise_a_jour_base_mssante.bat
    echo.
    set /p response="Continuer quand meme ? (o/n) "
    if /i not "%response%"=="o" exit /b 1
)

echo Demarrage de l'application...
python app.py 