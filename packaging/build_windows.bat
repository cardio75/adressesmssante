@echo off
setlocal

cd /d "%~dp0\.."

set APP_NAME=Adresses MSSante
set PYTHON_BIN=python

%PYTHON_BIN% --version >nul 2>&1
if errorlevel 1 (
    echo Python 3 est requis pour generer le build Windows.
    pause
    exit /b 1
)

echo Creation de l'environnement de build...
%PYTHON_BIN% -m venv .build-venv
call .build-venv\Scripts\activate.bat

echo Installation des dependances de build...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

if not exist "adresses.db" (
    echo Base adresses.db absente, creation de la base...
    python creer_bd_mssante.py
)

if not exist "adresses.db" (
    echo Erreur: adresses.db n'a pas ete creee.
    pause
    exit /b 1
)

echo Generation de l'application Windows...
pyinstaller ^
    --noconfirm ^
    --clean ^
    --windowed ^
    --name "%APP_NAME%" ^
    --add-data "templates;templates" ^
    --add-data "static;static" ^
    --add-data "adresses.db;." ^
    app.py

echo.
echo Build termine:
echo dist\%APP_NAME%\%APP_NAME%.exe
pause
