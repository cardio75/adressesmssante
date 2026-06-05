# Installation et utilisation - Mac

## Installation recommandee

Cette installation ne demande pas Python.

1. Telecharger `Adresses-MSSante-macOS-arm64.dmg`
2. Ouvrir le fichier DMG
3. Glisser `Adresses MSSante.app` vers `Applications`
4. Ouvrir `Adresses MSSante.app`

Au premier lancement, macOS peut bloquer l'application car elle n'est pas signee. Dans ce cas :

1. Ouvrir le dossier `Applications`
2. Faire clic droit sur `Adresses MSSante.app`
3. Cliquer sur `Ouvrir`
4. Confirmer l'ouverture

## Utilisation

L'application ouvre automatiquement le navigateur sur :

```text
http://localhost:6150
```

Pour un autre appareil du reseau local, utiliser l'adresse affichee au demarrage, par exemple :

```text
http://192.168.x.x:6150
```

## Mise a jour de la base

La mise a jour se fait directement dans l'application :

1. Ouvrir l'application
2. Cliquer sur `Mettre a jour la base`
3. Attendre le message de fin

Une connexion internet est necessaire. La base mise a jour est stockee dans :

```text
~/Library/Application Support/Adresses MSSante/adresses.db
```

## Installation depuis le code source

Cette option sert surtout au developpement ou au depannage. Elle necessite Python 3.11 ou superieur.

```bash
cd /chemin/vers/adressesmssante
./scripts/install_mac.sh
./scripts/lancer_base_mssante_mac.sh
```

Pour mettre a jour la base en ligne de commande :

```bash
./scripts/mise_a_jour_base_mssante_mac.sh
```

## Generer le DMG

Depuis la racine du projet :

```bash
./packaging/build_macos.sh
./packaging/build_macos_dmg.sh
```

Le DMG est cree ici :

```text
dist/Adresses-MSSante-macOS-arm64.dmg
```
