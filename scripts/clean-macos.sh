#!/bin/bash

# BLACKMANE - Cleanup Script for macOS
# Removes temporary files, logs, and build artifacts

echo "BLACKMANE - Cleanup Script"
echo "=========================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to ask for confirmation
confirm() {
    read -p "$1 (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        return 0
    else
        return 1
    fi
}

# Stop any running processes
echo "Stopping BLACKMANE processes..."
pkill -f "python main.py" 2>/dev/null || true
pkill -f "vite" 2>/dev/null || true
echo -e "${GREEN}✓ Processes stopped${NC}"

# Clean Python cache
echo ""
echo "Cleaning Python cache files..."
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
find . -type f -name "*.pyo" -delete 2>/dev/null || true
find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✓ Python cache cleaned${NC}"

# Clean pytest cache
echo "Cleaning pytest cache..."
find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".mypy_cache" -exec rm -rf {} + 2>/dev/null || true
find . -type d -name ".coverage" -delete 2>/dev/null || true
find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
echo -e "${GREEN}✓ Test cache cleaned${NC}"

# Clean frontend build
echo "Cleaning frontend build files..."
rm -rf frontend/dist 2>/dev/null || true
rm -rf frontend/.vite 2>/dev/null || true
rm -rf frontend/.turbo 2>/dev/null || true
echo -e "${GREEN}✓ Frontend build cleaned${NC}"

# Clean logs
LOG_DIR="$HOME/Library/Logs/BLACKMANE"
if [ -d "$LOG_DIR" ]; then
    echo ""
    if confirm "Clean logs in $LOG_DIR?"; then
        rm -rf "$LOG_DIR"
        echo -e "${GREEN}✓ Logs cleaned${NC}"
    else
        echo "Logs preserved"
    fi
fi

# Clean database (optional)
echo ""
if [ -f "backend/blackmane.db" ]; then
    if confirm "${YELLOW}WARNING: Delete database backend/blackmane.db? This will delete all your data!${NC}"; then
        rm backend/blackmane.db
        rm backend/blackmane.db-journal 2>/dev/null || true
        echo -e "${GREEN}✓ Database deleted${NC}"
    else
        echo "Database preserved"
    fi
fi

# Clean node_modules (optional - saves space)
echo ""
if [ -d "frontend/node_modules" ]; then
    if confirm "Remove frontend/node_modules? (saves ~500MB, requires npm install to rebuild)"; then
        rm -rf frontend/node_modules
        echo -e "${GREEN}✓ node_modules removed${NC}"
    else
        echo "node_modules preserved"
    fi
fi

# Clean virtual environment (optional)
echo ""
if [ -d "backend/venv" ]; then
    if confirm "Remove backend/venv? (requires running setup-macos.sh again)"; then
        rm -rf backend/venv
        echo -e "${GREEN}✓ Virtual environment removed${NC}"
    else
        echo "Virtual environment preserved"
    fi
fi

# Clean macOS specific files
echo ""
echo "Cleaning macOS system files..."
find . -name ".DS_Store" -delete 2>/dev/null || true
echo -e "${GREEN}✓ .DS_Store files cleaned${NC}"

echo ""
echo "==========================="
echo "Cleanup complete!"
echo "==========================="
echo ""
echo "To rebuild:"
echo "1. Run ./scripts/setup-macos.sh (if venv or node_modules were removed)"
echo "2. Run ./scripts/start-macos.sh"
echo ""
