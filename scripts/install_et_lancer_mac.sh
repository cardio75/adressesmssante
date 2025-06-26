#!/bin/bash

echo "🚀 Installation et lancement automatique - Adresses MSSanté"
echo "=========================================================="

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ ERREUR: Python 3 n'est pas installé"
    echo "Installez Python 3.11+ depuis https://python.org"
    exit 1
fi

echo "✅ Python détecté: $(python3 --version)"

# Supprimer l'ancien venv s'il existe
if [ -d "venv" ]; then
    echo "🗑️  Suppression de l'ancien environnement virtuel..."
    rm -rf venv
fi

# Créer l'environnement virtuel
echo "🔧 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer et installer
echo "📦 Installation des dépendances..."
source venv/bin/activate
pip install --upgrade pip
pip install Flask>=2.3.3 playwright>=1.52.0

# Installer Playwright
echo "🌐 Installation de Playwright..."
python -m playwright install

# Créer la base de données
echo "🗄️  Création de la base de données..."
python creer_bd_mssante.py

# Vérifier que la base existe
if [ ! -f "adresses.db" ]; then
    echo "❌ ERREUR: La base de données n'a pas été créée"
    exit 1
fi

echo "✅ Base de données créée avec succès"

# Lancer l'application
echo "🚀 Lancement de l'application..."
echo "🌐 L'application sera accessible sur http://$(hostname -I | awk '{print $1}'):6150"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter l'application"
echo ""

python app.py 