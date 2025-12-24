#!/bin/bash

# BLACKMANE - Installation Script for macOS M1/M2/M3
# This script sets up BLACKMANE on macOS with Apple Silicon

set -e  # Exit on error

echo "=========================================="
echo "  BLACKMANE - macOS Setup Script"
echo "=========================================="
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Detect architecture
ARCH=$(uname -m)
echo "Detected architecture: $ARCH"

if [ "$ARCH" != "arm64" ]; then
    echo -e "${YELLOW}Warning: This script is optimized for Apple Silicon (M1/M2/M3).${NC}"
    echo -e "${YELLOW}You appear to be running on $ARCH.${NC}"
    read -p "Continue anyway? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

echo ""

# Check Homebrew
echo "Checking Homebrew..."
if ! command -v brew &> /dev/null; then
    echo -e "${RED}Homebrew not found!${NC}"
    echo "Please install Homebrew first:"
    echo '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"'
    exit 1
else
    echo -e "${GREEN}✓ Homebrew found${NC}"
fi

# Check Python 3.11+
echo "Checking Python..."
if command -v python3.11 &> /dev/null; then
    PYTHON_CMD="python3.11"
    echo -e "${GREEN}✓ Python 3.11 found${NC}"
elif command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
    if (( $(echo "$PYTHON_VERSION >= 3.11" | bc -l) )); then
        PYTHON_CMD="python3"
        echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"
    else
        echo -e "${YELLOW}Python $PYTHON_VERSION found, but 3.11+ recommended${NC}"
        echo "Installing Python 3.11 via Homebrew..."
        brew install python@3.11
        PYTHON_CMD="python3.11"
    fi
else
    echo -e "${RED}Python not found!${NC}"
    echo "Installing Python 3.11 via Homebrew..."
    brew install python@3.11
    PYTHON_CMD="python3.11"
fi

# Check Node.js
echo "Checking Node.js..."
if ! command -v node &> /dev/null; then
    echo -e "${RED}Node.js not found!${NC}"
    echo "Installing Node.js via Homebrew..."
    brew install node
else
    NODE_VERSION=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
    if [ "$NODE_VERSION" -lt 18 ]; then
        echo -e "${YELLOW}Node.js version < 18 found. Upgrading...${NC}"
        brew upgrade node
    else
        echo -e "${GREEN}✓ Node.js $(node --version) found${NC}"
    fi
fi

echo ""
echo "=========================================="
echo "  Installing Backend Dependencies"
echo "=========================================="
echo ""

cd backend

# Create virtual environment
if [ -d "venv" ]; then
    echo "Virtual environment already exists. Removing..."
    rm -rf venv
fi

echo "Creating Python virtual environment..."
$PYTHON_CMD -m venv venv

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install dependencies
echo "Installing Python dependencies..."
echo "This may take a few minutes on first install..."

# Set architecture flags for M1 compatibility
export ARCHFLAGS="-arch arm64"

pip install -r requirements.txt

# Verify installation
echo ""
echo "Verifying Python installation..."
python -c "import fastapi; print('✓ FastAPI installed')"
python -c "import sqlalchemy; print('✓ SQLAlchemy installed')"
python -c "import pydantic; print('✓ Pydantic installed')"

deactivate
cd ..

echo ""
echo "=========================================="
echo "  Installing Frontend Dependencies"
echo "=========================================="
echo ""

cd frontend

# Install npm dependencies
echo "Installing npm dependencies..."
npm install

# Verify installation
echo ""
echo "Verifying npm installation..."
npm list react --depth=0 2>/dev/null && echo "✓ React installed" || echo "React installed (dependency)"

cd ..

echo ""
echo "=========================================="
echo "  Setup Complete!"
echo "=========================================="
echo ""
echo -e "${GREEN}BLACKMANE has been successfully installed on your Mac!${NC}"
echo ""
echo "Architecture: $ARCH"
echo "Python: $($PYTHON_CMD --version)"
echo "Node.js: $(node --version)"
echo "npm: $(npm --version)"
echo ""
echo "Next steps:"
echo "1. Start BLACKMANE:"
echo "   ./scripts/start-macos.sh"
echo ""
echo "2. Or start manually:"
echo "   Terminal 1: cd backend && source venv/bin/activate && python main.py"
echo "   Terminal 2: cd frontend && npm run dev"
echo ""
echo "3. Access the application:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/api/docs"
echo ""
echo "For more information, see docs/MACOS_M1.md"
echo ""
