# Installation et utilisation - Windows

## Installation recommandee

Cette installation ne demande pas Python.

1. Telecharger la version Windows generee
2. Extraire le zip si necessaire
3. Lancer `Adresses MSSante.exe`

Windows SmartScreen peut afficher un avertissement car l'executable n'est pas signe.

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
%APPDATA%\Adresses MSSante\adresses.db
```

## Installation depuis le code source

Cette option sert surtout au developpement ou au depannage. Elle necessite Python 3.11 ou superieur.

```bat
cd C:\chemin\vers\adressesmssante
scripts-windows\install_windows.bat
scripts-windows\lancer_base_mssante.bat
```

Pour mettre a jour la base en ligne de commande :

```bat
scripts-windows\mise_a_jour_base_mssante.bat
```

## Generer l'executable Windows

Depuis la racine du projet, sur Windows :

```bat
packaging\build_windows.bat
```

L'executable est cree ici :

```text
dist\Adresses MSSante\Adresses MSSante.exe
```
