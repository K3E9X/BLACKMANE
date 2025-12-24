# BLACKMANE - Structure du Projet

## Arborescence Complète

```
BLACKMANE/
├── README.md                    # Documentation principale
├── .gitignore                   # Fichiers à exclure du versioning
│
├── docs/                        # Documentation
│   ├── ARCHITECTURE.md          # Architecture logicielle détaillée
│   ├── MVP.md                   # Définition du MVP
│   ├── DATA_MODELS.md           # Modèles de données
│   ├── SECURITY_RULES.md        # Règles d'analyse
│   ├── SECURITY_DESIGN.md       # Sécurité de l'outil
│   ├── ROADMAP.md               # Plan de développement
│   └── PROJECT_STRUCTURE.md     # Ce fichier
│
├── backend/                     # Backend Python/FastAPI
│   ├── main.py                  # Point d'entrée application
│   ├── config.py                # Configuration
│   ├── requirements.txt         # Dépendances Python
│   │
│   ├── api/                     # Couche API (routes HTTP)
│   │   ├── __init__.py
│   │   └── v1/                  # API version 1
│   │       ├── __init__.py
│   │       ├── projects.py      # Routes projets (à créer)
│   │       ├── architectures.py # Routes architectures (à créer)
│   │       ├── analyses.py      # Routes analyses (à créer)
│   │       ├── recommendations.py # Routes recommandations (à créer)
│   │       ├── maturity.py      # Routes maturité (à créer)
│   │       └── roadmap.py       # Routes roadmap (à créer)
│   │
│   ├── services/                # Couche services (logique métier)
│   │   ├── __init__.py
│   │   ├── project_service.py   # Service projets (à créer)
│   │   ├── architecture_service.py # Service architectures (à créer)
│   │   ├── analysis_service.py  # Service analyses (à créer)
│   │   ├── recommendation_service.py # Service recommandations (à créer)
│   │   ├── maturity_service.py  # Service maturité (à créer)
│   │   └── roadmap_service.py   # Service roadmap (à créer)
│   │
│   ├── core/                    # Moteur de règles
│   │   ├── __init__.py
│   │   ├── rule_engine.py       # Moteur d'exécution des règles (à créer)
│   │   ├── base_rule.py         # Classe abstraite Rule (à créer)
│   │   ├── architecture_parser.py # Parser d'architecture (à créer)
│   │   ├── threat_analyzer.py   # Analyseur de menaces (à créer)
│   │   ├── maturity_evaluator.py # Évaluateur de maturité (à créer)
│   │   │
│   │   └── rules/               # Règles de sécurité
│   │       ├── __init__.py
│   │       ├── sec_001_admin_no_mfa.py      # Règle 1 (à créer)
│   │       ├── sec_002_critical_no_auth.py  # Règle 2 (à créer)
│   │       ├── sec_003_internet_to_internal.py # Règle 3 (à créer)
│   │       └── ... (12 autres règles)
│   │
│   ├── repositories/            # Couche d'accès aux données
│   │   ├── __init__.py
│   │   ├── project_repository.py # Repository projets (à créer)
│   │   ├── architecture_repository.py # Repository architectures (à créer)
│   │   └── analysis_repository.py # Repository analyses (à créer)
│   │
│   ├── models/                  # Modèles Pydantic
│   │   ├── __init__.py
│   │   ├── project.py           # Modèles Project (à créer)
│   │   ├── architecture.py      # Modèles Architecture (à créer)
│   │   ├── analysis.py          # Modèles Analysis (à créer)
│   │   ├── recommendation.py    # Modèles Recommendation (à créer)
│   │   ├── maturity.py          # Modèles Maturity (à créer)
│   │   └── orm.py               # Modèles SQLAlchemy ORM (à créer)
│   │
│   ├── database/                # Configuration base de données
│   │   ├── __init__.py
│   │   ├── connection.py        # Configuration SQLAlchemy
│   │   └── migrations/          # Migrations Alembic (futur)
│   │
│   └── tests/                   # Tests unitaires
│       ├── __init__.py
│       ├── conftest.py          # Configuration pytest (à créer)
│       ├── test_rules.py        # Tests des règles (à créer)
│       ├── test_services.py     # Tests des services (à créer)
│       └── test_api.py          # Tests des API (à créer)
│
├── frontend/                    # Frontend React
│   ├── package.json             # Dépendances npm
│   ├── tsconfig.json            # Configuration TypeScript
│   ├── tsconfig.node.json       # Config TS pour Node (à créer)
│   ├── vite.config.ts           # Configuration Vite
│   ├── tailwind.config.js       # Configuration Tailwind
│   ├── postcss.config.js        # Configuration PostCSS (à créer)
│   ├── index.html               # Point d'entrée HTML
│   │
│   ├── public/                  # Assets statiques (à créer)
│   │
│   └── src/                     # Code source frontend
│       ├── main.tsx             # Point d'entrée React
│       ├── App.tsx              # Composant racine
│       ├── index.css            # Styles globaux
│       │
│       ├── pages/               # Pages de l'application
│       │   ├── ProjectList.tsx      # Liste projets (à créer)
│       │   ├── ProjectCreate.tsx    # Création projet (à créer)
│       │   ├── ProjectDetail.tsx    # Détail projet (à créer)
│       │   ├── ArchitectureInput.tsx # Input architecture (à créer)
│       │   ├── Analysis.tsx         # Résultats analyse (à créer)
│       │   ├── Recommendations.tsx  # Recommandations (à créer)
│       │   ├── Maturity.tsx         # Maturité (à créer)
│       │   └── Roadmap.tsx          # Roadmap (à créer)
│       │
│       ├── components/          # Composants réutilisables
│       │   ├── Layout/          # Layout principal (à créer)
│       │   ├── Navigation/      # Navigation (à créer)
│       │   ├── Button/          # Bouton (à créer)
│       │   ├── Input/           # Input (à créer)
│       │   ├── Card/            # Card (à créer)
│       │   ├── FindingCard/     # Card finding (à créer)
│       │   ├── RecommendationCard/ # Card recommandation (à créer)
│       │   └── MaturityTable/   # Tableau maturité (à créer)
│       │
│       ├── services/            # Services API
│       │   ├── api.ts           # Client API (à créer)
│       │   ├── projectService.ts # Service projets (à créer)
│       │   ├── architectureService.ts # Service architectures (à créer)
│       │   └── analysisService.ts # Service analyses (à créer)
│       │
│       ├── types/               # Types TypeScript
│       │   ├── project.ts       # Types Project (à créer)
│       │   ├── architecture.ts  # Types Architecture (à créer)
│       │   └── analysis.ts      # Types Analysis (à créer)
│       │
│       └── theme/               # Configuration thème
│           └── dark.ts          # Thème dark (à créer)
│
└── scripts/                     # Scripts utilitaires
    ├── start.sh                 # Script de démarrage
    └── setup.sh                 # Script d'installation (à créer)
```

## Fichiers Créés (État Actuel)

### Documentation Complète ✅
- [x] `README.md` - Documentation principale
- [x] `docs/ARCHITECTURE.md` - Architecture détaillée (5000+ mots)
- [x] `docs/MVP.md` - Périmètre MVP précis
- [x] `docs/DATA_MODELS.md` - Schéma de données complet
- [x] `docs/SECURITY_RULES.md` - 15 règles détaillées
- [x] `docs/SECURITY_DESIGN.md` - Sécurité de l'outil
- [x] `docs/ROADMAP.md` - Roadmap 8 semaines + évolutions
- [x] `docs/PROJECT_STRUCTURE.md` - Ce fichier

### Configuration Projet ✅
- [x] `.gitignore` - Configuration Git

### Backend (Structure) ✅
- [x] `backend/main.py` - Application FastAPI avec sécurité
- [x] `backend/config.py` - Configuration centralisée
- [x] `backend/requirements.txt` - Dépendances Python
- [x] `backend/database/connection.py` - Configuration DB
- [x] Tous les `__init__.py` pour packages

### Frontend (Structure) ✅
- [x] `frontend/package.json` - Configuration npm
- [x] `frontend/vite.config.ts` - Configuration Vite
- [x] `frontend/tsconfig.json` - Configuration TypeScript
- [x] `frontend/tailwind.config.js` - Configuration Tailwind (dark theme)
- [x] `frontend/index.html` - HTML avec CSP
- [x] `frontend/src/main.tsx` - Point d'entrée React
- [x] `frontend/src/App.tsx` - Composant racine
- [x] `frontend/src/index.css` - Styles Tailwind

### Scripts ✅
- [x] `scripts/start.sh` - Script de démarrage complet

## Fichiers à Créer (Prochaines Étapes)

### Semaine 1 : Backend Core
- [ ] `backend/models/orm.py` - Modèles SQLAlchemy (Project, Architecture, etc.)
- [ ] `backend/models/project.py` - Modèles Pydantic Project
- [ ] `backend/repositories/project_repository.py` - Repository projets
- [ ] `backend/services/project_service.py` - Service projets
- [ ] `backend/api/v1/projects.py` - Routes API projets
- [ ] `backend/tests/test_projects.py` - Tests projets

### Semaine 2 : Architecture
- [ ] `backend/models/architecture.py` - Modèles Pydantic Architecture
- [ ] `backend/repositories/architecture_repository.py` - Repository architectures
- [ ] `backend/services/architecture_service.py` - Service architectures
- [ ] `backend/api/v1/architectures.py` - Routes API architectures
- [ ] `frontend/src/pages/ArchitectureInput.tsx` - Page input architecture

### Semaine 3-4 : Moteur de Règles
- [ ] `backend/core/base_rule.py` - Classe abstraite Rule
- [ ] `backend/core/rule_engine.py` - Moteur d'exécution
- [ ] `backend/core/rules/sec_001_admin_no_mfa.py` - Règle 1
- [ ] ... (14 autres règles)
- [ ] `backend/services/analysis_service.py` - Service analyses
- [ ] `backend/tests/test_rules.py` - Tests règles

### Semaine 5-6 : Recommandations & UI
- [ ] `backend/services/recommendation_service.py` - Service recommandations
- [ ] `backend/services/maturity_service.py` - Service maturité
- [ ] `backend/services/roadmap_service.py` - Service roadmap
- [ ] `frontend/src/pages/Analysis.tsx` - Page analyse
- [ ] `frontend/src/pages/Recommendations.tsx` - Page recommandations
- [ ] `frontend/src/pages/Maturity.tsx` - Page maturité
- [ ] `frontend/src/pages/Roadmap.tsx` - Page roadmap

## Commandes Utiles

### Installation

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Développement

```bash
# Option 1 : Script automatique
./scripts/start.sh

# Option 2 : Manuel (2 terminaux)
# Terminal 1 - Backend
cd backend && source venv/bin/activate && python main.py

# Terminal 2 - Frontend
cd frontend && npm run dev
```

### Tests

```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

### Linting & Type Checking

```bash
# Backend
cd backend
black .
ruff check .
mypy .

# Frontend
cd frontend
npm run lint
npm run type-check
```

## URLs

- **Frontend** : http://localhost:5173
- **Backend API** : http://localhost:8000
- **API Docs (Swagger)** : http://localhost:8000/api/docs
- **API Docs (ReDoc)** : http://localhost:8000/api/redoc

## État d'Avancement

### Terminé ✅
- Architecture logicielle complète
- Définition MVP détaillée
- Modèles de données complets
- 15 règles de sécurité spécifiées
- Design sécurité de l'outil
- Roadmap 8 semaines
- Structure complète du projet
- Configuration backend et frontend
- Scripts de démarrage

### En Cours 🚧
- Implémentation MVP Semaine 1

### À Venir 📋
- Semaines 2-8 selon roadmap

## Prochaines Actions Recommandées

1. **Installer les dépendances**
   ```bash
   cd backend && python -m venv venv && source venv/bin/activate && pip install -r requirements.txt
   cd ../frontend && npm install
   ```

2. **Tester le lancement**
   ```bash
   ./scripts/start.sh
   ```

3. **Commencer Semaine 1**
   - Créer les modèles ORM (Project)
   - Implémenter le CRUD projets
   - Tester l'API
   - Créer la page frontend liste projets

4. **Valider avec un utilisateur**
   - Montrer la structure
   - Valider l'approche
   - Ajuster si nécessaire

---

## Notes Importantes

- **Pas de sur-ingénierie** : Focus sur le MVP
- **Security by Design** : Sécurité à chaque étape
- **Tests first** : Écrire les tests en même temps que le code
- **Documentation continue** : Mettre à jour la doc au fur et à mesure
- **Validation terrain** : Tester avec des architectes réels dès que possible

---

**Structure créée avec succès. Prêt pour le développement MVP.**
