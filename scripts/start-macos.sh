#!/bin/bash

# BLACKMANE - Start Script for macOS M1/M2/M3
# Starts both backend and frontend with proper macOS handling

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}"
echo "=========================================="
echo "  BLACKMANE - Security by Design"
echo "=========================================="
echo -e "${NC}"

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    echo -e "${RED}Backend virtual environment not found!${NC}"
    echo "Please run the setup script first:"
    echo "./scripts/setup-macos.sh"
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    echo -e "${RED}Frontend dependencies not found!${NC}"
    echo "Please run the setup script first:"
    echo "./scripts/setup-macos.sh"
    exit 1
fi

# Function to cleanup on exit
cleanup() {
    echo -e "\n${YELLOW}Stopping BLACKMANE...${NC}"

    # Kill backend if running
    if [ ! -z "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null || true
    fi

    # Kill frontend if running
    if [ ! -z "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null || true
    fi

    # Kill any remaining processes
    pkill -f "python main.py" 2>/dev/null || true
    pkill -f "vite" 2>/dev/null || true

    echo -e "${GREEN}BLACKMANE stopped.${NC}"
    exit 0
}

# Trap SIGINT (Ctrl+C) and SIGTERM
trap cleanup INT TERM

# Check if ports are available
check_port() {
    lsof -ti:$1 >/dev/null 2>&1
}

if check_port 8000; then
    echo -e "${YELLOW}Warning: Port 8000 is already in use${NC}"
    echo "Kill the process? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill -9 $(lsof -ti:8000) 2>/dev/null || true
        sleep 1
    else
        echo "Please free port 8000 and try again"
        exit 1
    fi
fi

if check_port 5173; then
    echo -e "${YELLOW}Warning: Port 5173 is already in use${NC}"
    echo "Kill the process? (y/n)"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        kill -9 $(lsof -ti:5173) 2>/dev/null || true
        sleep 1
    else
        echo "Please free port 5173 and try again"
        exit 1
    fi
fi

# Create log directory
LOG_DIR="$HOME/Library/Logs/BLACKMANE"
mkdir -p "$LOG_DIR"

# Start backend
echo -e "${GREEN}Starting Backend...${NC}"
cd backend
source venv/bin/activate

# Start backend in background with logging
nohup python main.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!
cd ..

echo "Backend PID: $BACKEND_PID"
echo "Backend logs: $LOG_DIR/backend.log"

# Wait for backend to start
echo "Waiting for backend to start..."
sleep 3

# Check if backend is running
if ! ps -p $BACKEND_PID > /dev/null; then
    echo -e "${RED}Backend failed to start!${NC}"
    echo "Check logs: tail -f $LOG_DIR/backend.log"
    exit 1
fi

# Verify backend is responding
if ! curl -s http://127.0.0.1:8000/health > /dev/null; then
    echo -e "${YELLOW}Backend started but not responding yet, waiting...${NC}"
    sleep 2
fi

echo -e "${GREEN}✓ Backend running on http://127.0.0.1:8000${NC}"

# Start frontend
echo -e "${GREEN}Starting Frontend...${NC}"
cd frontend

# Start frontend in background with logging
nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!
cd ..

echo "Frontend PID: $FRONTEND_PID"
echo "Frontend logs: $LOG_DIR/frontend.log"

# Wait for frontend to start
echo "Waiting for frontend to start..."
sleep 5

# Check if frontend is running
if ! ps -p $FRONTEND_PID > /dev/null; then
    echo -e "${RED}Frontend failed to start!${NC}"
    echo "Check logs: tail -f $LOG_DIR/frontend.log"
    cleanup
    exit 1
fi

echo -e "${GREEN}✓ Frontend running on http://127.0.0.1:5173${NC}"

echo ""
echo -e "${BLUE}=========================================="
echo "  BLACKMANE is running!"
echo "==========================================${NC}"
echo ""
echo "Frontend:  ${GREEN}http://localhost:5173${NC}"
echo "Backend:   ${GREEN}http://localhost:8000${NC}"
echo "API Docs:  ${GREEN}http://localhost:8000/api/docs${NC}"
echo ""
echo "Logs directory: $LOG_DIR"
echo ""
echo -e "${YELLOW}Press Ctrl+C to stop all services${NC}"
echo ""

# Open browser (optional - uncomment if desired)
# sleep 2
# open http://localhost:5173

# Show real-time logs
echo "=== Backend Logs ==="
tail -f "$LOG_DIR/backend.log" &
TAIL_PID=$!

# Wait for interrupt
wait
