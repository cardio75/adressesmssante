import os
import re
import sqlite3
import csv
import unicodedata
import zipfile
import urllib.parse
import urllib.request
from datetime import datetime
from email.utils import parsedate_to_datetime

EXTRACTION_DOWNLOAD_URL = "https://www.data.gouv.fr/api/1/datasets/r/afe01105-d9a1-41fe-921f-e40ea48b2ba6"
EXTRACTION_FILE_MARKERS = (
    "extraction_correspondance_mssante",
    "extraction-correspondance-mssante",
)

def normalize_text(text):
    if text is None:
        return ''
    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    ).lower()

def is_extraction_file(filename):
    filename_normalized = normalize_text(filename)
    return filename_normalized.endswith('.txt') and any(
        marker in filename_normalized for marker in EXTRACTION_FILE_MARKERS
    )

def find_extraction_files():
    return [f for f in os.listdir('.') if is_extraction_file(f)]

def extract_date_from_download(filename, final_url='', last_modified=''):
    values = [filename, final_url]
    for value in values:
        date_match = re.search(r'(\d{8})[-_]?\d{4,6}', value or '')
        if date_match:
            return date_match.group(1)

    if last_modified:
        try:
            return parsedate_to_datetime(last_modified).strftime('%Y%m%d')
        except (TypeError, ValueError):
            pass

    return datetime.now().strftime('%Y%m%d')

def filename_from_response(response):
    filename = response.headers.get_filename()
    if filename:
        return os.path.basename(filename)

    parsed_url = urllib.parse.urlparse(response.geturl())
    filename = os.path.basename(parsed_url.path)
    return filename or 'extraction-correspondance-mssante.txt'

def download_and_extract():
    try:
        print(f"📥 Téléchargement depuis data.gouv.fr...")
        with urllib.request.urlopen(EXTRACTION_DOWNLOAD_URL) as response:
            filename = filename_from_response(response)
            download_path = os.path.join(os.getcwd(), filename)
            final_url = response.geturl()
            last_modified = response.headers.get('Last-Modified', '')

            with open(download_path, 'wb') as destination:
                while True:
                    chunk = response.read(1024 * 1024)
                    if not chunk:
                        break
                    destination.write(chunk)

        extraction_date = extract_date_from_download(filename, final_url, last_modified)

        if zipfile.is_zipfile(download_path):
            with zipfile.ZipFile(download_path, 'r') as zip_ref:
                zip_ref.extractall(os.getcwd())
            os.remove(download_path)
            print("Téléchargement et décompression terminés.")
        else:
            print("Téléchargement terminé.")

        return extraction_date
    except Exception as e:
        print(f"❌ Erreur de téléchargement : {e}")
        return ''

def update_database(extraction_date):
    # Trouver le fichier texte extrait (ignorer requirements.txt et autres fichiers parasites)
    extracted_files = find_extraction_files()
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
    existing_files = find_extraction_files()
    
    if existing_files:
        print(f"Utilisation du fichier existant : {existing_files[0]}")
        # Extraire la date du nom du fichier existant
        filename = existing_files[0]
        extraction_date = extract_date_from_download(filename)
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
