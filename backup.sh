#!/bin/bash
# backup.sh - Backup utility for Advanced Operating Systems Assignment
# Usage: ./backup.sh [target_directory] [destination_directory]

# Default directories (if not provided)
TARGET_DIR=${1:-"."}  # Current directory if not specified
DEST_DIR=${2:-"./backups"}

# Display info
echo "📁 Target Directory: $TARGET_DIR"
echo "📁 Destination Directory: $DEST_DIR"

# Create timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="assignment_backup_${TIMESTAMP}.tar.gz"

# Get absolute paths
ORIG_DIR=$(pwd)
cd "$DEST_DIR" 2>/dev/null || mkdir -p "$DEST_DIR"
DEST_ABS=$(pwd)
cd "$ORIG_DIR"

# Go to target directory
cd "$TARGET_DIR" || { echo "❌ Target directory not found!"; exit 1; }

# Find files modified in last 24 hours
echo "🔍 Finding files modified in last 24 hours..."
YESTERDAY=$((TIMESTAMP - 86400))  # 24 hours ago in seconds

# List files to backup
FILES_TO_BACKUP=()
for file in $(ls -a); do
    # Skip directories and special files
    [ -f "$file" ] || continue
    [[ "$file" == .* ]] && continue  # Skip hidden files
    
    # Check modification time
    FILE_TIME=$(date -r "$file" +%s 2>/dev/null)
    if [ "$FILE_TIME" -gt "$YESTERDAY" ]; then
        FILES_TO_BACKUP+=("$file")
        echo "   + $file"
    fi
done

# Create backup if files found
if [ ${#FILES_TO_BACKUP[@]} -gt 0 ]; then
    echo "📦 Creating backup: $BACKUP_FILE"
    tar -czf "$ORIG_DIR/$BACKUP_FILE" "${FILES_TO_BACKUP[@]}" 2>/dev/null
    
    # Move to destination
    mv "$ORIG_DIR/$BACKUP_FILE" "$DEST_ABS/"
    echo "✅ Backup saved to: $DEST_ABS/$BACKUP_FILE"
    
    # Display size
    SIZE=$(du -h "$DEST_ABS/$BACKUP_FILE" | cut -f1)
    echo "📊 Backup size: $SIZE"
else
    echo "ℹ️ No files modified in last 24 hours. No backup created."
fi

cd "$ORIG_DIR"

# Clean old backups (keep last 5)
echo "🧹 Cleaning old backups (keeping last 5)..."
cd "$DEST_ABS"
ls -t *.tar.gz 2>/dev/null | tail -n +6 | xargs -r rm
cd "$ORIG_DIR"

echo "✅ Backup process completed!"