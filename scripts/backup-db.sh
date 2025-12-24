#!/bin/bash

# BLACKMANE - Database Backup Script
# Creates timestamped backups of the SQLite database

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}BLACKMANE - Database Backup${NC}"
echo "============================"
echo ""

# Database path
DB_PATH="backend/blackmane.db"

# Check if database exists
if [ ! -f "$DB_PATH" ]; then
    echo -e "${RED}Database not found: $DB_PATH${NC}"
    echo "No database to backup."
    exit 1
fi

# Create backup directory
BACKUP_DIR="$HOME/Library/Application Support/BLACKMANE/backups"
mkdir -p "$BACKUP_DIR"

# Generate timestamp
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Backup filename
BACKUP_FILE="$BACKUP_DIR/blackmane_backup_$TIMESTAMP.db"

# Create backup
echo "Backing up database..."
echo "Source: $DB_PATH"
echo "Destination: $BACKUP_FILE"
echo ""

# Use SQLite .backup command for safe backup (even if DB is in use)
if command -v sqlite3 &> /dev/null; then
    sqlite3 "$DB_PATH" ".backup '$BACKUP_FILE'"
else
    # Fallback to simple copy if sqlite3 not available
    cp "$DB_PATH" "$BACKUP_FILE"
fi

# Set permissions
chmod 600 "$BACKUP_FILE"

# Check backup size
ORIGINAL_SIZE=$(stat -f%z "$DB_PATH")
BACKUP_SIZE=$(stat -f%z "$BACKUP_FILE")

echo -e "${GREEN}✓ Backup created successfully!${NC}"
echo ""
echo "Original size: $(numfmt --to=iec $ORIGINAL_SIZE 2>/dev/null || echo $ORIGINAL_SIZE bytes)"
echo "Backup size:   $(numfmt --to=iec $BACKUP_SIZE 2>/dev/null || echo $BACKUP_SIZE bytes)"
echo ""
echo "Backup location: $BACKUP_FILE"

# List all backups
echo ""
echo "All backups:"
echo "------------"
ls -lh "$BACKUP_DIR" | grep "blackmane_backup" | awk '{print $9, "-", $5}'

# Cleanup old backups (keep last 10)
echo ""
BACKUP_COUNT=$(ls -1 "$BACKUP_DIR"/blackmane_backup_*.db 2>/dev/null | wc -l | tr -d ' ')

if [ "$BACKUP_COUNT" -gt 10 ]; then
    echo "Cleaning up old backups (keeping last 10)..."
    ls -t "$BACKUP_DIR"/blackmane_backup_*.db | tail -n +11 | xargs rm -f
    echo -e "${GREEN}✓ Old backups cleaned${NC}"
fi

echo ""
echo "To restore a backup:"
echo "1. Stop BLACKMANE: pkill -f 'python main.py'"
echo "2. Replace: cp '$BACKUP_FILE' backend/blackmane.db"
echo "3. Restart BLACKMANE: ./scripts/start-macos.sh"
echo ""
