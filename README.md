# 🏥 Adresses MSSanté - Moteur de recherche

Application simple pour rechercher les adresses MSSanté des professionnels de santé français.

## ✨ Fonctionnalités

- 🔍 Recherche en temps réel des professionnels de santé
- 📱 Interface web simple et intuitive
- 📋 Copie d'adresses MSSanté en un clic
- 🔄 Mise à jour de la base depuis l'application
- 🌐 Accessible depuis le réseau local
- 📦 Version autonome sans installation de Python

## 🚀 Installation recommandée pour les utilisateurs

Cette option ne nécessite pas d'installer Python.

Téléchargements officiels :
https://github.com/cardio75/adressesmssante/releases/latest

### Mac

1. Télécharger `Adresses-MSSante-macOS-arm64.dmg`
2. Ouvrir le DMG
3. Glisser `Adresses MSSante.app` vers `Applications`
4. Lancer l'application depuis `Applications`

Au premier lancement, macOS peut afficher un avertissement car l'application n'est pas signée. Dans ce cas : clic droit sur l'application, puis `Ouvrir`.

### Windows

1. Télécharger le zip Windows adapté depuis la page des releases :
   - `Adresses-MSSante-Windows-x64.zip` pour la plupart des PC Windows Intel/AMD
   - `Adresses-MSSante-Windows-arm64.zip` pour Windows ARM
2. Ouvrir `Adresses MSSante.exe`
3. L'application ouvre automatiquement le navigateur

Windows SmartScreen peut afficher un avertissement car l'exécutable n'est pas signé.

## 🛠️ Utilisation

1. Lancer l'application
2. Le navigateur s'ouvre sur `http://localhost:6150`
3. Remplir un ou plusieurs champs de recherche
4. Cliquer sur `Copier` pour copier l'adresse MSSanté

## 🔄 Mise à jour de la base

La base incluse dans l'application peut être mise à jour directement depuis l'interface.

1. Ouvrir l'application
2. Cliquer sur `Mettre à jour la base`
3. Attendre la fin du téléchargement et de la reconstruction

L'application télécharge la dernière extraction officielle depuis data.gouv.fr. Une connexion internet est nécessaire. En version autonome, la base mise à jour est stockée dans le dossier utilisateur :

- Mac : `~/Library/Application Support/Adresses MSSante/adresses.db`
- Windows : `%APPDATA%\Adresses MSSante\adresses.db`

## 📦 Générer une version autonome

Ces commandes sont destinées à la personne qui prépare les fichiers à distribuer.

### Mac
```bash
./packaging/build_macos.sh
./packaging/build_macos_dmg.sh
```

Fichiers générés :
- `dist/Adresses MSSante.app`
- `dist/Adresses-MSSante-macOS-arm64.dmg`

### Windows
```bat
packaging\build_windows.bat
```

Fichier généré : `dist\Adresses MSSante\Adresses MSSante.exe`

Pour préparer un zip Windows à publier dans une release :

```powershell
Compress-Archive -Path "dist\Adresses MSSante" -DestinationPath "dist\Adresses-MSSante-Windows-x64.zip" -Force
```

Adaptez le nom du zip à l'architecture de la machine de build : `Windows-x64` pour un PC Intel/AMD, `Windows-arm64` pour Windows ARM.

Chaque build embarque Python, Flask, l'interface web et une copie initiale de `adresses.db`. Le build Mac doit être généré sur Mac, et le build Windows sur Windows. PyInstaller produit un binaire pour l'architecture du Python utilisé.

## 🧑‍💻 Installation depuis le code source

Cette option nécessite Python et sert surtout au développement ou au dépannage.

### Installation tout-en-un

Mac :
```bash
./scripts/install_et_lancer_mac.sh
```

Windows :
```bat
scripts-windows\install_et_lancer_windows.bat
```

### Installation manuelle

Prérequis : Python 3.11 ou supérieur.

Mac :
```bash
./scripts/install_mac.sh
./scripts/lancer_base_mssante_mac.sh
```

Windows :
```bat
scripts-windows\install_windows.bat
scripts-windows\lancer_base_mssante.bat
```

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

## 📁 Structure

```
adressesmssante/
├── app.py                 # Application principale
├── creer_bd_mssante.py    # Mise à jour des données
├── config.py              # Configuration
├── requirements.txt       # Dépendances
├── packaging/             # Builds autonomes PyInstaller
├── scripts/               # Scripts Mac/Linux
├── scripts-windows/       # Scripts Windows
└── templates/             # Interface web
```

## 🔒 Sécurité

- Application locale/réseau local uniquement
- Aucune donnée personnelle stockée
- Données officielles de l'annuaire santé
