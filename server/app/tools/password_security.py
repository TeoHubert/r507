import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from pathlib import Path

# Génération d'un secret key si elle n'existe pas
abs_path = os.path.dirname(os.path.abspath(__file__))
secret_key_path = f"{abs_path}/../../data/secret.key"
if os.getenv("EXECUTION_EN_DOCKER") == "true":
    secret_key_path = "/app/data/secret.key"
if not Path(secret_key_path).exists():
    with open(secret_key_path, "w") as key_file:
        key_file.write(base64.urlsafe_b64encode(os.urandom(32)).decode())

# Lecture de la clé secrète
with open(secret_key_path, "r") as key_file:
    secret = key_file.read()

def chiffrer_mot_de_passe(mot_de_passe: str) -> str:
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    token = Fernet(key).encrypt(mot_de_passe.encode())
    return base64.urlsafe_b64encode(salt + token).decode()

def dechiffrer_mot_de_passe(mot_de_passe_chiffre: str) -> str:
    data = base64.urlsafe_b64decode(mot_de_passe_chiffre.encode())
    salt = data[:16]
    token = data[16:]
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=390000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(secret.encode()))
    mot_de_passe = Fernet(key).decrypt(token).decode()
    return mot_de_passe