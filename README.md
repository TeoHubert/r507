# R507 
## Réalisation par Téo HUBERT - BUT R&T Saint Malo 3ème Année DEV CLOUD

> Lien vers le dépot GITHUB : https://github.com/TeoHubert/r507

### Contexte du projet
Réaliser un outil permettant de superviser des indicateurs (Mémoire, CPU, Disque, ...) sur différentes cibles.
Cela doit être basé sur Python à l'aide principalement de POO, Pydantic, SQLModel, FastAPI.

### Utilisation de l'application
1. Créer un environnement python (recommandé)

Exemple sous linux :
```bash
python -m venv venv
```

2. Activer cet environnement (si utilisation d'un environnement)

Exemple sous linux :
```bash
source venv/bin/activate
```

3. Installer la dépendance nécéssaire "Poetry"

Exemple général sous linux :
```bash
pip install poetry
```

4. Lancer l'application

Exemple général sous linux :
```bash
cd {source_du_projet}/server/app
poetry run uvicorn main:app --reload
```

### Gestion des versions de la BDD

Générer une nouvelle version de la base de donnée (côté DEV)
```bash
poetry run alembic revision --autogenerate -m ""
```

Réaliser la mise à jour de la base (côté client)
```bash
poetry run alembic upgrade head
```


### Informations utiles

**Le chiffrement des mots de passes :**
Pour des raisons de "sécurité", les mots de passes SSH sont chiffré lors de leurs stockages dans la base et sont déchiffré à l'utilisation de la connexion SSH.
Une clé dans le fichier `server/app/secret.key` est automatiquement générée pour réaliser le chiffrement. Une fois générée, il faut donc la conserver pour pouvoir déchiffrer les mots de passes stockés.

**Logigramme d'utilisation :**

![A faire](docs/img/logigrame.png "A faire")

### Utilisation de Bruno
Une fois une application déployée, vous pouvez utiliser bruno pour tester la réponses aux endponts.

Voici un exemple en utilisant l'extention VSCode (Visual Studio Code) de Bruno :

1. Ouvrir le menu d'import de collection

![Image représentant le bouton + cliqué permettant l'accès à "Open Collection"](docs/img/bruno_open_collection.png "Accès au menu d'import d'une collection")

2. Selectionner le dossier `{source_du_projet}/bruno/tests-app`

3. Activer l'environnement

![Image représentant la selection d'un environnement dans bruno](docs/img/bruno_enable_env.png "Selection d'un environnement")

4. FACULTATIF : Changer l'url du serveur

Si vous executez le serveur applicatif sur un autre hote par exemple, changer l'url/port racine du serveur à cibler par les requêtes :
![Image représentant le changement de la variable d'environnement dans bruno](docs/img/bruno_change_env_serveur.png "Modification de la variable d'environnement Serveur")
