import os
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from pathlib import Path

# Génération d'un secret key si elle n'existe pas
if not Path("/app/data/secret.key").exists():
    with open("/app/data/secret.key", "w") as key_file:
        key_file.write(base64.urlsafe_b64encode(os.urandom(32)).decode())

# Lecture de la clé secrète
with open("/app/data/secret.key", "r") as key_file:
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