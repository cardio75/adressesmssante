#!/bin/bash

echo "🔄 Mise à jour de la base de données Adresses MSSanté"

# Vérifier l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "❌ Lancez d'abord l'installation : ./scripts/install_mac.sh"
    exit 1
fi

# Activer l'environnement virtuel
source venv/bin/activate

echo "📥 Téléchargement et traitement des données..."
echo "⏳ Cela peut prendre plusieurs minutes..."

python creer_bd_mssante.py

if [ $? -eq 0 ]; then
    echo "✅ Mise à jour terminée !"
    echo "🚀 Lancez l'application : ./scripts/lancer_base_mssante_mac.sh"
else
    echo "❌ Erreur lors de la mise à jour"
    exit 1
fi 