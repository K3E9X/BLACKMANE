# BLACKMANE - Définition MVP

## Objectif MVP

Livrer un outil fonctionnel minimal permettant à un architecte sécurité de :
1. Créer un projet d'architecture
2. Décrire manuellement une architecture simple
3. Lancer une analyse basée sur des règles Zero Trust
4. Obtenir une liste de faiblesses et recommandations
5. Consulter une évaluation de maturité basique

**Durée estimée MVP** : 6-8 semaines (1 développeur senior)

## Périmètre IN

### 1. Gestion de Projets (Semaine 1)

#### Fonctionnalités
- Créer un nouveau projet
- Lister tous les projets
- Voir les détails d'un projet
- Supprimer un projet

#### Données projet
- Nom (obligatoire)
- Type : Cloud / On-premise / Hybride
- Contexte métier (texte libre, optionnel)
- Niveau de criticité : Faible / Moyen / Élevé / Critique
- Date de création

#### Interface
- Page liste des projets (tableau simple)
- Formulaire de création
- Page détail projet avec onglets

### 2. Modélisation d'Architecture - Mode Manuel (Semaine 2-3)

**Mode simplifié pour MVP** : Saisie manuelle uniquement.

L'import d'images/PDF est reporté en post-MVP pour limiter la complexité.

#### Fonctionnalités
- Définir les zones de confiance
- Ajouter des composants
- Définir des flux entre composants
- Spécifier des mécanismes de sécurité

#### Modèle de données simplifié

**Zones** :
- Nom (ex: "Internet", "DMZ", "LAN", "Management")
- Niveau de confiance : Untrusted / Low / Medium / High
- Description (optionnel)

**Composants** :
- Nom (ex: "Firewall-1", "AD-Server", "API-Gateway")
- Type : Firewall / Load Balancer / Server / Database / IAM / Bastion / Autre
- Zone d'appartenance
- Caractéristiques :
  - Expose admin interface (oui/non)
  - Requires MFA (oui/non)
  - Has logging (oui/non)
  - Encryption at rest (oui/non)
  - Encryption in transit (oui/non)

**Flux** :
- Source (composant)
- Destination (composant)
- Protocol (HTTP/HTTPS/SSH/RDP/SQL/Autre)
- Port (optionnel)
- Est authentifié (oui/non)
- Est chiffré (oui/non)
- Description (optionnel)

#### Interface
- Formulaire de saisie structuré par étapes :
  1. Définir les zones
  2. Ajouter les composants
  3. Définir les flux
  4. Réviser le modèle complet

### 3. Moteur d'Analyse - Core Rules (Semaine 3-4)

#### Set de règles MVP (15 règles de base)

**Catégorie Identity & Access (5 règles)**
1. Admin access sans MFA
2. Composant critique sans authentification
3. Accès direct depuis Internet vers zone interne
4. Absence de bastion pour administration
5. Flux inter-zones sans contrôle d'accès explicite

**Catégorie Network & Segmentation (5 règles)**
6. Zone management accessible depuis Internet
7. Flux non chiffré entre zones de confiance différentes
8. Absence de segmentation entre composants critiques
9. Composant exposé à Internet sans firewall
10. Flux bidirectionnel injustifié

**Catégorie Data & Encryption (3 règles)**
11. Base de données sans chiffrement au repos
12. Flux contenant des données sensibles non chiffré
13. Absence de TLS/SSL sur API exposée

**Catégorie Observability & Control (2 règles)**
14. Composant critique sans logging
15. Absence de centralisation des logs

#### Moteur d'analyse
- Exécution séquentielle de toutes les règles
- Génération de findings par règle
- Agrégation des résultats
- Calcul d'un score de criticité global

#### Finding
Chaque finding contient :
- ID unique
- Règle déclenchée
- Composant(s) ou flux concerné(s)
- Description du problème
- Impact sécurité
- Sévérité (Critical / High / Medium / Low)

### 4. Génération de Recommandations (Semaine 4-5)

Pour chaque finding, générer automatiquement une recommandation.

#### Structure recommandation
- Description de la recommandation
- Domaine (Identity / Network / Data / Management)
- Actions concrètes (liste à puces)
- Priorité (Critique / Haute / Moyenne / Basse)
- Effort estimé (Faible / Moyen / Élevé)
- Gain sécurité (Faible / Moyen / Élevé)

#### Exemples de recommandations

**Finding** : "Admin access sans MFA sur AD-Server"
**Recommandation** :
- Description : Activer MFA sur tous les accès administratifs
- Domaine : Identity
- Actions :
  - Déployer une solution MFA (TOTP, FIDO2, etc.)
  - Configurer les policies AD pour exiger MFA
  - Former les administrateurs
- Priorité : Critique
- Effort : Moyen
- Gain : Élevé

#### Priorisation automatique
Formule simple :
```
Score = (Severity * 3 + Security_Gain * 2) / Effort
```

Tri par score décroissant.

### 5. Évaluation de Maturité Basique (Semaine 5)

#### Domaines évalués (5 domaines)
1. **Identity & Access Management**
2. **Network Segmentation**
3. **Data Protection**
4. **Observability & Logging**
5. **Zero Trust Readiness**

#### Échelle de maturité (1-5)
1. Initial (aucune pratique formelle)
2. Basique (quelques éléments en place)
3. Défini (pratiques standardisées)
4. Géré (mesure et contrôle)
5. Optimisé (amélioration continue)

#### Calcul de maturité MVP
Pour chaque domaine :
- Lister les règles associées
- Calculer le % de règles respectées
- Mapper au niveau de maturité :
  - < 20% : Niveau 1
  - 20-40% : Niveau 2
  - 40-60% : Niveau 3
  - 60-80% : Niveau 4
  - > 80% : Niveau 5

#### Affichage
- Tableau récapitulatif par domaine
- Score global de maturité
- Pas de visualisation graphique complexe dans MVP

### 6. Roadmap de Sécurité Basique (Semaine 6)

#### Principe
Générer une roadmap automatique en 3 horizons temporels basée sur les priorités.

**Court terme (0-3 mois)** :
- Recommandations priorité Critique + effort Faible/Moyen
- Maximum 5 recommandations

**Moyen terme (3-6 mois)** :
- Recommandations priorité Haute + effort Moyen/Élevé
- Maximum 8 recommandations

**Long terme (6-12 mois)** :
- Recommandations priorité Moyenne/Basse
- Recommandations structurelles

#### Affichage
- Liste chronologique simple
- Regroupement par horizon
- Export texte brut (copier-coller)

### 7. Interface Utilisateur MVP (Semaine 6-8)

#### Pages principales
1. **Dashboard** : Liste des projets
2. **Projet - Détail** : Onglets (Architecture / Analyse / Recommandations / Maturité / Roadmap)
3. **Architecture - Input** : Formulaire de saisie manuelle
4. **Analyse - Résultats** : Liste des findings
5. **Recommandations** : Liste triée par priorité
6. **Maturité** : Tableau de scores
7. **Roadmap** : Timeline simple

#### Style
- Dark theme obligatoire
- Palette : Noir/Anthracite + 1 couleur accent (bleu froid ou cyan)
- Typographie : Inter ou similaire
- Composants minimaux, pas d'animation
- Responsive basique (desktop only pour MVP)

#### Navigation
```
/                          → Liste projets
/projects/new              → Créer projet
/projects/{id}             → Détail projet (default: Architecture)
/projects/{id}/architecture → Input architecture
/projects/{id}/analysis    → Résultats analyse
/projects/{id}/recommendations → Recommandations
/projects/{id}/maturity    → Maturité
/projects/{id}/roadmap     → Roadmap
```

### 8. Backend API MVP

#### Endpoints requis

**Projets**
```
POST   /api/v1/projects
GET    /api/v1/projects
GET    /api/v1/projects/{id}
DELETE /api/v1/projects/{id}
PUT    /api/v1/projects/{id}
```

**Architecture**
```
POST   /api/v1/projects/{id}/architecture
GET    /api/v1/projects/{id}/architecture
PUT    /api/v1/projects/{id}/architecture
```

**Analyse**
```
POST   /api/v1/projects/{id}/analyze
GET    /api/v1/projects/{id}/analysis/latest
GET    /api/v1/projects/{id}/findings
```

**Recommandations**
```
GET    /api/v1/projects/{id}/recommendations
```

**Maturité**
```
GET    /api/v1/projects/{id}/maturity
```

**Roadmap**
```
GET    /api/v1/projects/{id}/roadmap
```

#### Validation
- Pydantic pour tous les endpoints
- Retours d'erreur structurés (RFC 7807)

### 9. Stockage MVP

**Base SQLite unique** : `blackmane.db`

Tables minimum :
- `projects`
- `architectures` (1-to-1 avec project)
- `zones`
- `components`
- `flows`
- `analyses`
- `findings`
- `recommendations`
- `maturity_assessments`

Pas de chiffrement dans MVP (ajout post-MVP).

## Périmètre OUT (Post-MVP)

### Fonctionnalités reportées
- Import d'images (OCR)
- Import de PDF
- Assistance IA pour extraction de composants
- Visualisation graphique de l'architecture
- Export PDF des rapports
- Historique complet des analyses (MVP : dernière analyse seulement)
- Gestion des utilisateurs / multi-tenancy
- Chiffrement de la base
- Métriques avancées
- Intégration avec outils externes
- Mode collaboratif
- Comparaison d'architectures
- Règles personnalisées (interface)
- Templates d'architectures
- Mode hors ligne strict (MVP nécessite backend actif)

### Limitations MVP assumées
- Interface desktop uniquement (pas de mobile)
- Pas de real-time (polling manuel de l'analyse)
- Pas de concurrence (1 utilisateur local)
- Modélisation manuelle uniquement
- Set de règles fixe (extension via code seulement)

## Critères de Succès MVP

### Critères fonctionnels
1. Un architecte peut créer un projet en < 1 minute
2. Modéliser une architecture simple (10 composants) en < 15 minutes
3. Analyse complète en < 5 secondes
4. Liste de recommandations exploitable immédiatement
5. Roadmap générée automatiquement

### Critères techniques
1. Application démarre en < 3 secondes
2. Aucun crash sur cas d'usage nominal
3. Données persistées correctement
4. Code couvert à > 70% par tests
5. Typing strict (mypy pass)

### Critères de qualité
1. Code lisible et maintenable
2. Architecture extensible (ajout de règles facile)
3. Pas de dettes techniques majeures
4. Documentation technique complète

## Livrables MVP

1. Application fonctionnelle (backend + frontend)
2. Base de données initialisée
3. Set de 15 règles implémentées
4. Documentation utilisateur basique
5. Documentation technique (architecture, API)
6. Tests automatisés
7. Script de lancement

## Post-MVP : Priorités

### Version 1.1 (post-MVP immédiat)
- Import d'images avec OCR
- Visualisation graphique basique de l'architecture
- Export Markdown des rapports

### Version 1.2
- Historique complet des analyses
- Comparaison avant/après
- Templates d'architectures courantes

### Version 2.0
- Interface de création de règles personnalisées
- Chiffrement de la base
- Mode collaboratif (multi-projets)
- Assistance IA optionnelle

## Planning MVP Recommandé

| Semaine | Focus | Livrables |
|---------|-------|-----------|
| S1 | Setup + Projets | Backend API projets, Frontend liste/création, DB schema |
| S2 | Architecture (zones, composants) | Input manual zones + composants |
| S3 | Architecture (flux) + Début analyse | Input flux, Moteur de règles (structure) |
| S4 | Analyse (règles) | 15 règles implémentées, Findings |
| S5 | Recommandations + Maturité | Génération reco, Calcul maturité |
| S6 | Roadmap + UI polish | Roadmap auto, Amélioration UX |
| S7 | Tests + Documentation | Tests complets, Docs utilisateur |
| S8 | Bug fixes + Stabilisation | Corrections, Optimisations |

## Notes Importantes

- **Pas de sur-ingénierie** : Le MVP doit être fonctionnel, pas parfait
- **Validation terrain** : Tester avec 2-3 architectes réels après semaine 6
- **Feedback loop** : Ajuster les règles selon les premiers retours
- **Code quality** : Maintenir la qualité dès le début, pas de dette technique volontaire
