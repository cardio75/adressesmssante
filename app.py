from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import re
from datetime import datetime
from config import HOST, PORT, DEBUG, DATABASE_PATH

app = Flask(__name__)

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
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT extraction_date FROM adresses LIMIT 1")
        result = cursor.fetchone()
        if result and result[0]:
            extraction_date = result[0]
            date_formatee = datetime.strptime(extraction_date, '%Y%m%d').strftime('%d/%m/%Y')
        else:
            date_formatee = 'Date inconnue'
        conn.close()
    except Exception as e:
        print(f"Erreur base de données: {e}")
        date_formatee = 'Erreur de lecture'

    return render_template('index.html', extraction_date=date_formatee)

@app.route('/search')
def search():
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

if __name__ == '__main__':
    print(f"🚀 Application démarrée sur http://{HOST}:{PORT}")
    print(f"📱 Accessible depuis le réseau local")
    app.run(host=HOST, port=PORT, debug=DEBUG)
