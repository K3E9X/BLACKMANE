# BLACKMANE - Guide de Démarrage Rapide macOS M1/M2/M3

## Installation en 2 Minutes

### Étape 1 : Cloner le Projet

```bash
cd ~/Projects  # ou votre répertoire de projets
git clone <url-du-repo> BLACKMANE
cd BLACKMANE
```

### Étape 2 : Installation Automatique

```bash
./scripts/setup-macos.sh
```

Ce script va installer automatiquement :
- Python 3.11 (via Homebrew si nécessaire)
- Node.js 18+ (via Homebrew si nécessaire)
- Toutes les dépendances backend (environnement virtuel ARM64 natif)
- Toutes les dépendances frontend

**Durée** : 3-5 minutes selon votre connexion

### Étape 3 : Lancer BLACKMANE

```bash
./scripts/start-macos.sh
```

Le terminal affichera :
```
==========================================
  BLACKMANE is running!
==========================================

Frontend:  http://localhost:5173
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/api/docs
```

### Étape 4 : Accéder à l'Application

Ouvrez votre navigateur :
- **Application** : http://localhost:5173
- **Documentation API** : http://localhost:8000/api/docs

**Arrêter l'application** : Appuyez sur `Ctrl+C` dans le terminal

## Vérification

Si tout fonctionne correctement, vous devriez voir :
1. Page d'accueil BLACKMANE (dark theme)
2. Message "Application en cours de développement..."
3. API Health check à http://localhost:8000/health

## Problèmes Courants

### "Homebrew not found"

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
source ~/.zshrc
```

### "Port 8000 already in use"

```bash
# Tuer le processus utilisant le port
kill -9 $(lsof -ti:8000)
```

### "xcrun: error: invalid active developer path"

```bash
xcode-select --install
```

## Scripts Utiles

```bash
# Nettoyage
./scripts/clean-macos.sh

# Sauvegarde de la base de données
./scripts/backup-db.sh

# Réinstallation complète
./scripts/clean-macos.sh
./scripts/setup-macos.sh
```

## Développement avec VS Code

Si vous utilisez VS Code sur votre Mac :

```bash
# Installer VS Code (si pas déjà fait)
brew install --cask visual-studio-code

# Ouvrir le projet
code .
```

VS Code va automatiquement :
- Détecter l'environnement Python
- Proposer d'installer les extensions recommandées
- Configurer le formatage automatique

**Extensions recommandées** (auto-suggérées) :
- Python
- Pylance
- Ruff
- ESLint
- Prettier
- Tailwind CSS IntelliSense

## Architecture Détectée

Vérifier que tout est en ARM64 natif :

```bash
# Vérifier Python
cd backend
source venv/bin/activate
python -c "import platform; print(f'Python: {platform.machine()}')"
# Devrait afficher : arm64

# Vérifier Node
node -p "process.arch"
# Devrait afficher : arm64
```

## Performances sur Apple Silicon

BLACKMANE est optimisé pour M1/M2/M3 :
- **Backend** : Python ARM64 natif via Homebrew
- **SQLite** : Compilé pour ARM64
- **Frontend** : Node.js ARM64 natif
- **Pas d'émulation Rosetta 2**

Temps de démarrage typiques sur M1 :
- Backend : < 2 secondes
- Frontend : < 3 secondes
- Total : < 5 secondes

## Prochaines Étapes

1. **Explorer la Documentation** :
   - [Architecture Complète](docs/ARCHITECTURE.md)
   - [Guide macOS Détaillé](docs/MACOS_M1.md)
   - [Plan MVP](docs/MVP.md)

2. **Commencer le Développement** :
   - Consulter [GETTING_STARTED.md](GETTING_STARTED.md)
   - Suivre la roadmap dans [docs/ROADMAP.md](docs/ROADMAP.md)

3. **Tester l'API** :
   - Ouvrir http://localhost:8000/api/docs
   - Explorer les endpoints disponibles
   - Tester les requêtes

## Support

Pour des informations détaillées sur macOS M1/M2/M3 :
- Documentation complète : [docs/MACOS_M1.md](docs/MACOS_M1.md)
- Problèmes courants et solutions
- Optimisations spécifiques
- Intégration avec macOS

---

**BLACKMANE fonctionne nativement sur Apple Silicon !**

Démarrage < 5 secondes · Aucune émulation · Performance optimale
