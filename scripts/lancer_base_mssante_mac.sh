#!/bin/bash

echo "🚀 Lancement de l'application Adresses MSSanté"

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Lancez d'abord l'installation : ./scripts/install_mac.sh"
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier la base de données
if [ ! -f "adresses.db" ]; then
    echo "⚠️  Base de données manquante. Lancez d'abord la mise à jour :"
    echo "   ./scripts/mise_a_jour_base_mssante_mac.sh"
    echo ""
    read -p "Continuer quand même ? (o/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Oo]$ ]]; then
        exit 1
    fi
fi

echo "🏥 Démarrage de l'application..."
python app.py 