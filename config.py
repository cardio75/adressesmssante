import socket
import os
import shutil
import sys

BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
APP_NAME = "Adresses MSSante"

def resource_path(relative_path):
    """Retourne le bon chemin en mode source ou app PyInstaller."""
    return os.path.join(BASE_DIR, relative_path)

def get_user_data_dir():
    """Retourne un dossier modifiable pour la base en mode app autonome."""
    if sys.platform == "darwin":
        base_dir = os.path.expanduser("~/Library/Application Support")
    elif os.name == "nt":
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base_dir = os.environ.get("XDG_DATA_HOME", os.path.expanduser("~/.local/share"))

    return os.path.join(base_dir, APP_NAME)

def ensure_database_exists():
    """Copie la base embarquee vers le dossier utilisateur si besoin."""
    if not getattr(sys, 'frozen', False):
        return DATABASE_PATH

    os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    bundled_database = resource_path('adresses.db')

    if not os.path.exists(DATABASE_PATH) and os.path.exists(bundled_database):
        shutil.copy2(bundled_database, DATABASE_PATH)

    return DATABASE_PATH

def get_local_ip():
    """Récupère l'IP locale automatiquement"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"

# Configuration simple
HOST = os.environ.get("MSSANTE_HOST", "0.0.0.0")
LOCAL_IP = get_local_ip()
PORT = int(os.environ.get("MSSANTE_PORT", "6150"))
DEBUG = False
USER_DATA_DIR = os.environ.get("MSSANTE_DATA_DIR", get_user_data_dir())
DATABASE_PATH = os.environ.get(
    'MSSANTE_DATABASE_PATH',
    os.path.join(USER_DATA_DIR, 'adresses.db') if getattr(sys, 'frozen', False) else 'adresses.db'
)
