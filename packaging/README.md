# Packaging PyInstaller

Ces scripts generent une version autonome de l'application, avec Python et les dependances embarques.

## macOS

Depuis la racine du projet :

```bash
./packaging/build_macos.sh
```

Le resultat est cree dans `dist/Adresses MSSante.app`.

Pour creer aussi un DMG avec un raccourci vers Applications :

```bash
./packaging/build_macos_dmg.sh
```

Le resultat est cree dans `dist/Adresses-MSSante-macOS-arm64.dmg`.

## Windows

Depuis la racine du projet, dans `cmd.exe` :

```bat
packaging\build_windows.bat
```

Le resultat est cree dans `dist\Adresses MSSante\Adresses MSSante.exe`.

Pour creer le zip a publier dans une release GitHub :

```powershell
Compress-Archive -Path "dist\Adresses MSSante" -DestinationPath "dist\Adresses-MSSante-Windows-x64.zip" -Force
```

Le dossier zippe doit contenir `Adresses MSSante.exe` et le dossier `_internal`. Ne publiez pas seulement le fichier `.exe`.

## Notes

- Le build macOS doit etre lance sur macOS.
- Le build Windows doit etre lance sur Windows.
- PyInstaller genere un build pour l'architecture du Python utilise : `Windows-x64` sur un PC Intel/AMD, `Windows-arm64` sur Windows ARM.
- Si `adresses.db` n'existe pas, le script lance `creer_bd_mssante.py` pour la creer avant le build.
- `adresses.db` est incluse comme base initiale pour eviter aux utilisateurs d'installer Python ou de telecharger la base au premier lancement.
- Au premier lancement de l'app autonome, la base incluse est copiee dans le dossier utilisateur.
- Les mises a jour lancees depuis le bouton `Mettre a jour la base` modifient cette copie utilisateur, pas le bundle `.app`.
- Sans signature, macOS Gatekeeper et Windows SmartScreen peuvent afficher un avertissement au premier lancement.
