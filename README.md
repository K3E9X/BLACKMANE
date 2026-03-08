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

### Installation Rapide sur macOS M1/M2/M3 (Recommandé)

BLACKMANE est 100% compatible avec Apple Silicon. Installation automatique :

```bash
# Installation automatique complète
./scripts/setup-macos.sh
```

Ce script va :
- Vérifier Python et Node.js (et les installer via Homebrew si nécessaire)
- Créer l'environnement virtuel Python (ARM64 natif)
- Installer toutes les dépendances backend et frontend
- Optimiser pour Apple Silicon

**Documentation complète** : Voir [docs/MACOS_M1.md](docs/MACOS_M1.md)

### Installation Manuelle (Linux / Windows / macOS manuel)

#### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### Frontend

```bash
cd frontend
npm install
```

## Lancement

### Démarrage Rapide sur macOS (Recommandé)

```bash
# Lancement automatique backend + frontend
./scripts/start-macos.sh
```

Le script va :
- Démarrer le backend sur http://127.0.0.1:8000
- Démarrer le frontend sur http://127.0.0.1:5173
- Gérer les logs dans ~/Library/Logs/BLACKMANE/
- Appuyez sur Ctrl+C pour tout arrêter

### Démarrage Manuel

**Terminal 1 (Backend)** :
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 (Frontend)** :
```bash
cd frontend
npm run dev
```

**Application disponible sur** : `http://localhost:5173`

### Linux / Démarrage Automatique

```bash
./scripts/start.sh
```

### Déploiement Docker Compose

```bash
# Build et run
docker compose up --build
```

Services :
- Frontend : `http://localhost:5173`
- Backend API : `http://localhost:8000`

Arrêt :
```bash
docker compose down
```

### Déploiement Kubernetes

Les manifests sont dans `deploy/k8s/`.

```bash
# 1) Build des images localement
# (adapte selon ton registry)
docker build -f backend/Dockerfile -t blackmane-backend:latest .
docker build -f frontend/Dockerfile -t blackmane-frontend:latest .

# 2) Apply
kubectl apply -k deploy/k8s
```

Exemple d'accès (ingress nginx) :
- Host: `blackmane.local`
- Ajoute `blackmane.local` dans `/etc/hosts` vers ton ingress controller.


### Résolution rapide des conflits (check global)

1) Vérifier s'il reste des conflits :

```bash
./scripts/check-conflicts.sh
```

2) Résoudre automatiquement les conflits connus (README + manifests k8s prod-ready) :

```bash
./scripts/resolve-known-conflicts.sh
```

3) Vérifier à nouveau, puis finaliser :

```bash
./scripts/check-conflicts.sh
git commit -m "Resolve merge conflicts"
git push
```

> Si des fichiers hors liste restent en conflit, le script s'arrête et te les affiche pour résolution manuelle.

### Déploiement Production-Ready (GHCR + Kubernetes + TLS + CI/CD)

Cette version inclut :
- Pipeline GitHub Actions CI/CD : `.github/workflows/ci-cd.yml`
- Publication d'images sur GHCR (`blackmane-backend`, `blackmane-frontend`)
- Déploiement Kubernetes automatisé (`kubectl apply -k deploy/k8s`)
- Ingress TLS (secret `blackmane-tls`, annotation cert-manager)
- Variables et secrets Kubernetes (`ConfigMap` + `Secret`)

#### 1) Préparer GitHub Secrets

Ajoute ces secrets dans le repository GitHub :
- `KUBE_CONFIG_DATA` : kubeconfig encodé en base64
- `GHCR_PULL_TOKEN` : token lecture package GHCR pour le cluster

Exemple pour générer `KUBE_CONFIG_DATA` :
```bash
base64 -w 0 ~/.kube/config
```

#### 2) Adapter les images Kubernetes

Par défaut, les manifests utilisent des placeholders :
- `ghcr.io/your-org/blackmane-backend:latest`
- `ghcr.io/your-org/blackmane-frontend:latest`

Le workflow les remplace automatiquement par un tag SHA lors du job `deploy`.

#### 3) Configurer TLS

L'Ingress est prêt pour cert-manager :
- annotation `cert-manager.io/cluster-issuer: letsencrypt-prod`
- secret TLS cible : `blackmane-tls`

Assure-toi d'avoir :
- ingress-nginx installé
- cert-manager installé
- un `ClusterIssuer` nommé `letsencrypt-prod`

#### 4) Variables / secrets applicatifs

- `deploy/k8s/configmap-app.yaml` : variables non sensibles
- `deploy/k8s/secret-app.yaml` : secrets applicatifs (à surcharger en environnement réel)

⚠️ Change impérativement `SECRET_KEY` avant la mise en production.

## Documentation

- [Architecture](docs/ARCHITECTURE.md) - Architecture logicielle détaillée
- [MVP](docs/MVP.md) - Périmètre MVP
- [Modèles de Données](docs/DATA_MODELS.md) - Schéma de données
- [Règles de Sécurité](docs/SECURITY_RULES.md) - Règles d'analyse
- [Security Design](docs/SECURITY_DESIGN.md) - Sécurité de l'outil
- [Roadmap](docs/ROADMAP.md) - Plan de développement
- [macOS M1/M2/M3](docs/MACOS_M1.md) - Guide spécifique Apple Silicon

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
