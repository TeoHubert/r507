# R507 - Guardian Supervision
## 📋 Project by Téo HUBERT - BUT R&T Saint Malo 3rd Year DEV CLOUD

> **GitHub Link:** https://github.com/TeoHubert/r507

## 📖 Table of Contents
- [Project Context](#project-context)
- [Architecture](#architecture)
- [Features](#features)
- [Installation and Deployment](#installation-and-deployment)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Testing](#testing)
- [Development](#development)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Project Context

Guardian Supervision is an infrastructure monitoring tool that allows monitoring system indicators (Memory, CPU, network connectivity) on different remote targets via SSH.

**Technical Stack:**
- **Backend:** Python, FastAPI, SQLModel, Alembic, Pydantic
- **Frontend:** HTML5, Bootstrap 5.3, Vanilla JavaScript, Chart.js
- **Database:** SQLite
- **Containerization:** Docker & Docker Compose
- **Security:** AES encryption of SSH passwords

---

## 🏗️ Architecture

```
r507/
├── 📁 server/                     # Backend API
│   ├── 🐳 Dockerfile
│   └── 📁 app/
│   └── 📁 app/
│       ├── 📋 main.py            # FastAPI entry point
│       ├── 🗄️ database.py       # SQLite configuration
│       ├── ⚙️ scheduler.py       # Automatic scheduler
│       ├── 📁 models/            # Data models
│       │   ├── 🖥️ host.py        # Host management
│       │   ├── ⚡ action.py      # Action scripts
│       │   ├── 📊 indicator.py   # Indicators
│       │   └── 📁 actions/       # Monitoring scripts (customization and addition here)
│       ├── 📁 tools/             # Utilities
│       │   └── 🔒 password_security.py
│       └── 📁 alembic/           # Database migrations
├── 📁 frontend/                   # Web Interface
│   ├── 🐳 Dockerfile
│   └── 📁 html/
│       ├── 🏠 index.html         # Main dashboard
│       ├── ⚙️ configuration.html # Config management
│       ├── ⚙️ configuration_edithost.html # Host editor
│       ├── ⚙️ configuration_actions.html # Action editor
│       └── 📈 graph.js           # Real-time charts
│       └── 📈 toaster.js         # User notification system
├── 📁 tests/                     # API Tests
│   └── 📁 server/bruno/          # Bruno Collection
└── 🐳 docker-compose.yml         # Orchestration
```

---

## 🚀 Features

### 🖥️ Host Monitoring
- **Add/remove hosts** with secure SSH connection
- **Automatic monitoring** with configurable intervals
- **Predefined system actions:**
  - 🧠 Linux memory usage (`memory_linux.py`)
  - 🔥 Linux CPU usage (`cpu_linux.py`)
  - 🗄️ Router interface status (`get_interface_status.py`)
  - 🌐 Connectivity and latency test (`ping_time_linux.py`)
![Default Actions](docs/img/defaults_actions.png "Default Actions")


### 📊 Real-time Monitoring
- **Interactive dashboard** with accordion per host
- **Temporal charts** with Chart.js
- **Manual execution** of indicators
- **History** of collected values

### 🔐 Security
- **AES-256 encryption** of SSH passwords
- **Encryption key** automatically generated (`secret.key`)
- **Secure SSH connections** with Paramiko

### 🗄️ Data Management
- **SQLite database** with Alembic migrations
- **Complete REST API** with FastAPI
- **Automatic collection scheduler**

---

## 📦 Installation and Deployment

### 🐳 Docker Deployment (Recommended)

1. **Clone the repository:**
```bash
git clone https://github.com/TeoHubert/r507.git
cd r507
```

2. **Start the application:**
```bash
docker compose up --build
```

3. **Access the services:**
- **Web Interface:** http://localhost:80
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs

### 🛠️ Local Environment Deployment (Not recommended except for DEV)

#### Prerequisites
- Python 3.9+
- Poetry

#### Backend Installation
```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install Poetry
pip install poetry

# Install dependencies
cd server/app
poetry install

# Configure the database
poetry run alembic upgrade head

# Start the server
poetry run uvicorn main:app --reload --port 8000
```

#### Frontend Part
Open the HTML file `index.html` located in `./frontend/html/` and navigate.

---

## ⚙️ Usage Configuration

> Recommended to use the web graphical interface

### 🖥️ Adding a Host

1. **Via the web interface:**
   - Go to the `Configuration` tab
     ![Configuration Section](docs/img/blank_host_section.png "Configuration Section")
   - Fill in the host information and click "+"
     ![Adding a host](docs/img/fill_new_host.png "Adding a host")
   - Enter the host configuration menu with the blue edit button to the right of the corresponding line that was just added to the table
     ![Host configuration](docs/img/added_host.png "Host configuration")
   - Complete the SSH parameters then save
     ![SSH parameters configuration](docs/img/configure_ssh_settings.png "SSH parameters configuration")

2. **Via REST API:**
```bash
curl -X POST "http://localhost:8000/host" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Server",
    "ip": "192.168.1.100",
    "ssh_port": 22,
    "username": "admin",
    "password": "password"
  }'
```

### 📊 Configuring Indicators on a Host

1. **Via the web interface:**
   
   - Now with the Host configured, on the configuration page add an indicator to the relevant host
     ![Add an indicator](docs/img/add_indicator.png "Add an indicator")
   - Click "+" to validate the addition


2. **Via REST API:**

```bash
# Add a memory indicator
curl -X POST "http://localhost:8000/host/1/indicator" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "RAM Usage",
    "action_id": 1,
    "interval": 300
  }'

# Add a ping indicator with custom destination
curl -X POST "http://localhost:8000/host/1/indicator" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Ping Google",
    "action_id": 3,
    "interval": 60,
    "parametre": {"dest": "8.8.8.8"}
  }'

# Add an interface status indicator
curl -X POST "http://localhost:8000/host/1/indicator" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "eth0 Status",
    "action_id": 4,
    "interval": 120,
    "parametre": {"interface": "eth0"}
  }'
```

### ⚡ Available Actions

| Action | Script Path | Description | Parameters |
|--------|-------------|-------------|------------|
| Linux Memory | `models.actions.memory_linux` | RAM usage percentage | None |
| Linux CPU | `models.actions.cpu_linux` | CPU usage percentage | None |
| Ping Test | `models.actions.ping_time_linux` | Latency to a destination (8.8.8.8 by default) | `{"dest": "ip_address"}` (optional) |
| Interface Status | `models.actions.get_interface_status` | Network interface status (router) | `{"interface": "interface_name"}` (required) |

#### 📋 Action Details

**Ping Test:**
- **Optional parameter:** `{"dest": "192.168.1.1"}` to change the destination
- **Default:** 8.8.8.8
- **Return:** Latency in milliseconds

**Interface Status:**
- **Required parameter:** `{"interface": "eth0"}` name of the interface to check
- **Return:** 2 (up), 1 (down), 0 (error)
- **Prerequisites:** vtysh installed on the target host


---

## 🔌 API Documentation

### 📡 Main Endpoints

#### Hosts
```bash
GET    /hosts                    # List all hosts
GET    /host/{id}               # Details of a host
POST   /host                    # Create a host
PUT    /host/{id}               # Modify a host
DELETE /host/{id}               # Delete a host
```

#### Indicators
```bash
GET    /host/{id}/indicators              # Host indicators
POST   /host/{id}/indicator               # Create an indicator
POST   /indicator/{id}/execute            # Execute manually
GET    /indicator/{id}/values             # Value history
DELETE /indicator/{id}/values             # Purge history
```

#### Actions
```bash
GET    /actions                 # List of available actions
POST   /action                  # Create a new action
PUT    /action/{id}             # Modify an action
```

---

## 🔐 Sécurité

### 🔑 Chiffrement des mots de passe

Les mots de passe SSH sont automatiquement chiffrés lors du stockage :

```python
# Chiffrement automatique à l'ajout
host = Host(name="Server", ip="192.168.1.100", password="secret123")
# Le mot de passe est chiffré avec AES-256 + PBKDF2
```

**⚠️ Important :** Conservez le fichier `server/app/secret.key` - il est nécessaire pour déchiffrer les mots de passe existants.

### 🛡️ Bonnes pratiques

- Utilisez des mots de passe forts pour SSH
- Sauvegardez régulièrement le fichier `secret.key`

---

## 🧪 Tests

### 🔍 Tests avec Bruno

1. **Importer la collection :**
   - Ouvrir Bruno → "Open Collection"

     ![Image représentant le bouton + cliqué permettant l'accès à "Open Collection"](docs/img/bruno_open_collection.png "Accès au menu d'import d'une collection")

   - Sélectionner le dossier `tests/server/bruno/`

2. **Configurer l'environnement :**
   - Activer l'environnement "Local APP"

     ![Image représentant la selection d'un environnement dans bruno](docs/img/bruno_enable_env.png "Selection d'un environnement")

   - Vérifier l'URL : `http://127.0.0.1:8000`

3. **Tests disponibles :**
   - ✅ Gestion des hôtes (CRUD)
   - ✅ Gestion des actions
   - ✅ Gestion des indicateurs
   - ✅ Exécution d'indicateurs
   - ✅ Purge des données

4. **FACULTATIF : Changer l'url du serveur**

Si vous executez le serveur applicatif sur un autre hote par exemple, changer l'url/port racine du serveur à cibler par les requêtes :
![Image représentant le changement de la variable d'environnement dans bruno](docs/img/bruno_change_env_serveur.png "Modification de la variable d'environnement Serveur")

### 📋 Exemples de tests

```bash
# Test de création d'hôte
POST /host
{
  "name": "Test Server",
  "ip": "192.168.1.10",
  "username": "testuser",
  "password": "testpass"
}

# Test d'exécution d'indicateur
POST /indicator/1/execute
```

---

## 🛠️ Développement

### 🗄️ Gestion de la base de données

```bash
# Générer une nouvelle migration
cd server/app
poetry run alembic revision --autogenerate -m "Description des changements"

# Appliquer les migrations
poetry run alembic upgrade head

# Voir l'historique des migrations
poetry run alembic history
```

### 🏗️ Créer une action personnalisée

Pour créer une nouvelle action de supervision :

1. **Créer le fichier script dans `server/app/models/actions/` :**

```python
# Exemple : custom_action.py
from models.host import Host

def run(host: Host, parametre: str = None) -> str:
    try:
        # Votre logique de supervision ici
        # Exemple : récupérer un métrique personnalisé
        result = host.execute_ssh_command("votre_commande_ssh")
        value = float(result.strip())
        return value
    except Exception as e:
        print(f"Erreur dans l'action personnalisée : {e}")
        return 0.0
```

2. **Enregistrer l'action via l'API :**

```bash
curl -X POST "http://localhost:8000/action" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mon Action Personnalisée",
    "script_path": "models.actions.custom_action",
    "min_value": 0,
    "max_value": 100,
    "unite": "units",
    "rounding": 2
  }'
```

3. **Bonnes pratiques :**
   - Toujours inclure une gestion d'erreur
   - Retourner une valeur numérique
   - Utiliser `parametre` pour la configuration
   - Tester la commande SSH manuellement avant

---

## 🚨 Troubleshooting

### ❌ Problèmes possibles et solutions envisageables

### ❌ Problèmes possibles et solutions envisageables

#### Connexion SSH échoue
```bash
# Vérifier la connectivité réseau
ping <ip_host>

# Tester la connexion SSH manuellement
ssh -p <port> <username>@<ip_host>

# Vérifier les logs du serveur
docker compose logs server
```

#### Actions retournent des erreurs
```bash
# Vérifier que la commande fonctionne manuellement
ssh <username>@<ip_host> "free -m | grep Mem | awk '{print \$3}'"

# Vérifier les paramètres de l'indicateur
curl http://localhost:8000/indicator/<id>
```

#### Base de données corrompue
```bash
# Réinitialiser la base
cd server/app
rm supervision.db
poetry run alembic upgrade head
```

#### Interface routeur (vtysh) ne fonctionne pas
```bash
# Installer vtysh sur l'hôte cible (Ubuntu/Debian)
sudo apt-get install frr-pythontools

# Vérifier l'accès vtysh
ssh <username>@<ip_host> "vtysh -c 'show version'"
```


### 📊 Monitoring des performances

```bash
# Surveiller les ressources Docker
docker stats r507_backend r507_frontend

# Logs en temps réel
docker compose logs -f

# Taille de la base de données
ls -lh server/app/supervision.db
```

---

## 📄 Licence

Ce projet est réalisé dans le cadre du BUT R&T R507 - Saint Malo 3ème Année DEV CLOUD.

**Auteur :** Téo HUBERT  
**Email :** teohubert00@gmail.com - teo.hubert@etudiant.univ-rennes.fr 
**GitHub :** https://github.com/TeoHubert/r507

---

*Dernière mise à jour : 5 Décembre 2025*