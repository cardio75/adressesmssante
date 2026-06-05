from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import re
import os
import threading
import webbrowser
from datetime import datetime
from config import HOST, LOCAL_IP, PORT, DEBUG, DATABASE_PATH, ensure_database_exists, resource_path
from creer_bd_mssante import rebuild_database

app = Flask(
    __name__,
    template_folder=resource_path('templates'),
    static_folder=resource_path('static'),
)

update_lock = threading.Lock()
update_status = {
    'running': False,
    'message': '',
    'success': None,
    'error': '',
    'extraction_date': '',
}

def format_extraction_date(extraction_date):
    if not extraction_date:
        return 'Date inconnue'
    return datetime.strptime(extraction_date, '%Y%m%d').strftime('%d/%m/%Y')

def get_database_extraction_date():
    ensure_database_exists()
    conn = sqlite3.connect(DATABASE_PATH)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT extraction_date FROM adresses LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result and result[0] else ''
    finally:
        conn.close()

def run_database_update():
    global update_status

    try:
        with update_lock:
            update_status.update({
                'message': 'Téléchargement et reconstruction de la base en cours...',
                'success': None,
                'error': '',
            })

        extraction_date = rebuild_database(DATABASE_PATH)
        if not extraction_date:
            raise RuntimeError("Le téléchargement de la base a échoué.")

        with update_lock:
            update_status.update({
                'running': False,
                'message': f"Base mise à jour le {format_extraction_date(extraction_date)}.",
                'success': True,
                'error': '',
                'extraction_date': format_extraction_date(extraction_date),
            })
    except Exception as e:
        with update_lock:
            update_status.update({
                'running': False,
                'message': 'Mise à jour impossible.',
                'success': False,
                'error': str(e),
            })

def escape_fts_query(query):
    """Échappe les caractères spéciaux pour les requêtes FTS5"""
    if not query:
        return query
    
    # Caractères spéciaux FTS5 à échapper
    special_chars = ['"', "'", '(', ')', '[', ']', '{', '}', ':', ';', ',', '.', '!', '?', '@', '#', '$', '%', '^', '&', '*', '+', '=', '|', '\\', '/', '<', '>', '~', '`']
    
    escaped_query = query
    for char in special_chars:
        escaped_query = escaped_query.replace(char, ' ')
    
    # Nettoyer les espaces multiples
    escaped_query = re.sub(r'\s+', ' ', escaped_query).strip()
    
    return escaped_query

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.svg', mimetype='image/svg+xml')

@app.route('/')
def index():
    try:
        date_formatee = format_extraction_date(get_database_extraction_date())
    except Exception as e:
        print(f"Erreur base de données: {e}")
        date_formatee = 'Erreur de lecture'

    return render_template('index.html', extraction_date=date_formatee)

@app.route('/search')
def search():
    ensure_database_exists()
    nom = escape_fts_query(request.args.get('nom', '').strip())
    prenom = escape_fts_query(request.args.get('prenom', '').strip())
    ville = escape_fts_query(request.args.get('ville', '').strip())
    code_postal = escape_fts_query(request.args.get('code_postal', '').strip())
    specialty = escape_fts_query(request.args.get('specialty', '').strip())

    conditions = []
    params = []

    if nom:
        conditions.append("nom_exercice MATCH ?")
        params.append(nom + '*')
    if prenom:
        conditions.append("prenom_exercice MATCH ?")
        params.append(prenom + '*')
    if ville:
        conditions.append("ville MATCH ?")
        params.append(ville + '*')
    if code_postal:
        conditions.append("code_postal MATCH ?")
        params.append(code_postal + '*')
    if specialty:
        conditions.append("specialty MATCH ?")
        params.append(specialty + '*')

    if not conditions:
        return jsonify([])

    where_clause = ' AND '.join(conditions)
    query = f"""
    SELECT raison_sociale, nom_exercice, prenom_exercice, adresse_complete, code_postal, ville, adresse_mssante, region, specialty
    FROM adresses
    WHERE {where_clause}
    LIMIT 50
    """

    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute(query, params)
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'raison_sociale': row[0] or '',
                'nom_exercice': row[1] or '',
                'prenom_exercice': row[2] or '',
                'adresse_complete': row[3] or '',
                'code_postal': row[4] or '',
                'ville': row[5] or '',
                'adresse_mssante': row[6] or '',
                'region': row[7] or '',
                'specialty': row[8] or ''
            })
        conn.close()
        return jsonify(results)
    except Exception as e:
        print(f"Erreur recherche: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        return jsonify({'error': 'Erreur lors de la recherche'}), 500

@app.route('/update_database', methods=['POST'])
def update_database_route():
    with update_lock:
        if update_status['running']:
            return jsonify(update_status)

        update_status.update({
            'running': True,
            'message': 'Démarrage de la mise à jour...',
            'success': None,
            'error': '',
        })

    thread = threading.Thread(target=run_database_update, daemon=True)
    thread.start()
    return jsonify(update_status)

@app.route('/update_status')
def update_status_route():
    with update_lock:
        return jsonify(update_status)

if __name__ == '__main__':
    ensure_database_exists()

    if os.environ.get('MSSANTE_NO_BROWSER') != '1':
        threading.Timer(1.0, webbrowser.open, args=(f'http://localhost:{PORT}',)).start()

    print(f"🚀 Application démarrée sur http://localhost:{PORT}")
    print(f"📱 Accessible depuis le réseau local : http://{LOCAL_IP}:{PORT}")
    app.run(host=HOST, port=PORT, debug=DEBUG)
