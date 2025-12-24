# BLACKMANE - Architecture Logicielle

## Vue d'ensemble

BLACKMANE est un outil local d'analyse d'architectures sécurisées basé sur les principes Security by Design et Zero Trust pragmatique.

### Principes architecturaux

1. **Local First** - Aucune dépendance cloud obligatoire
2. **Modularité** - Composants découplés et extensibles
3. **Sécurité** - Pas d'exfiltration, données locales uniquement
4. **Simplicité** - Pas de sur-ingénierie, architecture claire
5. **Extensibilité** - Ajout facile de nouvelles règles et environnements

## Architecture Globale

```
┌─────────────────────────────────────────────────────────────┐
│                     BLACKMANE (Local)                        │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌────────────────────────────────────────────────────┐     │
│  │            Frontend (Web Local)                    │     │
│  │  - Interface utilisateur (React/Svelte)            │     │
│  │  - Dark theme natif                                │     │
│  │  - Visualisation architectures                     │     │
│  │  - Gestion projets                                 │     │
│  └─────────────────┬──────────────────────────────────┘     │
│                    │ HTTP (localhost)                       │
│  ┌─────────────────▼──────────────────────────────────┐     │
│  │            Backend API (FastAPI)                   │     │
│  │                                                     │     │
│  │  ┌──────────────────────────────────────────┐      │     │
│  │  │  API Layer (REST)                        │      │     │
│  │  │  - Projets                               │      │     │
│  │  │  - Architectures                         │      │     │
│  │  │  - Analyses                               │      │     │
│  │  │  - Recommandations                       │      │     │
│  │  └──────────────┬───────────────────────────┘      │     │
│  │                 │                                   │     │
│  │  ┌──────────────▼───────────────────────────┐      │     │
│  │  │  Service Layer (Business Logic)         │      │     │
│  │  │  - ProjectService                        │      │     │
│  │  │  - ArchitectureService                   │      │     │
│  │  │  - AnalysisService                       │      │     │
│  │  │  - RecommendationService                 │      │     │
│  │  │  - MaturityService                       │      │     │
│  │  └──────────────┬───────────────────────────┘      │     │
│  │                 │                                   │     │
│  │  ┌──────────────▼───────────────────────────┐      │     │
│  │  │  Core Engine                             │      │     │
│  │  │  - RuleEngine (moteur de règles)         │      │     │
│  │  │  - ArchitectureParser                    │      │     │
│  │  │  - ThreatAnalyzer                        │      │     │
│  │  │  - MaturityEvaluator                     │      │     │
│  │  └──────────────┬───────────────────────────┘      │     │
│  │                 │                                   │     │
│  │  ┌──────────────▼───────────────────────────┐      │     │
│  │  │  Data Access Layer                       │      │     │
│  │  │  - Repository pattern                    │      │     │
│  │  │  - ProjectRepository                     │      │     │
│  │  │  - ArchitectureRepository                │      │     │
│  │  │  - AnalysisRepository                    │      │     │
│  │  └──────────────┬───────────────────────────┘      │     │
│  └─────────────────┼───────────────────────────────────┘     │
│                    │                                         │
│  ┌─────────────────▼───────────────────────────┐             │
│  │  Storage Layer (SQLite)                     │             │
│  │  - projects.db                              │             │
│  │  - Données locales chiffrées                │             │
│  └─────────────────────────────────────────────┘             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Composants Détaillés

### 1. Frontend (Web Local)

**Technologie recommandée** : React + Vite ou Svelte

**Responsabilités** :
- Interface utilisateur dark mode
- Gestion des projets
- Upload et visualisation d'images/PDF
- Affichage des résultats d'analyse
- Visualisation des recommandations
- Roadmap de sécurité

**Modules principaux** :
```
frontend/
├── src/
│   ├── pages/
│   │   ├── ProjectList.tsx          # Liste des projets
│   │   ├── ProjectCreate.tsx        # Création projet
│   │   ├── ArchitectureInput.tsx    # Input architecture
│   │   ├── ArchitectureModel.tsx    # Modélisation
│   │   ├── Analysis.tsx             # Résultats d'analyse
│   │   └── Roadmap.tsx              # Roadmap sécurité
│   ├── components/
│   │   ├── ArchitectureViewer/      # Visualisation schémas
│   │   ├── FindingsList/            # Liste des findings
│   │   ├── RecommendationCard/      # Cartes recommandations
│   │   └── MaturityRadar/           # Radar de maturité
│   ├── services/
│   │   └── api.ts                   # Client API
│   └── theme/
│       └── dark.ts                  # Thème dark
```

### 2. Backend API (FastAPI)

**Technologie** : Python 3.11+, FastAPI

**Architecture en couches** :

#### 2.1 API Layer
Routes HTTP exposant les fonctionnalités.

```python
# Endpoints principaux
POST   /api/v1/projects
GET    /api/v1/projects
GET    /api/v1/projects/{id}
DELETE /api/v1/projects/{id}

POST   /api/v1/projects/{id}/architecture
GET    /api/v1/projects/{id}/architecture

POST   /api/v1/projects/{id}/analyze
GET    /api/v1/projects/{id}/analysis
GET    /api/v1/projects/{id}/findings

GET    /api/v1/projects/{id}/recommendations
POST   /api/v1/projects/{id}/recommendations/{rec_id}/accept

GET    /api/v1/projects/{id}/maturity
GET    /api/v1/projects/{id}/roadmap
```

#### 2.2 Service Layer
Logique métier isolée de l'API.

**ProjectService** :
- Création/suppression de projets
- Gestion du cycle de vie

**ArchitectureService** :
- Parsing d'images/PDF (OCR avec Tesseract)
- Extraction de composants
- Construction du modèle interne
- Validation humaine

**AnalysisService** :
- Orchestration de l'analyse
- Exécution des règles via RuleEngine
- Agrégation des résultats
- Calcul de criticité globale

**RecommendationService** :
- Génération de recommandations
- Priorisation (impact/effort)
- Suivi d'implémentation

**MaturityService** :
- Évaluation de maturité
- Définition de cibles
- Construction de roadmap

#### 2.3 Core Engine

**RuleEngine** :
Moteur de règles extensible basé sur un pattern Strategy.

```python
class Rule:
    id: str
    name: str
    description: str
    category: RuleCategory  # ZeroTrust, Segmentation, Identity, etc.
    severity: Severity      # Critical, High, Medium, Low

    def evaluate(self, architecture: Architecture) -> List[Finding]
```

**ArchitectureParser** :
- Extraction de composants depuis schémas
- Identification de zones
- Détection de flux
- Assistance IA optionnelle (vision API locale ou déportée selon config)

**ThreatAnalyzer** :
- Analyse des zones de confiance
- Détection de surfaces d'attaque
- Évaluation des chemins critiques

**MaturityEvaluator** :
- Évaluation par domaine (Identity, Network, Data, etc.)
- Scoring de maturité (1-5)
- Benchmark interne

#### 2.4 Data Access Layer

Pattern Repository pour isolation de la persistence.

```python
class ProjectRepository:
    def create(project: Project) -> Project
    def get(project_id: str) -> Optional[Project]
    def list() -> List[Project]
    def delete(project_id: str) -> bool

class ArchitectureRepository:
    def save(architecture: Architecture) -> Architecture
    def get(project_id: str) -> Optional[Architecture]

class AnalysisRepository:
    def save(analysis: Analysis) -> Analysis
    def get_latest(project_id: str) -> Optional[Analysis]
    def get_history(project_id: str) -> List[Analysis]
```

### 3. Storage Layer

**Technologie** : SQLite

**Base de données unique** : `blackmane.db`

**Tables principales** :
- `projects` - Projets d'architecture
- `architectures` - Modèles d'architecture
- `components` - Composants identifiés
- `zones` - Zones de confiance
- `flows` - Flux inter-composants
- `analyses` - Historique d'analyses
- `findings` - Faiblesses détectées
- `recommendations` - Recommandations générées
- `maturity_assessments` - Évaluations de maturité

**Sécurité du stockage** :
- Base SQLite avec SQLCipher (chiffrement optionnel)
- Pas de mot de passe en clair
- Logs structurés sans données sensibles

## Flux de Données

### Flux 1 : Création de projet
```
User → Frontend → POST /api/v1/projects → ProjectService → ProjectRepository → SQLite
```

### Flux 2 : Analyse d'architecture
```
User uploads image
  ↓
Frontend → POST /api/v1/projects/{id}/architecture (multipart/form-data)
  ↓
ArchitectureService
  ↓
ArchitectureParser (OCR + extraction)
  ↓
User validation/correction
  ↓
ArchitectureRepository.save()
  ↓
POST /api/v1/projects/{id}/analyze
  ↓
AnalysisService
  ↓
RuleEngine.evaluate_all()
  ↓
ThreatAnalyzer
  ↓
AnalysisRepository.save()
  ↓
Frontend displays findings
```

### Flux 3 : Génération de recommandations
```
Analysis results
  ↓
RecommendationService
  ↓
For each finding:
  - Generate recommendation
  - Estimate effort
  - Calculate priority
  ↓
RecommendationRepository.save()
  ↓
Frontend displays prioritized recommendations
```

## Extensibilité

### Ajout d'une nouvelle règle

```python
# backend/core/rules/custom_rule.py
from backend.core.rule_engine import Rule, Finding

class NoMFAOnAdminAccessRule(Rule):
    def __init__(self):
        super().__init__(
            id="SEC-001",
            name="Admin access without MFA",
            description="Administrative access detected without MFA requirement",
            category=RuleCategory.IDENTITY,
            severity=Severity.HIGH
        )

    def evaluate(self, architecture: Architecture) -> List[Finding]:
        findings = []
        for component in architecture.components:
            if component.is_admin_interface and not component.requires_mfa:
                findings.append(Finding(
                    rule_id=self.id,
                    component_id=component.id,
                    description=f"{component.name} allows admin access without MFA",
                    impact="Unauthorized access risk if credentials compromised",
                    recommendation="Enforce MFA on all administrative interfaces"
                ))
        return findings
```

Enregistrement dans `backend/core/rule_engine.py` :
```python
RULE_REGISTRY = [
    NoMFAOnAdminAccessRule(),
    # ... autres règles
]
```

### Ajout d'un nouveau type d'environnement

Créer un parser spécifique :
```python
# backend/parsers/kubernetes_parser.py
class KubernetesArchitectureParser(ArchitectureParser):
    def parse(self, input_data) -> Architecture:
        # Logique spécifique K8s
        pass
```

## Considérations Non-Fonctionnelles

### Performance
- Analyse d'une architecture : < 5 secondes pour 50 composants
- Interface réactive (< 100ms pour navigation)
- Base SQLite suffisante jusqu'à 1000 projets

### Sécurité
- Pas de code execution dynamique
- Validation stricte des inputs
- Pas d'accès réseau non sollicité
- Logs sans données sensibles
- Chiffrement optionnel de la base

### Maintenabilité
- Couverture de tests : > 80%
- Typing Python strict (mypy)
- Documentation code (docstrings)
- Séparation claire des responsabilités

### Observabilité
- Logs structurés (JSON)
- Pas de télémétrie externe
- Métriques internes optionnelles (nombre d'analyses, temps moyen)

## Stack Technologique

### Backend
- **Python 3.11+**
- **FastAPI** - Framework API
- **Pydantic** - Validation et sérialisation
- **SQLAlchemy** - ORM
- **SQLite** - Base de données
- **pytest** - Tests
- **mypy** - Type checking
- **black** - Formatage code
- **ruff** - Linting

### Frontend
- **React 18+** ou **Svelte 4+**
- **Vite** - Build tool
- **TypeScript** - Typage
- **TailwindCSS** - Styling (dark theme)
- **Vitest** - Tests
- **React Query** ou **SWR** - Data fetching

### Optionnel (selon évolution)
- **Tesseract OCR** - Extraction texte images
- **PyMuPDF** - Parsing PDF
- **Local LLM** (Ollama) - Assistance extraction (opt-in)

## Déploiement

### Mode développement
```bash
# Backend
cd backend
python -m uvicorn main:app --reload

# Frontend
cd frontend
npm run dev
```

### Mode production (local)
```bash
# Build frontend
cd frontend
npm run build

# Servir via FastAPI
cd backend
python -m uvicorn main:app --host 127.0.0.1 --port 8000
```

L'application tourne sur `http://localhost:8000`

### Packaging (future)
- Electron wrapper pour distribution desktop
- Ou binaire Python (PyInstaller)

## Prochaines Étapes

Voir `docs/ROADMAP.md` pour la séquence de développement.
