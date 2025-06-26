# 🏥 Adresses MSSanté - Moteur de recherche

Application simple pour rechercher les adresses MSSanté des professionnels de santé français.

## ✨ Fonctionnalités

- 🔍 Recherche en temps réel des professionnels de santé
- 📱 Interface web simple et intuitive
- 📋 Copie d'adresses MSSanté en un clic
- 🔄 Mise à jour automatique des données depuis l'annuaire santé
- 🌐 Accessible depuis le réseau local

## 🚀 Installation tout-en-un (Recommandé)

**Une seule commande pour tout faire : installation + base de données + lancement !**

### Windows
1. **Télécharger** et extraire le projet
2. **Double-cliquer** sur `scripts-windows\install_et_lancer_windows.bat`
3. **Attendre** que tout s'installe automatiquement
4. **L'application se lance** automatiquement dans votre navigateur

### Mac
1. **Ouvrir le Terminal** dans le dossier du projet
2. **Copier-coller** cette commande :
   ```bash
   ./scripts/install_et_lancer_mac.sh
   ```
3. **Attendre** que tout s'installe automatiquement
4. **L'application se lance** automatiquement

**Note** : Si vous avez une erreur "Permission denied", copiez-collez d'abord :
```bash
chmod +x scripts/*.sh
```

## 🔧 Installation manuelle (Optionnel)

Si vous préférez contrôler chaque étape :

### Prérequis
- **Python 3.11 ou supérieur** (3.12, 3.13...)
- L'installation est automatique, le script utilise la version par défaut de votre système

### Windows

1. **Télécharger** et extraire le projet
2. **Double-cliquer** sur `scripts-windows\install_windows.bat`
3. **Lancer** l'application avec `scripts-windows\lancer_base_mssante.bat`

### Mac

1. **Ouvrir le Terminal** dans le dossier du projet
2. **Copier-coller** cette commande :
   ```bash
   ./scripts/install_mac.sh
   ```
3. **Lancer** l'application :
   ```bash
   ./scripts/lancer_base_mssante_mac.sh
   ```

**Note** : Si vous avez une erreur "Permission denied", copiez-collez d'abord :
```bash
chmod +x scripts/*.sh
```

## 📋 Première utilisation

1. **Lancer l'application** (voir installation ci-dessus)
2. **Mettre à jour la base** de données :
   - Windows : `scripts-windows\mise_a_jour_base_mssante.bat`
   - Mac : `./scripts/mise_a_jour_base_mssante_mac.sh`
3. **Ouvrir votre navigateur** sur l'URL affichée
4. **Rechercher** un professionnel de santé

## ⚠️ Important : L'application doit tourner en continu

**L'application doit rester active en arrière-plan pour être accessible !**

### **Comment ça marche :**
- L'application tourne dans un terminal/console
- Elle reste active tant que le terminal est ouvert
- Si vous fermez le terminal, l'application s'arrête
- L'application doit être relancée à chaque redémarrage du PC

### **Solutions pour un usage permanent :**

#### **Option 1 : Démarrage automatique (Recommandé)**
- **Windows** : Voir `TUTORIEL_WINDOWS.md`
- **Mac** : Voir `TUTORIEL_MAC.md`

#### **Option 2 : Lancement manuel**
- **Windows** : Double-clic sur `scripts-windows\lancer_base_mssante.bat`
- **Mac** : `./scripts/lancer_base_mssante_mac.sh`

### **Vérifier que l'application tourne :**
- Ouvrir `http://[IP-DU-PC]:6150` dans le navigateur
- Si la page s'affiche, l'application fonctionne
- Si "Connexion refusée", l'application n'est pas lancée

## 🔖 Accès rapide - Créer un signet

Pour éviter de retaper l'adresse à chaque fois :

### **Créer un signet dans votre navigateur :**

1. **Ouvrir l'application** dans votre navigateur
2. **Appuyer sur** `Cmd+D` (Mac) ou `Ctrl+D` (Windows)
3. **Nommer** le signet : "MSSanté" ou "Adresses MSSanté"
4. **Sauvegarder** le signet

### **Ou utiliser la barre d'adresse :**
- **Taper** `mss` dans la barre d'adresse
- **Sélectionner** l'URL de l'application dans les suggestions

### **URL à retenir :**
```
http://[IP-DE-VOTRE-ORDINATEUR]:6150
```
Exemple : `http://192.168.86.100:6150`

## 🔧 Configuration du démarrage automatique

### Windows
- Utiliser le **Planificateur de tâches** pour lancer `lancer_base_mssante.bat` au démarrage
- Programmer `mise_a_jour_base_mssante.bat` une fois par semaine

### Mac
- Utiliser **Automator** pour créer une application de démarrage
- Utiliser **crontab** pour la mise à jour hebdomadaire

## 🛠️ Utilisation

1. **Remplir** un ou plusieurs champs de recherche
2. **Attendre** les résultats en temps réel
3. **Cliquer** sur "Copier l'adresse MSSanté" pour copier l'adresse
4. **Utiliser** l'adresse dans votre logiciel de messagerie

## 📁 Structure

```
adressesmssante/
├── app.py                 # Application principale
├── creer_bd_mssante.py    # Mise à jour des données
├── config.py              # Configuration
├── requirements.txt       # Dépendances
├── scripts/               # Scripts Mac/Linux
├── scripts-windows/       # Scripts Windows
└── templates/             # Interface web
```

## 🔒 Sécurité

- Application locale/réseau local uniquement
- Aucune donnée personnelle stockée
- Données officielles de l'annuaire santé 