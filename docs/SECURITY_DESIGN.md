# BLACKMANE - Security Design

## Introduction

BLACKMANE étant un outil d'analyse de sécurité destiné à un usage en entreprise, sa propre sécurité est critique.

Ce document définit les mesures de sécurité implémentées dans l'outil lui-même.

## Principes de Sécurité

1. **Local First** - Pas de dépendance cloud obligatoire
2. **No Exfiltration** - Aucune donnée ne quitte la machine
3. **Privacy by Design** - Pas de télémétrie par défaut
4. **Least Privilege** - Droits minimaux nécessaires
5. **Defense in Depth** - Multiples couches de sécurité
6. **Fail Secure** - Comportement sûr en cas d'erreur

## Menaces et Mitigations

### Threat Model

#### T-01 : Exfiltration de Données Sensibles

**Menace** : Les architectures analysées contiennent des informations sensibles (topology, IP, noms de serveurs).

**Mitigations** :
- Pas d'accès réseau non sollicité par le backend
- Validation stricte de toutes les sorties réseau
- Logs locaux uniquement
- Option de chiffrement de la base de données
- Pas de télémétrie par défaut
- Code review pour détecter tout appel réseau non autorisé

**Contrôles** :
```python
# Blocage explicite des appels réseau non autorisés
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Validation des URLs (si import PDF/image depuis URL)
def validate_url(url: str) -> bool:
    if not url.startswith("file://"):
        raise SecurityError("Only local file:// URLs allowed")
```

---

#### T-02 : Injection de Code

**Menace** : Injection via inputs utilisateur (noms de composants, descriptions, etc.).

**Mitigations** :
- Validation stricte avec Pydantic
- Pas d'`eval()` ou `exec()`
- Pas de templating dynamique avec code
- Parameterized queries (SQLAlchemy ORM)
- Sanitization des inputs

**Contrôles** :
```python
# Validation Pydantic
class ComponentCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, pattern="^[a-zA-Z0-9-_ ]+$")

# SQLAlchemy (pas de SQL raw)
session.query(Component).filter(Component.id == component_id).first()
# Jamais : session.execute(f"SELECT * FROM components WHERE id = '{component_id}'")
```

---

#### T-03 : Path Traversal

**Menace** : Upload de fichiers malveillants ou accès à des fichiers système.

**Mitigations** :
- Validation stricte des chemins de fichiers
- Stockage des uploads dans un répertoire dédié
- Pas d'accès direct au filesystem via API
- Validation des extensions de fichiers

**Contrôles** :
```python
import os
from pathlib import Path

UPLOAD_DIR = Path("/var/blackmane/uploads")

def validate_upload_path(filename: str) -> Path:
    # Nettoyer le nom de fichier
    safe_name = os.path.basename(filename)

    # Interdire les caractères dangereux
    if ".." in safe_name or "/" in safe_name or "\\" in safe_name:
        raise SecurityError("Invalid filename")

    full_path = UPLOAD_DIR / safe_name

    # Vérifier que le chemin résolu est bien dans UPLOAD_DIR
    if not full_path.resolve().is_relative_to(UPLOAD_DIR.resolve()):
        raise SecurityError("Path traversal detected")

    return full_path
```

---

#### T-04 : Denial of Service

**Menace** : Analyse d'architectures très complexes causant une surcharge CPU/mémoire.

**Mitigations** :
- Limites sur le nombre de composants (max 500 pour MVP)
- Timeout sur les analyses (max 30 secondes)
- Validation de la taille des uploads (max 10MB)
- Rate limiting sur l'API (optionnel)

**Contrôles** :
```python
# Limites architecturales
MAX_COMPONENTS = 500
MAX_FLOWS = 1000
MAX_ZONES = 50

# Timeout analysis
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Analysis timeout")

signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(30)  # 30 secondes
try:
    result = analyze_architecture(architecture)
finally:
    signal.alarm(0)
```

---

#### T-05 : Authentification/Autorisation (Post-MVP)

**Menace** : Accès non autorisé aux données (si multi-utilisateur).

**Mitigations** :
- MVP : Single user, local only (127.0.0.1)
- Post-MVP : Authentification locale (pas de SSO externe)
- Isolation par projet
- Pas de compte par défaut

**Contrôles** :
```python
# MVP : Binding localhost uniquement
uvicorn.run(app, host="127.0.0.1", port=8000)

# Post-MVP : Authentification basique
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
```

---

#### T-06 : Dépendances Vulnérables

**Menace** : Utilisation de libraries avec des CVE connues.

**Mitigations** :
- Scanning régulier avec `pip-audit` ou `safety`
- Pinning des versions exactes
- Revue des dépendances avant ajout
- Mise à jour régulière

**Contrôles** :
```bash
# CI/CD pipeline
pip-audit
safety check

# requirements.txt avec versions exactes
fastapi==0.104.1
pydantic==2.5.0
```

---

#### T-07 : Logs Contenant des Données Sensibles

**Menace** : Fuite d'informations sensibles via logs.

**Mitigations** :
- Pas de log de données utilisateur
- Structuration des logs (JSON)
- Sanitization automatique
- Logs locaux uniquement

**Contrôles** :
```python
import logging
import json

# Configuration logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Jamais :
# logging.info(f"User input: {user_data}")

# Préférer :
logging.info("Architecture created", extra={"project_id": project.id})
```

---

## Sécurisation de la Base de Données

### Chiffrement (Post-MVP)

Utiliser SQLCipher pour chiffrer la base SQLite.

```python
from sqlalchemy import create_engine

# Avec chiffrement
engine = create_engine(
    'sqlite:///blackmane.db',
    connect_args={'pragmas': {'key': get_encryption_key()}}
)

def get_encryption_key() -> str:
    # Récupérer depuis variable d'environnement ou keyring système
    import keyring
    key = keyring.get_password("blackmane", "db_key")
    if not key:
        # Générer et stocker
        key = secrets.token_urlsafe(32)
        keyring.set_password("blackmane", "db_key", key)
    return key
```

### Permissions Fichier

```bash
# Base de données accessible seulement par l'utilisateur
chmod 600 blackmane.db
```

### Backup Sécurisé

```python
import shutil
from datetime import datetime

def backup_database():
    backup_path = f"blackmane_backup_{datetime.now().isoformat()}.db"
    shutil.copy2("blackmane.db", backup_path)
    os.chmod(backup_path, 0o600)
```

---

## Sécurisation de l'API

### CORS

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Frontend dev
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)
```

### Rate Limiting (optionnel)

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/api/v1/projects")
@limiter.limit("10/minute")
async def create_project(request: Request, project: ProjectCreate):
    pass
```

### Validation des Inputs

Tous les endpoints utilisent Pydantic pour validation stricte.

```python
from pydantic import BaseModel, Field, validator

class ProjectCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)

    @validator('name')
    def name_must_be_safe(cls, v):
        if '<' in v or '>' in v or ';' in v:
            raise ValueError('Invalid characters in name')
        return v
```

### Headers de Sécurité

```python
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["localhost", "127.0.0.1"]
)

@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000"
    return response
```

---

## Sécurisation du Frontend

### Content Security Policy

```html
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self';
               script-src 'self';
               style-src 'self' 'unsafe-inline';
               img-src 'self' data:;
               connect-src 'self' http://localhost:8000;">
```

### Validation Côté Client

Ne jamais faire confiance aux validations frontend - toujours valider côté serveur.

### Sanitization des Données Affichées

```typescript
import DOMPurify from 'dompurify';

function displayDescription(description: string) {
    return DOMPurify.sanitize(description);
}
```

### Protection XSS

React protège automatiquement contre XSS, mais attention aux `dangerouslySetInnerHTML`.

```typescript
// Jamais :
<div dangerouslySetInnerHTML={{__html: userInput}} />

// Préférer :
<div>{userInput}</div>
```

---

## Gestion des Secrets

### Pas de Secrets en Dur

```python
# Jamais :
API_KEY = "sk-1234567890abcdef"

# Préférer :
import os
API_KEY = os.getenv("BLACKMANE_API_KEY")
```

### Variables d'Environnement

```bash
# .env (à ne jamais commit)
DATABASE_URL=sqlite:///blackmane.db
LOG_LEVEL=INFO
```

```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
```

### Gitignore

```
.env
*.db
*.db-journal
*.log
uploads/
__pycache__/
*.pyc
```

---

## Audit et Monitoring

### Logs d'Audit

Enregistrer toutes les actions sensibles :

```python
def audit_log(action: str, user: str, details: dict):
    logging.info(
        "AUDIT",
        extra={
            "action": action,
            "user": user,
            "timestamp": datetime.now().isoformat(),
            "details": details
        }
    )

# Usage
audit_log("project_created", "admin", {"project_id": project.id})
audit_log("analysis_run", "admin", {"project_id": project.id, "findings_count": 5})
```

### Monitoring des Erreurs

```python
import logging

# Log des exceptions
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(
        f"Unhandled exception: {exc}",
        exc_info=True,
        extra={"path": request.url.path}
    )
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

---

## Déploiement Sécurisé

### Environnement de Production

```bash
# Désactiver le mode debug
export DEBUG=False

# Utiliser un serveur ASGI production
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

# Binding localhost uniquement
--bind 127.0.0.1:8000
```

### Permissions Système

```bash
# Créer un utilisateur dédié
sudo useradd -r -s /bin/false blackmane

# Donner les permissions minimales
sudo chown -R blackmane:blackmane /opt/blackmane
sudo chmod 750 /opt/blackmane
```

### Isolation (optionnel)

Pour une isolation renforcée, utiliser Docker :

```dockerfile
FROM python:3.11-slim

# User non-root
RUN useradd -m -u 1000 blackmane
USER blackmane

WORKDIR /app
COPY --chown=blackmane:blackmane . .

RUN pip install --no-cache-dir -r requirements.txt

# Pas d'accès réseau externe
# Network mode: none ou internal

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]
```

---

## Tests de Sécurité

### Tests Automatisés

```python
def test_sql_injection():
    malicious_input = "'; DROP TABLE projects; --"
    response = client.post("/api/v1/projects", json={
        "name": malicious_input,
        "project_type": "cloud",
        "criticality_level": "high"
    })
    # Doit échouer à la validation
    assert response.status_code == 422

def test_path_traversal():
    malicious_path = "../../etc/passwd"
    response = client.post("/api/v1/upload", files={
        "file": (malicious_path, b"content")
    })
    assert response.status_code == 400

def test_xss():
    xss_payload = "<script>alert('xss')</script>"
    project = create_project(name=xss_payload)
    # Le nom doit être échappé
    assert "<script>" not in str(project.name)
```

### Checklist Sécurité

Avant chaque release :

- [ ] `pip-audit` sans vulnérabilités critiques
- [ ] Tests de sécurité passent
- [ ] Pas de secrets en dur dans le code
- [ ] `.env` dans `.gitignore`
- [ ] Logs ne contiennent pas de données sensibles
- [ ] CORS configuré correctement
- [ ] Headers de sécurité présents
- [ ] Validation stricte sur tous les endpoints
- [ ] Permissions fichiers correctes
- [ ] Documentation de sécurité à jour

---

## Gestion des Incidents

### Procédure en Cas de Vulnérabilité

1. **Détection** : Via audit automatique ou report
2. **Évaluation** : Criticité et impact
3. **Correction** : Patch urgent si critique
4. **Communication** : Notification aux utilisateurs si nécessaire
5. **Post-mortem** : Analyse et amélioration

### Contact Sécurité

Définir un canal de report de vulnérabilités :
- Email dédié : security@blackmane.local
- Délai de réponse : 48h
- Politique de divulgation responsable

---

## Conformité

### RGPD (si applicable)

Si des données personnelles sont traitées (post-MVP avec multi-users) :

- Droit d'accès : Export des données utilisateur
- Droit à l'effacement : Suppression complète
- Privacy by Design : Minimisation des données
- Pas de transfert hors UE

### ISO 27001

Alignement avec les contrôles :
- A.9 : Contrôle d'accès
- A.12 : Sécurité des opérations
- A.14 : Sécurité dans le développement

---

## Checklist de Sécurité pour Développeurs

Avant chaque commit :

- [ ] Pas de credentials en dur
- [ ] Validation de tous les inputs
- [ ] Pas d'appel réseau non autorisé
- [ ] Logs sans données sensibles
- [ ] Tests de sécurité ajoutés
- [ ] Dépendances à jour
- [ ] Code review sécurité

---

## Conclusion

La sécurité de BLACKMANE est critique car l'outil traite des informations sensibles sur les architectures d'entreprise.

Cette approche Security by Design garantit :
- Protection des données
- Confidentialité
- Intégrité
- Disponibilité

Et maintient la confiance des utilisateurs.
