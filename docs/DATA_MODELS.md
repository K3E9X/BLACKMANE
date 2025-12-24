# BLACKMANE - Modèles de Données

## Vue d'ensemble

Ce document décrit les modèles de données utilisés par BLACKMANE.

Les modèles sont définis en deux couches :
1. **Modèles de domaine** (Python Pydantic) : Logique métier
2. **Modèles de persistence** (SQLAlchemy) : Base de données

## Schéma de Base de Données

```sql
-- Projects
CREATE TABLE projects (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    project_type TEXT NOT NULL CHECK(project_type IN ('cloud', 'on-premise', 'hybrid')),
    business_context TEXT,
    criticality_level TEXT NOT NULL CHECK(criticality_level IN ('low', 'medium', 'high', 'critical')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Architectures (1-to-1 avec project)
CREATE TABLE architectures (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Trust Zones
CREATE TABLE zones (
    id TEXT PRIMARY KEY,
    architecture_id TEXT NOT NULL,
    name TEXT NOT NULL,
    trust_level TEXT NOT NULL CHECK(trust_level IN ('untrusted', 'low', 'medium', 'high')),
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (architecture_id) REFERENCES architectures(id) ON DELETE CASCADE
);

-- Components
CREATE TABLE components (
    id TEXT PRIMARY KEY,
    architecture_id TEXT NOT NULL,
    zone_id TEXT NOT NULL,
    name TEXT NOT NULL,
    component_type TEXT NOT NULL,
    has_admin_interface BOOLEAN NOT NULL DEFAULT 0,
    requires_mfa BOOLEAN NOT NULL DEFAULT 0,
    has_logging BOOLEAN NOT NULL DEFAULT 0,
    encryption_at_rest BOOLEAN NOT NULL DEFAULT 0,
    encryption_in_transit BOOLEAN NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (architecture_id) REFERENCES architectures(id) ON DELETE CASCADE,
    FOREIGN KEY (zone_id) REFERENCES zones(id) ON DELETE CASCADE
);

-- Flows between components
CREATE TABLE flows (
    id TEXT PRIMARY KEY,
    architecture_id TEXT NOT NULL,
    source_component_id TEXT NOT NULL,
    target_component_id TEXT NOT NULL,
    protocol TEXT NOT NULL,
    port INTEGER,
    is_authenticated BOOLEAN NOT NULL DEFAULT 0,
    is_encrypted BOOLEAN NOT NULL DEFAULT 0,
    description TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (architecture_id) REFERENCES architectures(id) ON DELETE CASCADE,
    FOREIGN KEY (source_component_id) REFERENCES components(id) ON DELETE CASCADE,
    FOREIGN KEY (target_component_id) REFERENCES components(id) ON DELETE CASCADE
);

-- Analyses
CREATE TABLE analyses (
    id TEXT PRIMARY KEY,
    project_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pending', 'running', 'completed', 'failed')),
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    global_risk_score REAL,
    total_findings INTEGER DEFAULT 0,
    critical_findings INTEGER DEFAULT 0,
    high_findings INTEGER DEFAULT 0,
    medium_findings INTEGER DEFAULT 0,
    low_findings INTEGER DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Findings (security issues detected)
CREATE TABLE findings (
    id TEXT PRIMARY KEY,
    analysis_id TEXT NOT NULL,
    rule_id TEXT NOT NULL,
    rule_name TEXT NOT NULL,
    category TEXT NOT NULL,
    severity TEXT NOT NULL CHECK(severity IN ('critical', 'high', 'medium', 'low')),
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    impact TEXT NOT NULL,
    affected_component_id TEXT,
    affected_flow_id TEXT,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE,
    FOREIGN KEY (affected_component_id) REFERENCES components(id) ON DELETE SET NULL,
    FOREIGN KEY (affected_flow_id) REFERENCES flows(id) ON DELETE SET NULL
);

-- Recommendations
CREATE TABLE recommendations (
    id TEXT PRIMARY KEY,
    finding_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    description TEXT NOT NULL,
    actions TEXT NOT NULL, -- JSON array
    priority TEXT NOT NULL CHECK(priority IN ('critical', 'high', 'medium', 'low')),
    effort TEXT NOT NULL CHECK(effort IN ('low', 'medium', 'high')),
    security_gain TEXT NOT NULL CHECK(security_gain IN ('low', 'medium', 'high')),
    priority_score REAL NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending' CHECK(status IN ('pending', 'accepted', 'rejected', 'implemented')),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (finding_id) REFERENCES findings(id) ON DELETE CASCADE
);

-- Maturity Assessments
CREATE TABLE maturity_assessments (
    id TEXT PRIMARY KEY,
    analysis_id TEXT NOT NULL,
    domain TEXT NOT NULL,
    maturity_level INTEGER NOT NULL CHECK(maturity_level BETWEEN 1 AND 5),
    score_percentage REAL NOT NULL,
    total_rules INTEGER NOT NULL,
    passed_rules INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (analysis_id) REFERENCES analyses(id) ON DELETE CASCADE
);

-- Indexes
CREATE INDEX idx_architectures_project ON architectures(project_id);
CREATE INDEX idx_zones_architecture ON zones(architecture_id);
CREATE INDEX idx_components_architecture ON components(architecture_id);
CREATE INDEX idx_components_zone ON components(zone_id);
CREATE INDEX idx_flows_architecture ON flows(architecture_id);
CREATE INDEX idx_flows_source ON flows(source_component_id);
CREATE INDEX idx_flows_target ON flows(target_component_id);
CREATE INDEX idx_analyses_project ON analyses(project_id);
CREATE INDEX idx_findings_analysis ON findings(analysis_id);
CREATE INDEX idx_findings_severity ON findings(severity);
CREATE INDEX idx_recommendations_finding ON recommendations(finding_id);
CREATE INDEX idx_recommendations_priority ON recommendations(priority_score DESC);
CREATE INDEX idx_maturity_analysis ON maturity_assessments(analysis_id);
```

## Modèles de Domaine (Pydantic)

### Project

```python
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum

class ProjectType(str, Enum):
    CLOUD = "cloud"
    ON_PREMISE = "on-premise"
    HYBRID = "hybrid"

class CriticalityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    project_type: ProjectType
    business_context: Optional[str] = None
    criticality_level: CriticalityLevel

class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    business_context: Optional[str] = None
    criticality_level: Optional[CriticalityLevel] = None

class Project(BaseModel):
    id: str
    name: str
    project_type: ProjectType
    business_context: Optional[str]
    criticality_level: CriticalityLevel
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Architecture

```python
class TrustLevel(str, Enum):
    UNTRUSTED = "untrusted"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ZoneCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    trust_level: TrustLevel
    description: Optional[str] = None

class Zone(BaseModel):
    id: str
    architecture_id: str
    name: str
    trust_level: TrustLevel
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ComponentType(str, Enum):
    FIREWALL = "firewall"
    LOAD_BALANCER = "load_balancer"
    SERVER = "server"
    DATABASE = "database"
    IAM = "iam"
    BASTION = "bastion"
    API_GATEWAY = "api_gateway"
    VPN = "vpn"
    OTHER = "other"

class ComponentCreate(BaseModel):
    zone_id: str
    name: str = Field(..., min_length=1, max_length=100)
    component_type: ComponentType
    has_admin_interface: bool = False
    requires_mfa: bool = False
    has_logging: bool = False
    encryption_at_rest: bool = False
    encryption_in_transit: bool = False
    description: Optional[str] = None

class Component(BaseModel):
    id: str
    architecture_id: str
    zone_id: str
    name: str
    component_type: ComponentType
    has_admin_interface: bool
    requires_mfa: bool
    has_logging: bool
    encryption_at_rest: bool
    encryption_in_transit: bool
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class FlowProtocol(str, Enum):
    HTTP = "http"
    HTTPS = "https"
    SSH = "ssh"
    RDP = "rdp"
    SQL = "sql"
    LDAP = "ldap"
    DNS = "dns"
    SMTP = "smtp"
    OTHER = "other"

class FlowCreate(BaseModel):
    source_component_id: str
    target_component_id: str
    protocol: FlowProtocol
    port: Optional[int] = Field(None, ge=1, le=65535)
    is_authenticated: bool = False
    is_encrypted: bool = False
    description: Optional[str] = None

class Flow(BaseModel):
    id: str
    architecture_id: str
    source_component_id: str
    target_component_id: str
    protocol: FlowProtocol
    port: Optional[int]
    is_authenticated: bool
    is_encrypted: bool
    description: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class ArchitectureCreate(BaseModel):
    description: Optional[str] = None
    zones: list[ZoneCreate] = []
    components: list[ComponentCreate] = []
    flows: list[FlowCreate] = []

class Architecture(BaseModel):
    id: str
    project_id: str
    description: Optional[str]
    zones: list[Zone] = []
    components: list[Component] = []
    flows: list[Flow] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### Analysis & Findings

```python
class AnalysisStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class RuleCategory(str, Enum):
    IDENTITY = "identity"
    NETWORK = "network"
    DATA = "data"
    OBSERVABILITY = "observability"
    ZERO_TRUST = "zero_trust"

class Finding(BaseModel):
    id: str
    analysis_id: str
    rule_id: str
    rule_name: str
    category: RuleCategory
    severity: Severity
    title: str
    description: str
    impact: str
    affected_component_id: Optional[str]
    affected_flow_id: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True

class Analysis(BaseModel):
    id: str
    project_id: str
    status: AnalysisStatus
    started_at: datetime
    completed_at: Optional[datetime]
    global_risk_score: Optional[float]
    total_findings: int
    critical_findings: int
    high_findings: int
    medium_findings: int
    low_findings: int
    findings: list[Finding] = []

    class Config:
        from_attributes = True
```

### Recommendations

```python
class RecommendationDomain(str, Enum):
    IDENTITY = "identity"
    NETWORK = "network"
    DATA = "data"
    MANAGEMENT = "management"
    ARCHITECTURE = "architecture"

class RecommendationPriority(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class EffortLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SecurityGain(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class RecommendationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    IMPLEMENTED = "implemented"

class Recommendation(BaseModel):
    id: str
    finding_id: str
    domain: RecommendationDomain
    description: str
    actions: list[str]
    priority: RecommendationPriority
    effort: EffortLevel
    security_gain: SecurityGain
    priority_score: float
    status: RecommendationStatus
    created_at: datetime

    class Config:
        from_attributes = True
```

### Maturity

```python
class MaturityDomain(str, Enum):
    IDENTITY = "identity"
    NETWORK = "network"
    DATA = "data"
    OBSERVABILITY = "observability"
    ZERO_TRUST = "zero_trust"

class MaturityAssessment(BaseModel):
    id: str
    analysis_id: str
    domain: MaturityDomain
    maturity_level: int = Field(..., ge=1, le=5)
    score_percentage: float
    total_rules: int
    passed_rules: int
    created_at: datetime

    class Config:
        from_attributes = True

class MaturityReport(BaseModel):
    analysis_id: str
    global_maturity_level: float
    assessments: list[MaturityAssessment]
```

### Roadmap

```python
class RoadmapHorizon(str, Enum):
    SHORT_TERM = "short_term"   # 0-3 months
    MEDIUM_TERM = "medium_term" # 3-6 months
    LONG_TERM = "long_term"     # 6-12 months

class RoadmapItem(BaseModel):
    recommendation_id: str
    horizon: RoadmapHorizon
    title: str
    description: str
    priority: RecommendationPriority
    effort: EffortLevel
    security_gain: SecurityGain

class Roadmap(BaseModel):
    project_id: str
    analysis_id: str
    short_term: list[RoadmapItem]
    medium_term: list[RoadmapItem]
    long_term: list[RoadmapItem]
```

## Relations entre Entités

```
Project (1) ─────┬───── (1) Architecture
                 │
                 └───── (N) Analysis

Architecture (1) ─────┬───── (N) Zone
                      │
                      ├───── (N) Component
                      │
                      └───── (N) Flow

Analysis (1) ─────┬───── (N) Finding
                  │
                  └───── (N) MaturityAssessment

Finding (1) ────── (1) Recommendation

Component (1) ────── (N) Flow (as source or target)
Zone (1) ────── (N) Component
```

## Exemples de Données

### Exemple 1 : Architecture Simple Cloud

```json
{
  "project": {
    "name": "Production API Platform",
    "project_type": "cloud",
    "business_context": "SaaS API serving 100k users",
    "criticality_level": "high"
  },
  "architecture": {
    "zones": [
      {
        "name": "Internet",
        "trust_level": "untrusted"
      },
      {
        "name": "DMZ",
        "trust_level": "low"
      },
      {
        "name": "Application",
        "trust_level": "medium"
      },
      {
        "name": "Data",
        "trust_level": "high"
      }
    ],
    "components": [
      {
        "zone_id": "dmz",
        "name": "CloudFront-CDN",
        "component_type": "load_balancer",
        "has_admin_interface": false,
        "encryption_in_transit": true
      },
      {
        "zone_id": "dmz",
        "name": "ALB-Public",
        "component_type": "load_balancer",
        "has_admin_interface": false,
        "encryption_in_transit": true
      },
      {
        "zone_id": "application",
        "name": "API-Gateway",
        "component_type": "api_gateway",
        "has_admin_interface": true,
        "requires_mfa": false,
        "has_logging": true,
        "encryption_in_transit": true
      },
      {
        "zone_id": "data",
        "name": "RDS-PostgreSQL",
        "component_type": "database",
        "has_admin_interface": true,
        "requires_mfa": false,
        "has_logging": true,
        "encryption_at_rest": true,
        "encryption_in_transit": true
      }
    ],
    "flows": [
      {
        "source_component_id": "internet",
        "target_component_id": "cloudfront",
        "protocol": "https",
        "port": 443,
        "is_encrypted": true,
        "is_authenticated": false
      },
      {
        "source_component_id": "cloudfront",
        "target_component_id": "alb",
        "protocol": "https",
        "port": 443,
        "is_encrypted": true,
        "is_authenticated": false
      },
      {
        "source_component_id": "api-gateway",
        "target_component_id": "rds",
        "protocol": "sql",
        "port": 5432,
        "is_encrypted": true,
        "is_authenticated": true
      }
    ]
  }
}
```

### Exemple 2 : Finding & Recommendation

```json
{
  "finding": {
    "rule_id": "SEC-001",
    "rule_name": "Admin Access Without MFA",
    "category": "identity",
    "severity": "high",
    "title": "API-Gateway admin interface accessible without MFA",
    "description": "The API-Gateway component has an admin interface enabled but does not require MFA for authentication",
    "impact": "If administrative credentials are compromised, an attacker could gain full control of the API Gateway without additional authentication factors",
    "affected_component_id": "api-gateway-123"
  },
  "recommendation": {
    "domain": "identity",
    "description": "Enable MFA for all administrative access to API Gateway",
    "actions": [
      "Deploy MFA solution (AWS IAM MFA, TOTP, or FIDO2)",
      "Configure API Gateway to enforce MFA on admin endpoints",
      "Update access policies to require MFA for privileged operations",
      "Train administrators on MFA usage"
    ],
    "priority": "high",
    "effort": "medium",
    "security_gain": "high",
    "priority_score": 8.5
  }
}
```

## Calculs et Formules

### Priority Score

```python
def calculate_priority_score(
    severity: Severity,
    security_gain: SecurityGain,
    effort: EffortLevel
) -> float:
    severity_weight = {"critical": 4, "high": 3, "medium": 2, "low": 1}
    gain_weight = {"high": 3, "medium": 2, "low": 1}
    effort_weight = {"low": 3, "medium": 2, "high": 1}

    score = (
        severity_weight[severity] * 3 +
        gain_weight[security_gain] * 2
    ) / effort_weight[effort]

    return round(score, 2)
```

### Global Risk Score

```python
def calculate_global_risk_score(findings: list[Finding]) -> float:
    if not findings:
        return 0.0

    severity_scores = {"critical": 10, "high": 7, "medium": 4, "low": 2}
    total_score = sum(severity_scores[f.severity] for f in findings)
    max_score = len(findings) * 10

    return round((total_score / max_score) * 100, 2)
```

### Maturity Level

```python
def calculate_maturity_level(passed_rules: int, total_rules: int) -> int:
    if total_rules == 0:
        return 1

    percentage = (passed_rules / total_rules) * 100

    if percentage < 20:
        return 1
    elif percentage < 40:
        return 2
    elif percentage < 60:
        return 3
    elif percentage < 80:
        return 4
    else:
        return 5
```

## Contraintes et Validations

### Validations métier

1. **Zone** : Un composant doit appartenir à une zone existante
2. **Flow** : Source et destination doivent être des composants différents
3. **Flow** : Un flux ne peut pas traverser plus de 2 zones sans justification
4. **Component** : Un composant avec `has_admin_interface=True` devrait avoir `requires_mfa=True`
5. **Analysis** : Une seule analyse "running" par projet à la fois

### Contraintes d'intégrité

- Suppression en cascade : Project → Architecture → (Zones, Components, Flows)
- Suppression en cascade : Analysis → Findings → Recommendations
- Unicité : Un projet ne peut avoir qu'une architecture active

## Migration et Évolution

Pour ajouter de nouveaux champs :

```python
# Utiliser Alembic pour migrations SQLAlchemy
alembic revision --autogenerate -m "Add new field to components"
alembic upgrade head
```

Versionning du schéma recommandé pour compatibilité future.
