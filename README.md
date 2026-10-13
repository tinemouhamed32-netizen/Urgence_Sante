# Urgence Santé

## Architecture générale

Ce projet est un socle Python pour une IA d'assistance sanitaire en mode démonstration. Il a été structuré pour rester simple, extensible et testable, avec une séparation claire entre API, services métier, schémas de validation, modèles de données et intégrations optionnelles.

### Rôle des technologies

- Python 3.12 : langage principal du backend.
- FastAPI : API REST avec validation automatique et documentation interactive.
- Uvicorn : serveur ASGI de production local.
- Pydantic : validation des entrées et sorties.
- SQLAlchemy : base de données locale et modèles de données.
- Alembic : migrations, prévu pour la version évolutive.
- SQLite : prototype local léger.
- Pytest : tests automatisés.
- Ruff et Mypy : qualité et vérification statique.

## Arborescence

```text
app/
  api/
  core/
  database/
  integrations/
  models/
  offline/
  repositories/
  schemas/
  services/
main.py
requirements.txt
pyproject.toml
README.md
```

## Environnement virtuel et dépendances

### Windows PowerShell

```powershell
cd C:\Users\WINDOWS\Desktop\Urgence_Sante
python -m venv .venv
. .\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Lancer le backend

```powershell
cd C:\Users\WINDOWS\Desktop\Urgence_Sante
. .\.venv\Scripts\Activate.ps1
python main.py
```

L'API sera disponible sur http://127.0.0.1:8000 et la documentation Swagger sur http://127.0.0.1:8000/docs.

## Lancer l'interface de démonstration

```powershell
cd C:\Users\WINDOWS\Desktop\Urgence_Sante
. .\.venv\Scripts\Activate.ps1
streamlit run streamlit_app.py --server.port 8501
```

L'interface Streamlit sera disponible sur http://127.0.0.1:8501.

## Déploiement public gratuit sur Render

Le fichier `render.yaml` décrit deux services Render (API FastAPI et interface Streamlit). Pour créer les URL publiques :

1. Publier le contenu de ce dossier dans un dépôt GitHub personnel.
2. Créer un compte Render, choisir **New > Blueprint**, puis connecter ce dépôt.
3. Approuver la création des deux services gratuits `urgence-sante-api` et `urgence-sante-ui`.
4. Ouvrir l'URL publique du service `urgence-sante-ui`. Son adresse est affichée dans le tableau de bord Render.

L'API est configurée avec un endpoint de vérification (`/health`), et l'interface récupère automatiquement le nom d'hôte de l'API. Les services gratuits peuvent se mettre en veille après une période d'inactivité et le premier accès peut prendre quelques instants. Leur système de fichiers n'est pas persistant : la base SQLite et les sessions de démonstration peuvent être réinitialisées lors d'un redéploiement ou d'un redémarrage du service. Ne pas y stocker de données de santé réelles.

## Tests rapides

```powershell
cd C:\Users\WINDOWS\Desktop\Urgence_Sante
. .\.venv\Scripts\Activate.ps1
pytest -q
```

## Exemples de requêtes

### Check santé

```powershell
curl http://127.0.0.1:8000/health
```

### Session d'urgence de démonstration

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/emergency/session -H "Content-Type: application/json" -d '{"country":"SN","language":"fr","scenario":"demo"}'
```

### Question générale

```powershell
curl -X POST http://127.0.0.1:8000/api/v1/assistant/message -H "Content-Type: application/json" -d '{"question":"Quels conseils pour rester hydraté ?","country":"SN","language":"fr"}'
```

## Limites du prototype

- Les scénarios sont fictifs et destinés à la démonstration.
- Les protocoles ne remplacent pas une validation médicale professionnelle.
- Les données de santé ne doivent pas être utilisées directement pour un traitement réel.
