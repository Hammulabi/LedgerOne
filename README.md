# LedgerOne

Application de gestion de dépenses avec backend **FastAPI + SQLite** et frontend **HTML/CSS/JS**.

## Prérequis
- Python 3.10+
- `pip`
- (Optionnel) Docker + Docker Compose

## 1) Installation locale (backend + frontend séparés)

### 1. Cloner le projet
```bash
git clone <repo-url>
cd LedgerOne
```

### 2. Créer et activer un environnement virtuel
```bash
cd backend
python -m venv .venv
```

Linux/macOS:
```bash
source .venv/bin/activate
```

Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Installer les dépendances backend
```bash
pip install -r requirements.txt
```

### 4. Initialiser la base SQLite
```bash
python scripts/init_db.py
```

Le script crée automatiquement le dossier `data/` s'il n'existe pas, puis crée les tables.

### 5. Démarrer le backend
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API:
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

### 6. Démarrer le frontend
Dans un **autre terminal**, depuis la racine du repo:
```bash
python -m http.server 8080 --directory frontend
```

Frontend:
- `http://127.0.0.1:8080`

## 2) Lancer via scripts (optionnel)

Depuis la racine:

Linux/macOS:
```bash
./start.sh
```

Windows PowerShell:
```powershell
./start.ps1
```

Ces scripts:
- créent/activent l'environnement virtuel backend,
- installent les dépendances,
- initialisent la DB,
- démarrent backend + frontend.

## 3) API URL côté frontend

Le frontend lit maintenant l'URL API depuis `frontend/js/config.js`:
- par défaut: `${window.location.origin}/api`
- surcharge possible: définir `window.__LEDGERONE_API_BASE_URL` avant `config.js`.

Cela évite les URLs hardcodées (`127.0.0.1:8000`) et facilite les déploiements.

## 4) Frontend servi par FastAPI (optionnel)

Le backend monte `frontend/` via `StaticFiles` sur:
- `http://127.0.0.1:8000/app`

Dans ce mode, frontend et backend partagent le même origin (moins de friction CORS).

## 5) Docker (optionnel)

Depuis la racine:
```bash
docker compose up --build
```

Services:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:8080`

Le volume `./data` est monté dans le conteneur backend pour persister la base SQLite.

## 6) Structure rapide

- `backend/app/main.py` : app FastAPI, CORS, routers, StaticFiles
- `backend/scripts/init_db.py` : création tables + bootstrap settings
- `frontend/js/config.js` : configuration URL API
- `frontend/js/api.js` : client API utilisé par toutes les pages
