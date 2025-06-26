import socket

def get_local_ip():
    """Récupère l'IP locale automatiquement"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

# Configuration simple
HOST = get_local_ip()
PORT = 6150
DEBUG = False
DATABASE_PATH = 'adresses.db' 