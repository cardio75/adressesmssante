#!/bin/bash

echo "🏥 Installation de l'application Adresses MSSanté pour Mac"
echo "=================================================="

# Vérifier que Python est installé
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer depuis https://python.org"
    echo "   Ou utilisez Homebrew : brew install python3"
    exit 1
fi

echo "✅ Python détecté : $(python3 --version)"

# Vérifier et corriger les permissions automatiquement
echo "🔧 Vérification des permissions..."
chmod +x scripts/*.sh 2>/dev/null

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer et installer
echo "📥 Installation des dépendances..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📋 Pour démarrer l'application :"
echo "   ./scripts/lancer_base_mssante_mac.sh"
echo ""
echo "🔄 Pour mettre à jour la base de données :"
echo "   ./scripts/mise_a_jour_base_mssante_mac.sh"
echo ""
echo "💡 Conseil : Créez un alias dans votre Terminal pour un accès rapide" 
