# 🚀 Configuration du démarrage automatique sur Windows

## Prérequis
- **Python 3.11 ou supérieur** (3.12, 3.13...)
- L'installation est automatique

---

## ⚠️ Pourquoi configurer le démarrage automatique ?

**L'application doit tourner en continu pour être accessible !**
- Sans démarrage automatique, vous devez relancer l'application à chaque redémarrage du PC
- L'application s'arrête si vous fermez le terminal
- Le démarrage automatique garantit que l'application est toujours disponible

## Option 1 : Planificateur de tâches (Recommandé)

### Pour le démarrage automatique :

1. **Ouvrir le Planificateur de tâches** (Win+R > taskschd.msc)
2. **Créer une tâche basique**
3. **Nom** : "Lancer MSSanté"
4. **Déclencheur** : "Au démarrage de l'ordinateur"
5. **Action** : "Démarrer un programme"
   - **Programme** : `cmd.exe`
   - **Arguments** : `/c "cd /d C:\chemin\vers\adressesmssante && venv\Scripts\activate.bat && python app.py"`
6. **Cocher** "Exécuter avec les privilèges les plus élevés"

### Pour la mise à jour hebdomadaire :

1. **Créer une nouvelle tâche**
2. **Nom** : "Mise à jour MSSanté"
3. **Déclencheur** : "Quotidiennement" > Choisir "Lundi"
4. **Action** : "Démarrer un programme"
   - **Programme** : `cmd.exe`
   - **Arguments** : `/c "cd /d C:\chemin\vers\adressesmssante && venv\Scripts\activate.bat && python creer_bd_mssante.py"`

## Option 2 : Dossier Démarrage

1. **Ouvrir** : Win+R > `shell:startup`
2. **Créer un raccourci** vers votre script de lancement
3. **Modifier les propriétés** du raccourci pour qu'il s'exécute en arrière-plan

## Vérification

- L'application sera accessible sur `http://votre-ip:6150`
- Vérifiez que le port 6150 n'est pas bloqué par le pare-feu Windows
- Testez en redémarrant l'ordinateur

## Dépannage

Si l'application ne démarre pas automatiquement :
1. Vérifiez les logs dans l'Observateur d'événements
2. Testez manuellement le script de lancement
3. Vérifiez les permissions de l'utilisateur

## Alternative : Lancement manuel

Si vous préférez lancer l'application manuellement :
- Double-clic sur `scripts-windows\lancer_base_mssante.bat`
- Gardez la fenêtre ouverte
- L'application s'arrête si vous fermez la fenêtre 