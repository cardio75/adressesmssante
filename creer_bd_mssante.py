import os
import re
import sqlite3
import csv
import unicodedata
import zipfile
from datetime import datetime
from playwright.sync_api import sync_playwright

def normalize_text(text):
    if text is None:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def download_and_extract():
    with sync_playwright() as p:
        # Démarrer le navigateur
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(accept_downloads=True)
        page = context.new_page()

        # Naviguer vers la page spécifiée
        page.goto("https://annuaire.sante.fr/web/site-pro/extractions-mss")

        # Attendre que la table soit chargée
        page.wait_for_selector("table")

        # Sélectionner le bouton "Télécharger" dans la dernière colonne de la dernière ligne
        download_button = page.query_selector("table tbody tr:last-child td:last-child a")

        if download_button:
            # Gérer le téléchargement
            with page.expect_download() as download_info:
                download_button.click()
            download = download_info.value

            # Enregistrer le fichier téléchargé dans le répertoire courant
            download_path = os.path.join(os.getcwd(), download.suggested_filename)
            download.save_as(download_path)

            # Décompresser le fichier téléchargé
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())

            # Extraire la date du nom du fichier
            filename = os.path.basename(download_path)
            date_match = re.search(r'(\d{8})\d{4}\.zip$', filename)
            if date_match:
                extraction_date = date_match.group(1)  # 'YYYYMMDD'
            else:
                extraction_date = ''

            # Supprimer le fichier ZIP téléchargé
            os.remove(download_path)

            print("Téléchargement et décompression terminés.")
            return extraction_date
        else:
            print("Bouton 'Télécharger' introuvable.")
            return ''

        # Fermer le navigateur
        browser.close()

def update_database(extraction_date):
    # Trouver le fichier texte extrait (ignorer requirements.txt et autres fichiers parasites)
    extracted_files = [f for f in os.listdir('.') if f.endswith('.txt') and 'Extraction_Correspondance_MSSante' in f]
    if not extracted_files:
        # Fallback: chercher n'importe quel fichier .txt sauf requirements.txt
        extracted_files = [f for f in os.listdir('.') if f.endswith('.txt') and f != 'requirements.txt']
    
    if not extracted_files:
        print("Aucun fichier texte trouvé après décompression.")
        return
    else:
        data_file = extracted_files[0]
        print(f"📁 Fichier source trouvé : {data_file}")

    # Vérifier la taille du fichier
    file_size = os.path.getsize(data_file)
    print(f"📊 Taille du fichier : {file_size:,} octets ({file_size/1024/1024:.1f} MB)")

    # Connexion à la base de données (création si elle n'existe pas)
    conn = sqlite3.connect('adresses.db')
    cursor = conn.cursor()

    # Activer les clés étrangères
    cursor.execute('PRAGMA foreign_keys = ON;')

    # Vérifier si la table FTS5 existe déjà
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='adresses';")
    table_exists = cursor.fetchone()

    if not table_exists:
        print("🗄️ Création de la table adresses...")
        # Créer la table virtuelle FTS5 avec la colonne extraction_date
        cursor.execute('''
        CREATE VIRTUAL TABLE adresses USING fts5(
            raison_sociale,
            nom_exercice,
            prenom_exercice,
            adresse_complete,
            code_postal,
            ville,
            adresse_mssante,
            region,
            specialty,
            extraction_date,
            tokenize = "unicode61 remove_diacritics 1"
        )
        ''')
    else:
        print("🗄️ Table adresses existante détectée...")
        # Vérifier si la colonne extraction_date existe
        cursor.execute("PRAGMA table_info(adresses);")
        columns = [info[1] for info in cursor.fetchall()]
        if 'extraction_date' not in columns:
            print("🔄 Mise à jour de la structure de la table...")
            # Supprimer et recréer la table pour ajouter la nouvelle colonne
            cursor.execute('DROP TABLE adresses;')
            cursor.execute('''
            CREATE VIRTUAL TABLE adresses USING fts5(
                raison_sociale,
                nom_exercice,
                prenom_exercice,
                adresse_complete,
                code_postal,
                ville,
                adresse_mssante,
                region,
                specialty,
                extraction_date,
                tokenize = "unicode61 remove_diacritics 1"
            )
            ''')
        else:
            print("🗑️ Vidage de la table existante...")
            # Vider la table existante pour mettre à jour les données
            cursor.execute('DELETE FROM adresses;')

    # Charger les données depuis le fichier texte extrait
    print("📥 Lecture et insertion des données...")
    lines_read = 0
    lines_inserted = 0
    lines_skipped = 0
    
    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='|')
            
            # Afficher les en-têtes pour debug
            print(f"📋 En-têtes détectés : {list(reader.fieldnames)}")
            
            for row in reader:
                lines_read += 1
                
                if lines_read % 10000 == 0:
                    print(f"⏳ Traitement en cours... {lines_read:,} lignes lues, {lines_inserted:,} insérées")
                
                try:
                    # Exclure les pharmacies basées sur "pharmacrypt" dans l'adresse e-mail
                    adresse_bal = row.get('Adresse BAL', '').lower()
                    if 'pharmacrypt' in adresse_bal:
                        lines_skipped += 1
                        continue  # Ignorer cette entrée si c'est une pharmacie

                    # Extraction des champs nécessaires
                    raison_sociale = row.get('Raison Sociale structure BAL', '')
                    nom_exercice = row.get('Nom d\'exercice', '')
                    prenom_exercice = row.get('Prénom d\'exercice', '')
                    code_postal = row.get('Code postal structure BAL', '')
                    ville = row.get('L6LIGNEACHEMINEMENT structure BAL', '')
                    adresse_mssante = row.get('Adresse BAL', '')
                    region = row.get('Département structure BAL', '')
                    specialty = row.get('Libellé savoir-faire', '')

                    # Construction de l'adresse complète
                    adresse_complete = ', '.join(filter(None, [
                        row.get('L2COMPLEMENTLOCALISATION structure BAL', ''),
                        row.get('L3COMPLEMENTDISTRIBUTION structure BAL', ''),
                        ' '.join(filter(None, [
                            row.get('L4NUMEROVOIE structure BAL', ''),
                            row.get('L4COMPLEMENTNUMEROVOIE structure BAL', ''),
                            row.get('NL4TYPEVOIE structure BAL', ''),
                            row.get('L4LIBELLEVOIE structure BAL', '')
                        ])),
                        row.get('L5LIEUDITMENTION structure BAL', ''),
                        row.get('L6LIGNEACHEMINEMENT structure BAL', ''),
                        code_postal,
                        region
                    ]))

                    # Traiter toutes les lignes, même celles sans nom/prénom (organisations)
                    # Si pas de nom/prénom, utiliser la raison sociale
                    if not nom_exercice and not prenom_exercice:
                        nom_exercice = raison_sociale
                        prenom_exercice = ''

                    # Insertion des données dans la table FTS5 avec la date d'extraction
                    cursor.execute('''
                    INSERT INTO adresses (
                        raison_sociale,
                        nom_exercice,
                        prenom_exercice,
                        adresse_complete,
                        code_postal,
                        ville,
                        adresse_mssante,
                        region,
                        specialty,
                        extraction_date
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''', (
                        raison_sociale,
                        nom_exercice,
                        prenom_exercice,
                        adresse_complete,
                        code_postal,
                        ville,
                        adresse_mssante,
                        region,
                        specialty,
                        extraction_date
                    ))
                    
                    lines_inserted += 1
                    
                except Exception as e:
                    print(f"❌ Erreur à la ligne {lines_read}: {e}")
                    print(f"   Données: {row}")
                    continue

    except Exception as e:
        print(f"❌ Erreur lors de la lecture du fichier: {e}")
        conn.close()
        return

    conn.commit()
    conn.close()

    print(f"✅ Traitement terminé:")
    print(f"   📖 Lignes lues : {lines_read:,}")
    print(f"   ➕ Lignes insérées : {lines_inserted:,}")
    print(f"   ⏭️ Lignes ignorées (pharmacies) : {lines_skipped:,}")

    # Supprimer le fichier texte extrait
    os.remove(data_file)

    print('La base de données a été mise à jour avec succès.')

if __name__ == '__main__':
    # Vérifier si un fichier d'extraction existe déjà
    existing_files = [f for f in os.listdir('.') if f.endswith('.txt') and 'Extraction_Correspondance_MSSante' in f]
    
    if existing_files:
        print(f"Utilisation du fichier existant : {existing_files[0]}")
        # Extraire la date du nom du fichier existant
        filename = existing_files[0]
        date_match = re.search(r'(\d{8})\d{4}\.txt$', filename)
        if date_match:
            extraction_date = date_match.group(1)  # 'YYYYMMDD'
        else:
            extraction_date = datetime.now().strftime('%Y%m%d')
    else:
        print("Téléchargement d'un nouveau fichier...")
        extraction_date = download_and_extract()
    
    if extraction_date:
        update_database(extraction_date)
        # Afficher la date d'extraction formatée
        date_formatee = datetime.strptime(extraction_date, '%Y%m%d').strftime('%d/%m/%Y')
        print(f'Date d\'extraction des données : {date_formatee}')
    else:
        print("Échec du téléchargement ou de l'extraction du fichier.")
