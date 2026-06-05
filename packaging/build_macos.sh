#!/bin/bash
set -euo pipefail

cd "$(dirname "$0")/.."

APP_NAME="Adresses MSSante"
PYTHON_BIN="${PYTHON:-python3}"

if ! command -v "$PYTHON_BIN" >/dev/null 2>&1; then
    echo "Python 3 est requis pour generer le build macOS."
    exit 1
fi

echo "Creation de l'environnement de build..."
"$PYTHON_BIN" -m venv .build-venv
source .build-venv/bin/activate

echo "Installation des dependances de build..."
python -m pip install --upgrade pip
python -m pip install -r requirements.txt pyinstaller

if [ ! -f "adresses.db" ]; then
    echo "Base adresses.db absente, creation de la base..."
    python creer_bd_mssante.py
fi

if [ ! -f "adresses.db" ]; then
    echo "Erreur: adresses.db n'a pas ete creee."
    exit 1
fi

echo "Generation de l'application macOS..."
pyinstaller \
    --noconfirm \
    --clean \
    --windowed \
    --name "$APP_NAME" \
    --add-data "templates:templates" \
    --add-data "static:static" \
    --add-data "adresses.db:." \
    app.py

echo ""
echo "Build termine:"
echo "dist/$APP_NAME.app"
