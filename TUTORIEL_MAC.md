# 📱 Tutoriel d'installation et d'utilisation - Mac

## 🚀 Installation rapide

### Prérequis
- **Python 3.11 ou supérieur** (3.12, 3.13...)
- L'installation est automatique

### Étape 1 : Préparer l'environnement
1. **Ouvrir le Terminal** (⌘ + Espace, taper "Terminal")
2. **Naviguer** vers le dossier du projet :
   ```bash
   cd /chemin/vers/adressesmssante
   ```

### Étape 2 : Installation automatique
**Copier-coller** cette commande dans le Terminal :
```bash
./scripts/install_mac.sh
```

Le script va automatiquement :
- ✅ Vérifier et corriger les permissions
- ✅ Installer Python si nécessaire
- ✅ Créer l'environnement virtuel
- ✅ Installer toutes les dépendances
- ✅ Configurer Playwright

### Étape 3 : Démarrer l'application
**Copier-coller** cette commande :
```bash
./scripts/lancer_base_mssante_mac.sh
```

## 🔧 En cas de problème

### Erreur "Permission denied"
Si vous avez une erreur de permission, copiez-collez :
```bash
chmod +x scripts/*.sh
```
Puis relancez l'installation.

### Python non installé
Si Python n'est pas détecté :
1. **Télécharger** Python depuis https://python.org
2. **Ou utiliser** Homebrew : `brew install python3`

## 📋 Utilisation quotidienne

### Démarrer l'application
```bash
./scripts/lancer_base_mssante_mac.sh
```

### Mettre à jour la base
```bash
./scripts/mise_a_jour_base_mssante_mac.sh
```

## 🎯 Accès rapide

### Option 1 : Alias Terminal
Ajouter dans `~/.zshrc` ou `~/.bash_profile` :
```bash
alias mssante="cd /chemin/vers/adressesmssante && ./scripts/lancer_base_mssante_mac.sh"
```

### Option 2 : Script de bureau
Créer un fichier `Lancer_MSSante.command` :
```bash
#!/bin/bash
cd /chemin/vers/adressesmssante
./scripts/lancer_base_mssante_mac.sh
```

Puis double-cliquer dessus.

## 🔄 Démarrage automatique

### Méthode 1 : Script de bureau
1. **Créer** le script `Lancer_MSSante.command` (voir ci-dessus)
2. **Rendre exécutable** : `chmod +x Lancer_MSSante.command`
3. **Double-cliquer** pour lancer

### Méthode 2 : Alias Terminal
1. **Ouvrir** `~/.zshrc` : `nano ~/.zshrc`
2. **Ajouter** : `alias mssante="cd /chemin/vers/adressesmssante && ./scripts/lancer_base_mssante_mac.sh"`
3. **Sauvegarder** : Ctrl+X, Y, Entrée
4. **Recharger** : `source ~/.zshrc`

## 📱 Accès depuis le réseau

L'application est accessible depuis :
- **Votre Mac** : http://localhost:6150
- **Autres appareils** : http://VOTRE_IP:6150

Pour trouver votre IP : `ifconfig | grep "inet " | grep -v 127.0.0.1`

## 🛠️ Dépannage

### L'application ne démarre pas
1. **Vérifier** que le Terminal est dans le bon dossier
2. **Relancer** : `./scripts/lancer_base_mssante_mac.sh`
3. **Vérifier** les logs d'erreur

### Erreur de port
Si le port 6150 est occupé :
1. **Arrêter** l'application : Ctrl+C
2. **Attendre** quelques secondes
3. **Relancer** l'application

### Base de données corrompue
```bash
./scripts/mise_a_jour_base_mssante_mac.sh
```

## 💡 Conseils

- **Gardez** le Terminal ouvert pendant l'utilisation
- **Créez** un signet dans votre navigateur pour un accès rapide
- **Utilisez** l'alias pour un démarrage plus rapide
- **Sauvegardez** régulièrement votre base de données 