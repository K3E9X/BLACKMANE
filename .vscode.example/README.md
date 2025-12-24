# Configuration VS Code pour BLACKMANE

Ce répertoire contient des configurations recommandées pour VS Code.

## Installation

Copiez le contenu de ce répertoire dans `.vscode/` :

```bash
cp -r .vscode.example .vscode
```

Ou manuellement :

```bash
mkdir -p .vscode
cp .vscode.example/settings.json .vscode/
cp .vscode.example/extensions.json .vscode/
cp .vscode.example/launch.json .vscode/
```

## Fichiers

- `settings.json` - Configuration VS Code (formatage, linting, Python, TypeScript)
- `extensions.json` - Extensions recommandées (auto-suggérées par VS Code)
- `launch.json` - Configurations de debugging

## Extensions Recommandées

Au premier lancement, VS Code proposera d'installer :
- Python
- Pylance
- Black Formatter
- Ruff
- ESLint
- Prettier
- Tailwind CSS IntelliSense

## Debugging

Utilisez `F5` ou le panneau Debug pour :
- Lancer le backend FastAPI en mode debug
- Debugger un fichier Python
- Lancer pytest sur le fichier courant
