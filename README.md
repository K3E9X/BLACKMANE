# BLACKMANE

Outil local d'analyse d'architectures sécurisées (Security by Design)

## Description

BLACKMANE est un outil professionnel destiné aux architectes cybersécurité et RSSI pour analyser et sécuriser les architectures IT (cloud, on-premise, hybrides).

### Principes
- Security by Design
- Zero Trust pragmatique
- Local first (pas de dépendance cloud)
- Aide à la décision

### Fonctionnalités
- Modélisation d'architectures (zones, composants, flux)
- Analyse automatisée basée sur règles de sécurité
- Génération de recommandations priorisées
- Évaluation de maturité sécurité
- Roadmap de sécurité

## Architecture

- **Backend** : Python 3.11+, FastAPI, SQLAlchemy, SQLite
- **Frontend** : React/Svelte, TypeScript, TailwindCSS
- **Stockage** : SQLite local

## Installation

### Prérequis
- Python 3.11+
- Node.js 18+
- npm ou yarn

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Frontend

```bash
cd frontend
npm install
```

## Lancement

### Mode Développement

Terminal 1 (Backend) :
```bash
cd backend
source venv/bin/activate
python main.py
```

Terminal 2 (Frontend) :
```bash
cd frontend
npm run dev
```

Application disponible sur : `http://localhost:5173`

### Mode Production

```bash
./scripts/start.sh
```

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Architecture logicielle détaillée
- [MVP](docs/MVP.md) - Périmètre MVP
- [Modèles de Données](docs/DATA_MODELS.md) - Schéma de données
- [Règles de Sécurité](docs/SECURITY_RULES.md) - Règles d'analyse
- [Security Design](docs/SECURITY_DESIGN.md) - Sécurité de l'outil
- [Roadmap](docs/ROADMAP.md) - Plan de développement

## Utilisation

### 1. Créer un projet

Créer un nouveau projet d'architecture avec :
- Nom
- Type (cloud/on-premise/hybride)
- Contexte métier
- Niveau de criticité

### 2. Modéliser l'architecture

Définir manuellement :
- Zones de confiance
- Composants (firewall, serveurs, DB, etc.)
- Flux entre composants

### 3. Lancer l'analyse

Analyse automatique basée sur 15 règles Zero Trust et Security by Design.

### 4. Consulter les résultats

- Findings (faiblesses détectées)
- Recommandations priorisées
- Évaluation de maturité
- Roadmap de sécurité

## Développement

### Structure du Projet

```
BLACKMANE/
├── backend/           # API FastAPI
│   ├── api/          # Routes HTTP
│   ├── services/     # Logique métier
│   ├── core/         # Moteur de règles
│   ├── repositories/ # Accès données
│   ├── models/       # Modèles Pydantic
│   ├── database/     # Configuration DB
│   └── tests/        # Tests unitaires
├── frontend/         # Interface React/Svelte
│   └── src/
│       ├── pages/    # Pages
│       ├── components/ # Composants
│       ├── services/ # Client API
│       └── theme/    # Thème dark
├── docs/             # Documentation
└── scripts/          # Scripts utilitaires
```

### Tests

Backend :
```bash
cd backend
pytest
```

Frontend :
```bash
cd frontend
npm test
```

### Ajouter une Règle de Sécurité

Voir [SECURITY_RULES.md](docs/SECURITY_RULES.md) pour la procédure complète.

## Sécurité

- Données stockées localement uniquement
- Pas d'exfiltration
- Pas de télémétrie
- Chiffrement optionnel de la base (post-MVP)

Voir [SECURITY_DESIGN.md](docs/SECURITY_DESIGN.md) pour détails.

## Contributions

Ce projet est actuellement en développement MVP.

Contributions futures :
- Nouvelles règles de sécurité
- Templates d'architectures
- Amélirations UX

## Licence

À définir (usage interne entreprise recommandé)

## Contact

Pour questions ou feedback, consulter la documentation ou créer une issue.

---

**BLACKMANE** - Security by Design Architecture Analysis Tool
