# LedgerOne — Dashboard de gestion financière personnelle

LedgerOne est une application web full-stack pour suivre ses dépenses, organiser ses catégories, gérer des budgets et analyser ses finances avec des indicateurs visuels.

Le projet repose sur :
- un **backend FastAPI** (API REST + logique métier),
- un **frontend HTML/CSS/JS vanilla** (interface dashboard),
- une **base SQLite** locale.

---

## Sommaire

- [1. Fonctionnalités](#1-fonctionnalités)
- [2. Stack technique](#2-stack-technique)
- [3. Architecture du projet](#3-architecture-du-projet)
- [4. Installation pas à pas](#4-installation-pas-à-pas)
- [5. Lancement (dev)](#5-lancement-dev)
- [6. Variables d'environnement](#6-variables-denvironnement)
- [7. API: conventions et endpoints](#7-api-conventions-et-endpoints)
- [8. Import CSV: format et comportement](#8-import-csv-format-et-comportement)
- [9. UX/UI et design system](#9-uxui-et-design-system)
- [10. Tests et qualité](#10-tests-et-qualité)
- [11. Dépannage](#11-dépannage)

---

## 1. Fonctionnalités

### Gestion des données
- CRUD des **catégories**.
- CRUD des **transactions**.
- Budget global mensuel.
- Budget mensuel par catégorie.

### Analyses financières
- Résumé mensuel (total, nombre d'opérations, moyenne).
- Répartition par catégorie.
- Totaux mensuels / annuels.
- Évolution mensuelle.
- KPI dashboard + visualisations Chart.js.
- Alertes de dépassement de budget.

### Import CSV
- Import de transactions depuis CSV.
- Détection du séparateur (`;` ou `,`).
- Prévisualisation avant import.
- Validation ligne à ligne avec rapport d'erreurs.

### Expérience utilisateur
- UI refactorée en style **fintech light** (inspiration dashboard market-data).
- Layout responsive.
- Messages d'erreur normalisés côté API et interprétés côté frontend.
- Loader global + notifications utilisateur.

---

## 2. Stack technique

### Backend
- Python 3.10+
- FastAPI
- SQLAlchemy
- Pydantic / pydantic-settings
- SQLite
- Pytest

### Frontend
- HTML5
- CSS3
- JavaScript ES6 (vanilla)
- Chart.js

---

## 3. Architecture du projet

```text
LedgerOne/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── alerts.py
│   │   │       ├── categories.py
│   │   │       ├── import_csv.py
│   │   │       ├── insights.py
│   │   │       ├── settings.py
│   │   │       └── transactions.py
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── utils/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── main.py
│   ├── scripts/
│   ├── tests/
│   └── requirements.txt
├── frontend/
│   ├── css/styles.css
│   ├── includes/sidebar.html
│   ├── js/
│   ├── index.html
│   ├── categories.html
│   ├── transactions.html
│   ├── budget.html
│   ├── import.html
│   └── detail_categorie.html
├── data/
└── README.md
```

### Organisation logique (backend)

1. **Routes API** (`app/api/routes`)  
   Exposent les endpoints REST et transforment les erreurs HTTP.

2. **Services** (`app/services`)  
   Contiennent la logique métier (validations métier, calculs, agrégations, import).

3. **Modèles ORM** (`app/models`)  
   Définissent les tables SQL et les relations.

4. **Schémas** (`app/schemas`)  
   Contrats d'entrée/sortie API.

---

## 4. Installation pas à pas

> Prérequis : Python 3.10+, `pip`, navigateur moderne.

### 4.1 Cloner le dépôt

```bash
git clone <URL_DU_REPO>
cd LedgerOne
```

### 4.2 Créer un environnement virtuel backend

```bash
cd backend
python -m venv .venv
```

Activation :

- Linux/macOS
```bash
source .venv/bin/activate
```

- Windows (PowerShell)
```powershell
.\.venv\Scripts\Activate.ps1
```

### 4.3 Installer les dépendances

```bash
pip install -r requirements.txt
```

### 4.4 Initialiser la base

```bash
python scripts/init_db.py
```

La DB SQLite sera créée/initialisée dans `backend/data/ledgerone.db` (selon la config active).

### 4.5 (Optionnel) Générer un CSV de test

```bash
python scripts/generation_csv.py
```

---

## 5. Lancement (dev)

### 5.1 Lancer le backend

Depuis `backend/` :

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend disponible sur :
- API root: `http://localhost:8000`
- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### 5.2 Lancer le frontend (mode statique)

Dans un second terminal :

```bash
cd frontend
python -m http.server 8080
```

Frontend : `http://localhost:8080`

### 5.3 Alternative: frontend servi par FastAPI

Le backend monte automatiquement `frontend/` sur `/app` si le dossier existe.  
Accès direct : `http://localhost:8000/app/index.html`.

---

## 6. Variables d'environnement

Le backend lit `backend/.env` (via `pydantic-settings`).

Variables principales :

```env
DATABASE_URL=sqlite:///data/ledgerone.db
DEBUG=True
ALLOWED_ORIGINS=["http://localhost:8000", "http://127.0.0.1:8000", "http://localhost:8080", "http://127.0.0.1:8080", "http://localhost:5500", "http://127.0.0.1:5500"]
API_PREFIX=/api
PROJECT_NAME=LedgerOne API
VERSION=1.0.0
```

### Note frontend/API origin

`frontend/js/config.js` applique un fallback utile en dev :
- si le frontend est servi sur `:8080` ou `:5500`, l'API base est automatiquement résolue vers `:8000/api`.

Cela évite les appels vers `:8080/api` quand le backend tourne sur `:8000`.

---

## 7. API: conventions et endpoints

Base URL: `http://localhost:8000/api`

### 7.1 Conventions d'erreur

L'API renvoie un format normalisé :

```json
{
  "detail": "Message lisible",
  "error": {
    "code": "HTTP_ERROR",
    "message": "Message lisible",
    "details": null
  }
}
```

> La clé racine `detail` est conservée pour la rétrocompatibilité avec les clients/tests existants.

### 7.2 Endpoints principaux

#### Catégories
- `GET /categories/`
- `GET /categories/{id}`
- `POST /categories/`
- `PATCH /categories/{id}`
- `DELETE /categories/{id}`

#### Transactions
- `GET /transactions/`
- `GET /transactions/{id}`
- `POST /transactions/`
- `PATCH /transactions/{id}`
- `DELETE /transactions/{id}`

#### Paramètres
- `GET /settings/`
- `PATCH /settings/`

#### Insights
- `GET /insights/summary?year=YYYY&month=M`
- `GET /insights/monthly-total?year=YYYY&month=M[&category_id=ID]`
- `GET /insights/category-breakdown?year=YYYY&month=M`
- `GET /insights/annual-expenses?year=YYYY`
- `GET /insights/monthly-evolution?year=YYYY&month=M`
- `GET /insights/savings-goal?year=YYYY&month=M&income=X&goal=Y`

#### Alertes
- `GET /alerts/?year=YYYY&month=M`

#### Import CSV
- `POST /import/preview`
- `POST /import/csv`

---

## 8. Import CSV: format et comportement

### Format attendu

Colonnes obligatoires :
- `date` (YYYY-MM-DD)
- `description`
- `amount`

Colonne optionnelle :
- `category`

Exemple :

```csv
date,description,amount,category
2025-01-15,Courses,45.50,Alimentation
2025-01-16,Essence,60.00,Transport
```

### Comportement

- Détection du séparateur `;` ou `,`.
- Vérification des colonnes obligatoires.
- Validation ligne par ligne.
- Catégorie auto-créée si absente.
- Rapport final:
  - `inserted`
  - `skipped`
  - `errors[]`

### Cas particulier corrigé

Pour un CSV mal formé/sans lignes parsables avec erreurs de parsing, le rapport ne renvoie plus un faux `skipped: 0` : un `skipped` cohérent est maintenant renvoyé.

---

## 9. UX/UI et design system

Le frontend a été refactoré autour d'un design system CSS basé sur des variables :

- thème clair par défaut,
- palette bleue/teal (fintech),
- cartes arrondies avec ombres légères,
- typographie hiérarchisée (valeurs financières mises en avant),
- tableaux/listes lisibles avec hover subtil,
- responsive desktop-first.

Le fichier principal de style est `frontend/css/styles.css`.

---

## 10. Tests et qualité

### Lancer les tests backend

Depuis `backend/` :

```bash
python -m pytest tests/ -q
```

### Commandes Makefile utiles

Depuis `backend/` :

```bash
make install      # Installe les dépendances
make run-backend  # Lance FastAPI
make run-frontend # Lance frontend statique (depuis ../frontend)
make init-db      # Initialise la DB
make reset-db     # Réinitialise la DB
make test         # Lance les tests avec couverture
make lint         # flake8 + black --check + isort --check
make format       # black + isort
```

---

## 11. Dépannage

### Problème: `ModuleNotFoundError: No module named 'app'`

Lancez les tests depuis `backend/` avec `python -m pytest ...` au lieu de `pytest` brut si le PYTHONPATH local n'est pas configuré.

### Problème: erreur DB `unable to open database file`

- Vérifiez que `backend/data/` existe.
- Vérifiez la cohérence de `DATABASE_URL` dans `.env`.
- Relancez `python scripts/init_db.py`.

### Problème: frontend ne charge pas les données

- Vérifiez que le backend tourne sur `:8000`.
- Vérifiez les `ALLOWED_ORIGINS` dans `.env`.
- En mode frontend `:8080`, `config.js` redirige déjà vers `:8000/api`.

---

## Licence

Ce projet a été développé dans le cadre d'un test technique pour JEECE (Junior-Entreprise de l'ECE).
Pour toute question ou remarque concernant ce projet, vous pouvez me contacter
