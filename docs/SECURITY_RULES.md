# BLACKMANE - Règles d'Analyse Sécurité

## Introduction

Ce document définit le premier set de règles d'analyse pour le MVP de BLACKMANE.

Chaque règle :
- Identifie une faiblesse architecturale
- Suit les principes Zero Trust et Security by Design
- Génère un Finding avec recommandation associée
- Est extensible et paramétrable

## Format de Règle

```python
class Rule:
    id: str                      # Identifiant unique (ex: SEC-001)
    name: str                    # Nom court de la règle
    description: str             # Description détaillée
    category: RuleCategory       # Catégorie (Identity, Network, etc.)
    severity: Severity           # Criticité par défaut
    rationale: str               # Justification sécurité (pourquoi cette règle)

    def evaluate(self, architecture: Architecture) -> List[Finding]:
        # Logique d'évaluation
        pass

    def generate_recommendation(self, finding: Finding) -> Recommendation:
        # Génération de recommandation
        pass
```

## Règles MVP (15 règles)

### Catégorie : Identity & Access Management

#### SEC-001 : Admin Access Without MFA

**Description** : Détecte les composants avec interface d'administration sans MFA obligatoire.

**Rationale** : L'authentification multi-facteurs est essentielle pour protéger les accès privilégiés contre le vol de credentials.

**Logique** :
```python
for component in architecture.components:
    if component.has_admin_interface and not component.requires_mfa:
        yield Finding(
            rule_id="SEC-001",
            severity=Severity.HIGH,
            title=f"Admin interface without MFA on {component.name}",
            description=f"Component {component.name} has administrative access without MFA requirement",
            impact="Risk of unauthorized access if credentials are compromised",
            affected_component_id=component.id
        )
```

**Recommendation** :
- Domain: Identity
- Actions:
  - Deploy MFA solution (TOTP, FIDO2, smart cards)
  - Configure component to enforce MFA on admin endpoints
  - Update access policies
  - Train administrators
- Effort: Medium
- Security Gain: High

---

#### SEC-002 : Critical Component Without Authentication

**Description** : Composant critique accessible sans authentification.

**Rationale** : Tout composant critique doit avoir un contrôle d'accès strict.

**Logique** :
```python
critical_types = [ComponentType.DATABASE, ComponentType.IAM, ComponentType.API_GATEWAY]

for component in architecture.components:
    if component.component_type in critical_types:
        # Vérifier les flux entrants
        incoming_flows = [f for f in architecture.flows if f.target_component_id == component.id]
        unauthenticated_flows = [f for f in incoming_flows if not f.is_authenticated]

        if unauthenticated_flows:
            yield Finding(
                rule_id="SEC-002",
                severity=Severity.CRITICAL,
                title=f"Critical component {component.name} accessible without authentication",
                description=f"{len(unauthenticated_flows)} unauthenticated flow(s) to critical component",
                impact="Unauthorized access to sensitive resources",
                affected_component_id=component.id
            )
```

**Recommendation** :
- Domain: Identity
- Actions:
  - Implement authentication on all incoming flows
  - Use OAuth2, JWT, or mutual TLS
  - Review and restrict network access
- Effort: Medium
- Security Gain: High

---

#### SEC-003 : Direct Internet Access to Internal Zone

**Description** : Détecte les accès directs depuis Internet vers des zones internes (non DMZ).

**Rationale** : Principe Zero Trust : tout accès depuis Internet doit passer par une zone de contrôle (DMZ).

**Logique** :
```python
internet_zone = next((z for z in architecture.zones if z.trust_level == TrustLevel.UNTRUSTED), None)
if not internet_zone:
    return  # Pas de zone Internet définie

for flow in architecture.flows:
    source = architecture.get_component(flow.source_component_id)
    target = architecture.get_component(flow.target_component_id)

    if source.zone_id == internet_zone.id:
        target_zone = architecture.get_zone(target.zone_id)
        if target_zone.trust_level in [TrustLevel.MEDIUM, TrustLevel.HIGH]:
            yield Finding(
                rule_id="SEC-003",
                severity=Severity.CRITICAL,
                title=f"Direct Internet access to {target.name} in internal zone",
                description=f"Flow from Internet directly to {target_zone.name} zone bypasses DMZ",
                impact="Exposure of internal resources without perimeter defense",
                affected_flow_id=flow.id
            )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Introduce DMZ zone with reverse proxy or API gateway
  - Restrict direct access from Internet to internal zones
  - Implement WAF/IDS in DMZ
- Effort: High
- Security Gain: High

---

#### SEC-004 : No Bastion for Administration

**Description** : Administration de composants critiques sans bastion host.

**Rationale** : L'accès administratif doit passer par un bastion sécurisé et auditable.

**Logique** :
```python
# Vérifier s'il existe un bastion
bastions = [c for c in architecture.components if c.component_type == ComponentType.BASTION]

if not bastions:
    # Vérifier s'il y a des composants avec admin interface
    admin_components = [c for c in architecture.components if c.has_admin_interface]

    if admin_components:
        yield Finding(
            rule_id="SEC-004",
            severity=Severity.HIGH,
            title="No bastion host for administrative access",
            description=f"{len(admin_components)} components with admin interfaces but no bastion in architecture",
            impact="Difficult to audit and control administrative access",
            affected_component_id=admin_components[0].id
        )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Deploy dedicated bastion host in management zone
  - Configure all admin access through bastion
  - Enable session recording and audit logging
  - Implement MFA on bastion access
- Effort: Medium
- Security Gain: High

---

#### SEC-005 : Uncontrolled Inter-Zone Flow

**Description** : Flux entre zones de confiance différentes sans contrôle explicite.

**Rationale** : Tout flux traversant des frontières de zones doit être contrôlé (firewall, ACL).

**Logique** :
```python
for flow in architecture.flows:
    source = architecture.get_component(flow.source_component_id)
    target = architecture.get_component(flow.target_component_id)

    if source.zone_id != target.zone_id:
        # Flux inter-zones
        # Vérifier s'il y a un firewall sur le chemin
        has_firewall_control = False

        # Dans MVP : simple heuristique
        # Post-MVP : analyse de graphe pour détecter firewall intermédiaire
        if source.component_type == ComponentType.FIREWALL or target.component_type == ComponentType.FIREWALL:
            has_firewall_control = True

        if not has_firewall_control:
            yield Finding(
                rule_id="SEC-005",
                severity=Severity.MEDIUM,
                title=f"Uncontrolled flow between {source.name} and {target.name}",
                description="Inter-zone flow without explicit firewall control",
                impact="Lateral movement risk if one zone is compromised",
                affected_flow_id=flow.id
            )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Deploy firewall or network ACL between zones
  - Implement micro-segmentation
  - Apply least privilege on network rules
- Effort: Medium
- Security Gain: Medium

---

### Catégorie : Network & Segmentation

#### SEC-006 : Management Zone Accessible from Internet

**Description** : Zone de management (control plane) accessible depuis Internet.

**Rationale** : Le plan de management doit être isolé et jamais exposé directement.

**Logique** :
```python
management_zones = [z for z in architecture.zones if "management" in z.name.lower() or "admin" in z.name.lower()]

internet_zone = next((z for z in architecture.zones if z.trust_level == TrustLevel.UNTRUSTED), None)

if internet_zone:
    for mgmt_zone in management_zones:
        # Chercher des flux depuis Internet vers cette zone
        for flow in architecture.flows:
            source = architecture.get_component(flow.source_component_id)
            target = architecture.get_component(flow.target_component_id)

            if source.zone_id == internet_zone.id and target.zone_id == mgmt_zone.id:
                yield Finding(
                    rule_id="SEC-006",
                    severity=Severity.CRITICAL,
                    title="Management zone accessible from Internet",
                    description=f"Direct access from Internet to management zone {mgmt_zone.name}",
                    impact="Administrative plane compromise risk",
                    affected_flow_id=flow.id
                )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Isolate management zone completely from Internet
  - Use VPN or dedicated admin network
  - Implement jump server/bastion
- Effort: High
- Security Gain: High

---

#### SEC-007 : Unencrypted Flow Between Different Trust Zones

**Description** : Flux non chiffré entre zones de confiance différentes.

**Rationale** : Les données traversant des frontières de zones doivent être chiffrées.

**Logique** :
```python
for flow in architecture.flows:
    source = architecture.get_component(flow.source_component_id)
    target = architecture.get_component(flow.target_component_id)

    source_zone = architecture.get_zone(source.zone_id)
    target_zone = architecture.get_zone(target.zone_id)

    if source_zone.id != target_zone.id and not flow.is_encrypted:
        # Calculer la différence de trust level
        trust_diff = abs(
            ["untrusted", "low", "medium", "high"].index(source_zone.trust_level) -
            ["untrusted", "low", "medium", "high"].index(target_zone.trust_level)
        )

        if trust_diff >= 2:
            severity = Severity.HIGH
        else:
            severity = Severity.MEDIUM

        yield Finding(
            rule_id="SEC-007",
            severity=severity,
            title=f"Unencrypted flow between {source_zone.name} and {target_zone.name}",
            description=f"Flow from {source.name} to {target.name} crosses trust boundaries without encryption",
            impact="Data exposure risk during transit",
            affected_flow_id=flow.id
        )
```

**Recommendation** :
- Domain: Data
- Actions:
  - Enable TLS/SSL on all inter-zone communications
  - Use VPN tunnels for site-to-site connections
  - Implement mutual TLS where applicable
- Effort: Low to Medium
- Security Gain: High

---

#### SEC-008 : No Segmentation Between Critical Components

**Description** : Composants critiques dans la même zone sans segmentation.

**Rationale** : Micro-segmentation pour limiter le blast radius.

**Logique** :
```python
critical_types = [ComponentType.DATABASE, ComponentType.IAM]

for zone in architecture.zones:
    critical_in_zone = [c for c in architecture.components
                        if c.zone_id == zone.id and c.component_type in critical_types]

    if len(critical_in_zone) >= 2:
        # Vérifier s'il y a des flux directs entre eux sans firewall intermédiaire
        for i, comp1 in enumerate(critical_in_zone):
            for comp2 in critical_in_zone[i+1:]:
                flows = [f for f in architecture.flows
                        if (f.source_component_id == comp1.id and f.target_component_id == comp2.id) or
                           (f.source_component_id == comp2.id and f.target_component_id == comp1.id)]

                if flows:
                    yield Finding(
                        rule_id="SEC-008",
                        severity=Severity.MEDIUM,
                        title=f"No segmentation between {comp1.name} and {comp2.name}",
                        description="Critical components in same zone without micro-segmentation",
                        impact="Lateral movement risk between critical assets",
                        affected_component_id=comp1.id
                    )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Implement micro-segmentation using security groups or host firewalls
  - Apply principle of least privilege on network rules
  - Consider separate subnets for different component types
- Effort: Medium
- Security Gain: Medium

---

#### SEC-009 : Internet-Exposed Component Without Firewall

**Description** : Composant exposé à Internet sans firewall devant.

**Rationale** : Toute exposition Internet doit être protégée par un firewall ou WAF.

**Logique** :
```python
internet_zone = next((z for z in architecture.zones if z.trust_level == TrustLevel.UNTRUSTED), None)

if internet_zone:
    for flow in architecture.flows:
        if architecture.get_component(flow.source_component_id).zone_id == internet_zone.id:
            target = architecture.get_component(flow.target_component_id)

            # Vérifier s'il y a un firewall dans la zone cible ou entre les zones
            zone_has_firewall = any(
                c.component_type == ComponentType.FIREWALL
                for c in architecture.components
                if c.zone_id == target.zone_id
            )

            if not zone_has_firewall and target.component_type != ComponentType.FIREWALL:
                yield Finding(
                    rule_id="SEC-009",
                    severity=Severity.HIGH,
                    title=f"Internet-exposed {target.name} without firewall protection",
                    description="Component accessible from Internet without firewall",
                    impact="Direct exposure to Internet-based attacks",
                    affected_component_id=target.id
                )
```

**Recommendation** :
- Domain: Network
- Actions:
  - Deploy WAF or network firewall in front of exposed components
  - Implement rate limiting and DDoS protection
  - Use CDN with security features
- Effort: Medium
- Security Gain: High

---

#### SEC-010 : Bidirectional Flow Without Justification

**Description** : Flux bidirectionnel détecté (peut indiquer un problème d'architecture).

**Rationale** : Les flux devraient être unidirectionnels dans une architecture bien segmentée.

**Logique** :
```python
flow_pairs = {}

for flow in architecture.flows:
    key = tuple(sorted([flow.source_component_id, flow.target_component_id]))
    if key not in flow_pairs:
        flow_pairs[key] = []
    flow_pairs[key].append(flow)

for (comp1_id, comp2_id), flows in flow_pairs.items():
    if len(flows) >= 2:
        # Flux bidirectionnel détecté
        comp1 = architecture.get_component(comp1_id)
        comp2 = architecture.get_component(comp2_id)

        yield Finding(
            rule_id="SEC-010",
            severity=Severity.LOW,
            title=f"Bidirectional flow between {comp1.name} and {comp2.name}",
            description="Two-way communication pattern detected",
            impact="May indicate architectural complexity or unnecessary exposure",
            affected_flow_id=flows[0].id
        )
```

**Recommendation** :
- Domain: Architecture
- Actions:
  - Review if bidirectional flow is necessary
  - Consider unidirectional patterns (e.g., message queues)
  - Simplify communication patterns
- Effort: Low
- Security Gain: Low

---

### Catégorie : Data Protection

#### SEC-011 : Database Without Encryption at Rest

**Description** : Base de données sans chiffrement au repos.

**Rationale** : Protection des données sensibles en cas de compromission physique ou backup volé.

**Logique** :
```python
for component in architecture.components:
    if component.component_type == ComponentType.DATABASE:
        if not component.encryption_at_rest:
            yield Finding(
                rule_id="SEC-011",
                severity=Severity.HIGH,
                title=f"Database {component.name} without encryption at rest",
                description="Database does not have encryption at rest enabled",
                impact="Data exposure risk if storage is compromised",
                affected_component_id=component.id
            )
```

**Recommendation** :
- Domain: Data
- Actions:
  - Enable transparent data encryption (TDE) on database
  - Use cloud provider encryption services (AWS KMS, Azure Key Vault)
  - Implement key rotation policy
- Effort: Low
- Security Gain: High

---

#### SEC-012 : Sensitive Data Flow Without Encryption

**Description** : Flux contenant des données sensibles non chiffré (détection heuristique).

**Rationale** : Les données sensibles doivent être protégées en transit.

**Logique** :
```python
sensitive_protocols = [FlowProtocol.SQL, FlowProtocol.LDAP]

for flow in architecture.flows:
    if flow.protocol in sensitive_protocols and not flow.is_encrypted:
        source = architecture.get_component(flow.source_component_id)
        target = architecture.get_component(flow.target_component_id)

        yield Finding(
            rule_id="SEC-012",
            severity=Severity.HIGH,
            title=f"Unencrypted {flow.protocol} flow between {source.name} and {target.name}",
            description="Potentially sensitive data transmitted without encryption",
            impact="Credential or data interception risk",
            affected_flow_id=flow.id
        )
```

**Recommendation** :
- Domain: Data
- Actions:
  - Enable TLS/SSL on database connections
  - Use LDAPS instead of LDAP
  - Configure certificate validation
- Effort: Low
- Security Gain: High

---

#### SEC-013 : No TLS on Exposed API

**Description** : API exposée sans TLS.

**Rationale** : Toute API exposée doit utiliser HTTPS.

**Logique** :
```python
internet_zone = next((z for z in architecture.zones if z.trust_level == TrustLevel.UNTRUSTED), None)

if internet_zone:
    for flow in architecture.flows:
        source = architecture.get_component(flow.source_component_id)
        target = architecture.get_component(flow.target_component_id)

        if source.zone_id == internet_zone.id:
            if target.component_type == ComponentType.API_GATEWAY:
                if flow.protocol == FlowProtocol.HTTP:
                    yield Finding(
                        rule_id="SEC-013",
                        severity=Severity.CRITICAL,
                        title=f"API {target.name} exposed over HTTP",
                        description="API accessible from Internet without TLS encryption",
                        impact="Man-in-the-middle attacks, credential theft",
                        affected_flow_id=flow.id
                    )
```

**Recommendation** :
- Domain: Data
- Actions:
  - Enable HTTPS on all API endpoints
  - Disable HTTP or redirect to HTTPS
  - Implement HSTS headers
  - Use valid TLS certificates
- Effort: Low
- Security Gain: High

---

### Catégorie : Observability & Logging

#### SEC-014 : Critical Component Without Logging

**Description** : Composant critique sans logging activé.

**Rationale** : Observabilité essentielle pour détection d'incidents et forensics.

**Logique** :
```python
critical_types = [
    ComponentType.DATABASE,
    ComponentType.IAM,
    ComponentType.API_GATEWAY,
    ComponentType.FIREWALL
]

for component in architecture.components:
    if component.component_type in critical_types or component.has_admin_interface:
        if not component.has_logging:
            yield Finding(
                rule_id="SEC-014",
                severity=Severity.MEDIUM,
                title=f"No logging enabled on {component.name}",
                description="Critical component without audit logging",
                impact="Blind spot for security monitoring and incident response",
                affected_component_id=component.id
            )
```

**Recommendation** :
- Domain: Observability
- Actions:
  - Enable comprehensive audit logging
  - Log authentication, authorization, and administrative actions
  - Configure log retention policy
- Effort: Low
- Security Gain: Medium

---

#### SEC-015 : No Centralized Logging

**Description** : Absence de centralisation des logs.

**Rationale** : Logs centralisés permettent corrélation et détection d'attaques distribuées.

**Logique** :
```python
# Rechercher un composant de type logging/SIEM (heuristique simple pour MVP)
logging_components = [c for c in architecture.components
                     if "siem" in c.name.lower() or
                        "log" in c.name.lower() or
                        "splunk" in c.name.lower() or
                        "elk" in c.name.lower()]

components_with_logging = [c for c in architecture.components if c.has_logging]

if components_with_logging and not logging_components:
    yield Finding(
        rule_id="SEC-015",
        severity=Severity.MEDIUM,
        title="No centralized logging solution detected",
        description=f"{len(components_with_logging)} components have logging but no central collector",
        impact="Difficult correlation and security monitoring",
        affected_component_id=components_with_logging[0].id
    )
```

**Recommendation** :
- Domain: Observability
- Actions:
  - Deploy SIEM or centralized logging platform (ELK, Splunk, etc.)
  - Configure log forwarding from all components
  - Implement log retention and backup
  - Set up alerting rules
- Effort: High
- Security Gain: Medium

---

## Extensibilité

### Ajouter une Nouvelle Règle

1. Créer un fichier dans `backend/core/rules/`
2. Implémenter la classe héritant de `Rule`
3. Ajouter dans le registry `backend/core/rule_engine.py`

Exemple :

```python
# backend/core/rules/sec_016_privilege_escalation.py

from backend.core.models import Rule, Finding, Architecture, Severity, RuleCategory

class PrivilegeEscalationRiskRule(Rule):
    def __init__(self):
        super().__init__(
            id="SEC-016",
            name="Privilege Escalation Risk",
            description="Detect components where privilege escalation is possible",
            category=RuleCategory.IDENTITY,
            severity=Severity.HIGH,
            rationale="Prevent lateral privilege escalation"
        )

    def evaluate(self, architecture: Architecture) -> list[Finding]:
        findings = []
        # Implementation logic here
        return findings

    def generate_recommendation(self, finding: Finding) -> Recommendation:
        return Recommendation(
            domain=RecommendationDomain.IDENTITY,
            description="Implement least privilege access",
            actions=[
                "Review and restrict permissions",
                "Implement RBAC",
                "Regular privilege audits"
            ],
            priority=RecommendationPriority.HIGH,
            effort=EffortLevel.MEDIUM,
            security_gain=SecurityGain.HIGH
        )
```

### Règles Paramétrables

Pour une règle ajustable :

```python
class ConfigurableRule(Rule):
    def __init__(self, threshold: int = 5):
        self.threshold = threshold
        super().__init__(...)

    def evaluate(self, architecture: Architecture) -> list[Finding]:
        if some_count > self.threshold:
            # Generate finding
            pass
```

## Priorisation des Règles

Dans le moteur d'analyse, l'ordre d'exécution peut être optimisé :

1. Règles critiques d'abord (CRITICAL severity)
2. Règles à faible coût computationnel
3. Règles à forte valeur ajoutée

## Tests Unitaires des Règles

Chaque règle doit avoir des tests :

```python
def test_sec_001_detects_admin_without_mfa():
    architecture = create_test_architecture(
        components=[
            Component(name="API", has_admin_interface=True, requires_mfa=False)
        ]
    )

    rule = AdminAccessWithoutMFARule()
    findings = rule.evaluate(architecture)

    assert len(findings) == 1
    assert findings[0].severity == Severity.HIGH
```

## Post-MVP : Règles Avancées

Futures règles à implémenter :
- Analyse de graphe pour détecter les chemins d'attaque
- Détection de patterns d'architecture à risque
- Scoring de conformité (NIST, ISO 27001)
- Règles contextuelles (cloud provider specific)
- Machine learning pour détection d'anomalies architecturales
