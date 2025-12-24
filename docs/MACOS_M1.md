# BLACKMANE - Installation et Utilisation sur macOS M1

## Compatibilité

BLACKMANE est 100% compatible avec macOS sur processeur Apple Silicon (M1/M2/M3).

Cette documentation couvre l'installation et l'utilisation spécifique sur macOS.

## Prérequis macOS M1

### 1. Homebrew (Gestionnaire de paquets)

Si Homebrew n'est pas installé :

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Après installation, ajouter Homebrew au PATH :

```bash
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zshrc
eval "$(/opt/homebrew/bin/brew shellenv)"
```

### 2. Python 3.11+ (via Homebrew)

```bash
# Installer Python 3.11
brew install python@3.11

# Vérifier la version
python3.11 --version
```

### 3. Node.js 18+ (via Homebrew)

```bash
# Installer Node.js
brew install node

# Vérifier les versions
node --version
npm --version
```

## Installation BLACKMANE sur macOS M1

### Méthode Automatique (Recommandée)

```bash
# Cloner le projet (si pas déjà fait)
cd ~/Projects  # ou votre répertoire de projets
git clone <url-du-repo> BLACKMANE
cd BLACKMANE

# Lancer le script d'installation macOS
chmod +x scripts/setup-macos.sh
./scripts/setup-macos.sh
```

### Méthode Manuelle

#### Étape 1 : Backend

```bash
cd backend

# Créer l'environnement virtuel Python
python3.11 -m venv venv

# Activer l'environnement virtuel
source venv/bin/activate

# Mettre à jour pip
pip install --upgrade pip

# Installer les dépendances
pip install -r requirements.txt

# Vérifier l'installation
python -c "import fastapi; print('FastAPI OK')"
```

#### Étape 2 : Frontend

```bash
cd frontend

# Installer les dépendances npm
npm install

# Vérifier l'installation
npm list react
```

## Lancement sur macOS M1

### Option 1 : Script Automatique

```bash
# Depuis la racine du projet
./scripts/start-macos.sh
```

Le script :
- Active automatiquement l'environnement Python
- Démarre le backend sur http://127.0.0.1:8000
- Démarre le frontend sur http://127.0.0.1:5173
- Ouvre automatiquement le navigateur

### Option 2 : Lancement Manuel

**Terminal 1 - Backend** :
```bash
cd backend
source venv/bin/activate
python main.py
```

**Terminal 2 - Frontend** :
```bash
cd frontend
npm run dev
```

**Accès** :
- Frontend : http://localhost:5173
- Backend API : http://localhost:8000
- API Docs : http://localhost:8000/api/docs

### Option 3 : Utiliser iTerm2 avec tmux (Avancé)

```bash
# Installer tmux
brew install tmux

# Lancer avec tmux
./scripts/start-tmux.sh
```

## Spécificités macOS M1

### 1. Architecture ARM64

Python et toutes les dépendances sont installées en natif ARM64 via Homebrew, garantissant :
- Performances optimales
- Compatibilité totale
- Pas d'émulation Rosetta 2 nécessaire

### 2. Permissions et Sécurité

macOS peut demander des autorisations :

```bash
# Donner les permissions d'exécution aux scripts
chmod +x scripts/*.sh

# Si Gatekeeper bloque un script
xattr -d com.apple.quarantine scripts/*.sh
```

### 3. Chemins Spécifiques macOS

Base de données SQLite :
```bash
# Emplacement par défaut
~/Library/Application Support/BLACKMANE/blackmane.db

# Ou dans le projet (développement)
./backend/blackmane.db
```

Logs :
```bash
~/Library/Logs/BLACKMANE/
```

## Problèmes Courants et Solutions

### Problème 1 : "python3.11: command not found"

**Solution** :
```bash
# Vérifier l'installation Python
brew list python@3.11

# Créer un alias si nécessaire
echo 'alias python3.11=/opt/homebrew/bin/python3.11' >> ~/.zshrc
source ~/.zshrc
```

### Problème 2 : "xcrun: error: invalid active developer path"

Cela signifie que les Command Line Tools Xcode ne sont pas installés.

**Solution** :
```bash
xcode-select --install
```

### Problème 3 : Erreur lors de l'installation des dépendances Python

Certaines bibliothèques nécessitent des compilateurs.

**Solution** :
```bash
# Installer les outils de build
brew install gcc

# Installer avec les flags appropriés
ARCHFLAGS="-arch arm64" pip install -r requirements.txt
```

### Problème 4 : Port déjà utilisé

**Solution** :
```bash
# Trouver le processus utilisant le port 8000
lsof -ti:8000

# Tuer le processus
kill -9 $(lsof -ti:8000)

# Ou utiliser un autre port
# Modifier dans backend/config.py
```

### Problème 5 : Node.js ou npm non trouvé après installation

**Solution** :
```bash
# Recharger le shell
source ~/.zshrc

# Ou ajouter manuellement au PATH
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

## Optimisations macOS M1

### 1. Performances Python

```bash
# Utiliser Python natif ARM64 (via Homebrew)
# Déjà fait si vous avez suivi les instructions ci-dessus

# Vérifier l'architecture
python3.11 -c "import platform; print(platform.machine())"
# Devrait afficher : arm64
```

### 2. Accélération SQLite

SQLite est déjà optimisé pour M1 via Homebrew.

### 3. VS Code sur M1

Si vous utilisez VS Code :

```bash
# Installer VS Code pour Apple Silicon
brew install --cask visual-studio-code

# Extensions recommandées
code --install-extension ms-python.python
code --install-extension ms-python.vscode-pylance
code --install-extension dbaeumer.vscode-eslint
code --install-extension bradlc.vscode-tailwindcss
```

Configuration VS Code (`.vscode/settings.json`) :
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/backend/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": false,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  },
  "tailwindCSS.includeLanguages": {
    "typescript": "javascript",
    "typescriptreact": "javascript"
  }
}
```

## Scripts macOS Utiles

### Nettoyage

```bash
# Nettoyer les fichiers temporaires
./scripts/clean-macos.sh
```

### Sauvegarde Base de Données

```bash
# Sauvegarder la base SQLite
./scripts/backup-db.sh
```

### Mise à Jour des Dépendances

```bash
# Backend
cd backend
source venv/bin/activate
pip list --outdated
pip install --upgrade <package>

# Frontend
cd frontend
npm outdated
npm update
```

## Développement sur macOS

### Hot Reload

Les deux serveurs (backend et frontend) supportent le hot reload :
- Backend : Uvicorn recharge automatiquement sur modification Python
- Frontend : Vite recharge automatiquement sur modification TypeScript/React

### Debugging

**Backend** :
```bash
# Lancer en mode debug
cd backend
source venv/bin/activate
python -m debugpy --listen 5678 main.py
```

**Frontend** :
```bash
# Debug dans le navigateur
# Utiliser Chrome DevTools ou React DevTools
```

## Tests sur macOS

```bash
# Tests backend
cd backend
source venv/bin/activate
pytest
pytest --cov=. --cov-report=html

# Tests frontend
cd frontend
npm test
npm run test:coverage
```

## Intégration avec macOS

### 1. Raccourcis Clavier

Créer des alias dans `~/.zshrc` :

```bash
# Ajouter à ~/.zshrc
alias blackmane-start='cd ~/Projects/BLACKMANE && ./scripts/start-macos.sh'
alias blackmane-stop='pkill -f "python main.py"; pkill -f "vite"'
alias blackmane-logs='tail -f ~/Library/Logs/BLACKMANE/app.log'
```

### 2. Automator (Optionnel)

Créer une application macOS pour lancer BLACKMANE :

1. Ouvrir Automator
2. Créer une Application
3. Ajouter "Exécuter un script Shell"
4. Script :
```bash
#!/bin/bash
cd ~/Projects/BLACKMANE
./scripts/start-macos.sh
```
5. Sauvegarder comme "BLACKMANE.app" dans Applications

### 3. Menu Bar (Optionnel - Future)

Pour la v2.0, envisager une app Electron avec icône dans la barre de menu.

## Monitoring sur macOS

### Activity Monitor

Surveiller les processus BLACKMANE :
- Ouvrir Activity Monitor
- Chercher "python" et "node"
- Vérifier CPU et mémoire

### Console.app

Voir les logs système :
- Ouvrir Console.app
- Filtrer par "BLACKMANE"

## Désinstallation

```bash
# Supprimer l'environnement virtuel
cd backend
rm -rf venv

# Supprimer node_modules
cd frontend
rm -rf node_modules

# Supprimer la base de données (optionnel)
rm backend/blackmane.db

# Supprimer le projet
cd ..
rm -rf BLACKMANE
```

## Checklist Installation macOS M1

- [ ] Homebrew installé et configuré
- [ ] Python 3.11 installé via Homebrew
- [ ] Node.js 18+ installé via Homebrew
- [ ] Command Line Tools Xcode installés
- [ ] Projet cloné
- [ ] Backend : environnement virtuel créé
- [ ] Backend : dépendances installées
- [ ] Frontend : dépendances npm installées
- [ ] Scripts exécutables (chmod +x)
- [ ] Application démarre correctement
- [ ] Frontend accessible sur http://localhost:5173
- [ ] Backend accessible sur http://localhost:8000
- [ ] API Docs accessible sur http://localhost:8000/api/docs

## Support macOS

### Versions Testées

- macOS Ventura 13.x ✅
- macOS Sonoma 14.x ✅
- macOS Sequoia 15.x ✅

### Processeurs Testés

- Apple M1 ✅
- Apple M1 Pro ✅
- Apple M1 Max ✅
- Apple M2 ✅
- Apple M3 ✅

## Ressources

- [Homebrew sur Apple Silicon](https://docs.brew.sh/Installation)
- [Python sur macOS](https://www.python.org/downloads/macos/)
- [Node.js sur macOS](https://nodejs.org/en/download/)
- [VS Code sur Apple Silicon](https://code.visualstudio.com/docs/setup/mac)

---

**BLACKMANE est optimisé pour macOS M1 et fonctionne nativement en ARM64.**

En cas de problème, consulter la section "Problèmes Courants" ci-dessus.
