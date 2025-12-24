# BLACKMANE - Roadmap de Développement

## Stratégie Globale

### Philosophie
- Développement incrémental
- MVP fonctionnel d'abord
- Itérations courtes
- Validation terrain régulière
- Pas de sur-ingénierie

### Approche
1. **MVP Core** (8 semaines) - Outil fonctionnel minimal
2. **MVP+** (4 semaines) - Amélirations critiques
3. **v1.0** (8 semaines) - Version production-ready
4. **v2.0+** (horizon long terme) - Fonctionnalités avancées

---

## Phase 1 : MVP Core (8 semaines)

### Semaine 1 : Fondations

**Backend**
- [ ] Setup projet Python
  - Structure de répertoires
  - Poetry ou pip + requirements.txt
  - Configuration FastAPI
  - Setup SQLAlchemy + SQLite
- [ ] Modèles de données (Pydantic + SQLAlchemy)
  - Project
  - Architecture
  - Zone
  - Component
  - Flow
- [ ] API Projets
  - POST /api/v1/projects
  - GET /api/v1/projects
  - GET /api/v1/projects/{id}
  - DELETE /api/v1/projects/{id}
- [ ] Tests unitaires backend (projets)

**Frontend**
- [ ] Setup projet (React + Vite ou Svelte + Vite)
- [ ] Configuration TypeScript
- [ ] Setup TailwindCSS (dark theme)
- [ ] Composants de base
  - Layout
  - Navigation
  - Button, Input, Card
- [ ] Pages projets
  - Liste des projets
  - Création de projet
  - Détail projet (vide)

**DevOps**
- [ ] Configuration Git
- [ ] Scripts de lancement (start.sh)
- [ ] Documentation README basique

**Livrable S1** : Application lancable, CRUD projets fonctionnel

---

### Semaine 2 : Architecture - Zones & Composants

**Backend**
- [ ] API Architecture
  - POST /api/v1/projects/{id}/architecture
  - GET /api/v1/projects/{id}/architecture
  - PUT /api/v1/projects/{id}/architecture
- [ ] Service ArchitectureService
  - Création architecture
  - Validation cohérence
- [ ] Tests unitaires (zones, composants)

**Frontend**
- [ ] Page input architecture (étape 1 : zones)
  - Formulaire ajout zone
  - Liste zones définies
  - Validation trust level
- [ ] Page input architecture (étape 2 : composants)
  - Formulaire ajout composant
  - Sélection zone
  - Checkboxes propriétés sécurité
- [ ] Composant ArchitectureForm
  - Stepper (zones → composants → flux)

**Livrable S2** : Saisie manuelle zones et composants fonctionnelle

---

### Semaine 3 : Architecture - Flux & Moteur de Règles (Structure)

**Backend**
- [ ] API Flux
  - Ajout flows à l'architecture
  - Validation (source ≠ target)
- [ ] Structure moteur de règles
  - Classe abstraite Rule
  - RuleEngine avec registry
  - Classe Finding
  - Classe Recommendation
- [ ] Implémentation de 3 règles (test)
  - SEC-001 : Admin sans MFA
  - SEC-011 : DB sans chiffrement
  - SEC-013 : API sans TLS
- [ ] Tests unitaires règles

**Frontend**
- [ ] Page input architecture (étape 3 : flux)
  - Formulaire ajout flux
  - Sélection source/destination
  - Propriétés protocole, encryption, auth
- [ ] Révision architecture complète
  - Vue récapitulative
  - Bouton "Lancer l'analyse"

**Livrable S3** : Saisie architecture complète + structure moteur règles

---

### Semaine 4 : Moteur d'Analyse - 15 Règles

**Backend**
- [ ] Implémentation des 15 règles MVP
  - 5 règles Identity
  - 5 règles Network
  - 3 règles Data
  - 2 règles Observability
- [ ] Service AnalysisService
  - Orchestration analyse
  - Exécution séquentielle des règles
  - Agrégation findings
  - Calcul global risk score
- [ ] Modèles Analysis & Finding
- [ ] API Analyse
  - POST /api/v1/projects/{id}/analyze
  - GET /api/v1/projects/{id}/analysis/latest
  - GET /api/v1/projects/{id}/findings
- [ ] Tests unitaires (toutes les règles)

**Frontend**
- [ ] Page Analyse
  - Affichage statut analyse (pending/running/completed)
  - Liste des findings
  - Filtres par sévérité
  - Badge count par criticité

**Livrable S4** : Analyse fonctionnelle avec 15 règles

---

### Semaine 5 : Recommandations & Maturité

**Backend**
- [ ] Service RecommendationService
  - Génération recommandations depuis findings
  - Calcul priority score
  - Priorisation
- [ ] Service MaturityService
  - Évaluation par domaine
  - Calcul maturity level
  - Scoring global
- [ ] API Recommandations & Maturité
  - GET /api/v1/projects/{id}/recommendations
  - GET /api/v1/projects/{id}/maturity
- [ ] Tests unitaires

**Frontend**
- [ ] Page Recommandations
  - Liste triée par priorité
  - Cards avec détails (effort, gain, actions)
  - Filtres par domaine
- [ ] Page Maturité
  - Tableau par domaine
  - Score global
  - Interprétation des niveaux

**Livrable S5** : Recommandations et maturité fonctionnels

---

### Semaine 6 : Roadmap & UI Polish

**Backend**
- [ ] Service RoadmapService
  - Génération roadmap automatique
  - Répartition court/moyen/long terme
- [ ] API Roadmap
  - GET /api/v1/projects/{id}/roadmap
- [ ] Tests unitaires

**Frontend**
- [ ] Page Roadmap
  - Vue par horizon temporel
  - Liste d'items par phase
- [ ] Amélioration UX globale
  - Transitions
  - Loading states
  - Error handling
  - Empty states
- [ ] Dark theme finalisé
  - Couleurs cohérentes
  - Contraste optimal

**Livrable S6** : Application complète fonctionnellement

---

### Semaine 7 : Tests & Documentation

**Backend**
- [ ] Tests d'intégration
  - Scénarios complets end-to-end
  - Test de performance (architecture 50 composants)
- [ ] Couverture de tests > 80%
- [ ] Documentation API (OpenAPI/Swagger)
- [ ] Docstrings sur toutes les fonctions publiques

**Frontend**
- [ ] Tests composants (Vitest)
- [ ] Tests d'intégration (Playwright ou Cypress)
- [ ] Accessibilité basique (clavier, screen reader)

**Documentation**
- [ ] Guide utilisateur
  - Comment créer un projet
  - Comment modéliser une architecture
  - Comment interpréter les résultats
- [ ] Guide développeur
  - Setup environnement
  - Comment ajouter une règle
  - Architecture du code

**Livrable S7** : Application testée et documentée

---

### Semaine 8 : Bug Fixes & Stabilisation

**Focus**
- [ ] Correction des bugs identifiés
- [ ] Optimisation performance
  - Indexation DB
  - Queries optimisées
  - Réduction temps d'analyse
- [ ] Validation avec utilisateurs test (2-3 architectes)
  - Feedback UX
  - Identification pain points
  - Ajustement priorités

**Préparation Release**
- [ ] Script de packaging
- [ ] Instructions d'installation
- [ ] CHANGELOG.md
- [ ] Release notes

**Livrable S8** : MVP Core stable et utilisable

---

## Phase 2 : MVP+ (4 semaines)

### Fonctionnalités Critiques Post-MVP

**Semaine 9-10 : Import d'Images**
- [ ] Backend : OCR avec Tesseract
- [ ] Extraction de texte depuis schémas
- [ ] Assistance IA optionnelle (vision API locale)
- [ ] Validation humaine des composants détectés
- [ ] Frontend : Upload image, preview, validation

**Semaine 11 : Visualisation Graphique**
- [ ] Bibliothèque de visualisation (D3.js, Cytoscape, ou React Flow)
- [ ] Rendu graphique de l'architecture
- [ ] Vue par zones
- [ ] Mise en évidence des findings

**Semaine 12 : Export & Historique**
- [ ] Export Markdown des rapports
- [ ] Historique complet des analyses
- [ ] Comparaison avant/après
- [ ] Tracking de l'amélioration de maturité

---

## Phase 3 : Version 1.0 (8 semaines)

### Objectif : Production-Ready

**Semaines 13-14 : Sécurité Renforcée**
- [ ] Chiffrement de la base (SQLCipher)
- [ ] Audit logging complet
- [ ] Tests de sécurité (OWASP)
- [ ] Hardening configuration

**Semaines 15-16 : Templates & Patterns**
- [ ] Templates d'architectures courantes
  - AWS 3-tier
  - Azure hub-spoke
  - On-prem DMZ classique
  - Kubernetes cluster
- [ ] Bibliothèque de patterns sécurisés

**Semaines 17-18 : Règles Avancées**
- [ ] 10 règles supplémentaires
- [ ] Règles contextuelles (cloud-specific)
- [ ] Analyse de graphe (chemins d'attaque)
- [ ] Scoring NIST/ISO 27001

**Semaines 19-20 : Polish & Release**
- [ ] UI/UX professionnelle finalisée
- [ ] Performance optimisée (< 2s pour analyse 100 composants)
- [ ] Documentation complète
- [ ] Packaging final (binaire ou Electron)
- [ ] Release 1.0

---

## Phase 4 : Version 2.0+ (Long terme)

### Fonctionnalités Avancées

**Extensibilité**
- [ ] Interface de création de règles personnalisées (no-code)
- [ ] Plugin system pour règles externes
- [ ] Support de parsers personnalisés (Terraform, CloudFormation)

**Collaboration**
- [ ] Mode collaboratif (multi-utilisateurs locaux)
- [ ] Partage de projets (export/import)
- [ ] Commentaires et annotations

**Intelligence**
- [ ] Suggestions proactives d'améliorations
- [ ] Détection d'anomalies architecturales
- [ ] Apprentissage des patterns de l'entreprise

**Intégrations**
- [ ] Import depuis outils IaC (Terraform, Pulumi)
- [ ] Export vers outils de threat modeling (STRIDE, PASTA)
- [ ] API pour intégration CI/CD

**Compliance**
- [ ] Frameworks de conformité (NIST CSF, ISO 27001, CIS)
- [ ] Rapports d'audit
- [ ] Mapping avec contrôles réglementaires

---

## Métriques de Succès

### MVP Core
- Application démarre en < 3 secondes
- Analyse d'une architecture (20 composants) en < 3 secondes
- Zéro crash sur cas d'usage nominaux
- 3 utilisateurs test satisfaits

### Version 1.0
- 50+ architectures analysées
- Taux d'adoption dans l'équipe > 80%
- Temps moyen de modélisation < 20 minutes
- Feedback utilisateur > 4/5

### Version 2.0
- 200+ architectures analysées
- Extension à d'autres équipes
- Contribution communauté (règles custom)

---

## Risques & Mitigations

### Risque : Complexité des règles
**Impact** : Règles difficiles à implémenter ou trop de faux positifs
**Mitigation** :
- Commencer par règles simples et éprouvées
- Validation avec architectes réels
- Ajustement itératif des seuils

### Risque : Performance
**Impact** : Analyse trop lente pour grandes architectures
**Mitigation** :
- Limites MVP (50 composants)
- Optimisation progressive
- Analyse incrémentale (post-MVP)

### Risque : Adoption utilisateur
**Impact** : Outil jugé trop complexe ou peu utile
**Mitigation** :
- Implication utilisateurs dès semaine 1
- Feedback régulier
- UX simple et guidée
- Documentation claire

### Risque : Maintenance
**Impact** : Code difficile à maintenir/étendre
**Mitigation** :
- Architecture modulaire
- Tests automatisés
- Documentation continue
- Code review systématique

---

## Priorisation des Features Post-MVP

### Must Have (v1.0)
1. Import d'images
2. Visualisation graphique
3. Export rapports
4. Templates architectures

### Should Have (v1.x)
1. Règles avancées
2. Historique complet
3. Chiffrement DB
4. Règles personnalisables

### Nice to Have (v2.0+)
1. Mode collaboratif
2. Intégrations IaC
3. IA générative pour suggestions
4. Mobile app

---

## Planning Réaliste

### Hypothèses
- 1 développeur senior full-time
- 40h/semaine effectives
- Pas de blocages majeurs

### Timeline
- **MVP Core** : 8 semaines (Février - Mars 2025)
- **MVP+** : 4 semaines (Avril 2025)
- **v1.0** : 8 semaines (Mai - Juin 2025)
- **v2.0** : Q4 2025

### Si équipe de 2 développeurs
- Backend specialist + Frontend specialist
- MVP Core : 5-6 semaines
- v1.0 : Q2 2025

---

## Conclusion

Cette roadmap est :
- **Réaliste** : Basée sur des estimations prudentes
- **Incrémentale** : Chaque phase livre de la valeur
- **Flexible** : Ajustable selon feedback
- **Mesurable** : Objectifs clairs à chaque étape

Le MVP Core en 8 semaines permet de valider rapidement la valeur de l'outil.

Les phases suivantes ajoutent des fonctionnalités selon les retours terrain.

**Principe directeur** : Livrer vite, itérer souvent, améliorer continuellement.
