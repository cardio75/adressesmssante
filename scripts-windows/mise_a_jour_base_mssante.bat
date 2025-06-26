@echo off
echo Mise a jour de la base de donnees Adresses MSSante

cd ..

if not exist "venv" (
    echo ERREUR: Lancez d'abord l'installation : scripts-windows\install_windows.bat
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo Telechargement et traitement des donnees...
echo Cela peut prendre plusieurs minutes...

python creer_bd_mssante.py

if %errorlevel% equ 0 (
    echo Mise a jour terminee !
    echo Lancez l'application : scripts-windows\lancer_base_mssante.bat
) else (
    echo Erreur lors de la mise a jour
)
pause 