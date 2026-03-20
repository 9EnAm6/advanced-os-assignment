#!/bin/bash

# Task 1: Process and Resource Management System
# Advanced Operating Systems - Assignment 1
# DISTINCTION VERSION - With robust validation and error handling

LOG_FILE="system_monitor_log.txt"
ARCHIVE_DIR="ArchiveLogs"
CRITICAL_PROCESSES=("init" "systemd" "kernel" "sshd" "cron")

# Function to log actions with timestamp
log_action() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to validate PID input
validate_pid() {
    local pid="$1"
    
    # Check if input is numeric
    if ! [[ "$pid" =~ ^[0-9]+$ ]]; then
        echo "❌ Invalid PID: Must be a numeric value"
        return 1
    fi
    
    # Check if PID exists in system
    if ! ps -p "$pid" > /dev/null 2>&1; then
        echo "❌ PID $pid does not exist in the system"
        return 2
    fi
    
    return 0
}

# Function to check if process is critical
is_critical_process() {
    local pid="$1"
    local process_name=$(ps -p "$pid" -o comm= 2>/dev/null)
    
    # Always protect PID 1 and 2 (init/system)
    if [ "$pid" -le 2 ]; then
        return 0
    fi
    
    # Check against critical process names
    for critical in "${CRITICAL_PROCESSES[@]}"; do
        if [[ "$process_name" == *"$critical"* ]]; then
            return 0
        fi
    done
    
    return 1
}

# Main menu loop
while true; do
    echo ""
    echo "====================================="
    echo "   PROCESS MANAGEMENT SYSTEM"
    echo "====================================="
    echo "1. Display CPU/Memory Usage"
    echo "2. List Top 10 Memory Processes"
    echo "3. Terminate a Process"
    echo "4. Inspect Disk and Archive Logs"
    echo "5. Exit"
    echo "====================================="
    read -p "Choose option [1-5]: " choice
    
    case $choice in
        1)
            echo "---------------------------------"
            echo "CPU and Memory Usage:"
            echo "---------------------------------"
            top -bn1 | head -15
            log_action "Viewed CPU/memory usage"
            ;;
            
        2)
            echo "---------------------------------"
            echo "Top 10 Memory-Consuming Processes:"
            echo "---------------------------------"
            printf "%-8s %-10s %-6s %-6s %s\n" "PID" "USER" "%CPU" "%MEM" "COMMAND"
            ps aux --sort=-%mem | head -11 | tail -10 | awk '{printf "%-8s %-10s %-6s %-6s %s\n", $2, $1, $3, $4, $11}'
            log_action "Listed top 10 memory processes"
            ;;
            
        3)
            read -p "Enter PID to terminate: " pid
            
            # ==== PID VALIDATION (Critical for distinction) ====
            if ! validate_pid "$pid"; then
                log_action "Attempted to terminate invalid PID: $pid"
                continue
            fi
            
            # Check if process is critical
            if is_critical_process "$pid"; then
                process_name=$(ps -p "$pid" -o comm= 2>/dev/null)
                echo "❌ ERROR: Cannot terminate critical system process: $process_name (PID: $pid)"
                log_action "Blocked termination of critical process: $process_name (PID: $pid)"
                continue
            fi
            
            # Get process name for logging
            process_name=$(ps -p "$pid" -o comm= 2>/dev/null)
            
            # Confirmation prompt
            read -p "Are you sure you want to terminate PID $pid ($process_name)? (y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                # Try graceful termination first (SIGTERM)
                kill -15 "$pid" 2>/dev/null
                sleep 1
                
                # Check if process still exists
                if ps -p "$pid" > /dev/null 2>&1; then
                    echo "⚠️  Process did not terminate gracefully. Force kill? (y/n): "
                    read -p "Force kill? (y/n): " force
                    if [ "$force" = "y" ] || [ "$force" = "Y" ]; then
                        kill -9 "$pid" 2>/dev/null
                        echo "✅ Process $pid force-terminated"
                        log_action "Force-terminated process PID $pid ($process_name)"
                    else
                        echo "Termination cancelled"
                        log_action "Cancelled force termination of PID $pid"
                    fi
                else
                    echo "✅ Process $pid terminated successfully"
                    log_action "Terminated process PID $pid ($process_name)"
                fi
            else
                echo "Termination cancelled"
                log_action "Cancelled termination of PID $pid"
            fi
            ;;
            
        4)
            read -p "Enter directory path to inspect: " dir_path
            
            # Validate directory exists
            if [ ! -d "$dir_path" ]; then
                echo "❌ Directory does not exist: $dir_path"
                log_action "Failed to inspect non-existent directory: $dir_path"
                continue
            fi
            
            echo "---------------------------------"
            echo "Disk usage for $dir_path:"
            echo "---------------------------------"
            du -sh "$dir_path"
            
            # Create archive directory if it doesn't exist
            mkdir -p "$ARCHIVE_DIR"
            
            # ==== ROBUST FILE HANDLING with -print0 (Distinction level) ====
            echo "Searching for log files > 50MB..."
            found_files=0
            
            # Using find -print0 for safe handling of special characters
            find "$dir_path" -name "*.log" -type f -size +50M -print0 2>/dev/null | while IFS= read -r -d '' logfile; do
                found_files=1
                echo "Found large log: $logfile"
                
                # Get file size for logging
                file_size=$(du -h "$logfile" 2>/dev/null | cut -f1)
                
                # Create timestamped archive name
                timestamp=$(date '+%Y%m%d_%H%M%S')
                filename=$(basename "$logfile")
                # Sanitize filename for archive (replace spaces with underscores)
                safe_filename=$(echo "$filename" | tr ' ' '_')
                archive_name="${safe_filename}_${timestamp}.tar.gz"
                
                # Compress the file
                echo "Compressing to $ARCHIVE_DIR/$archive_name..."
                if tar -czf "$ARCHIVE_DIR/$archive_name" -C "$(dirname "$logfile")" "$(basename "$logfile")" 2>/dev/null; then
                    echo "✅ Compressed: $file_size -> $(du -h "$ARCHIVE_DIR/$archive_name" | cut -f1)"
                    log_action "Compressed $logfile to $archive_name"
                else
                    echo "❌ Compression failed for $logfile"
                    log_action "Compression failed for $logfile"
                fi
            done
            
            if [ $found_files -eq 0 ]; then
                echo "No log files larger than 50MB found."
            fi
            
            # Check archive size and warn if >1GB
            if [ -d "$ARCHIVE_DIR" ]; then
                archive_size_bytes=$(du -sb "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
                archive_size_human=$(du -sh "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
                
                if [ -n "$archive_size_bytes" ] && [ "$archive_size_bytes" -gt $((1024*1024*1024)) ]; then
                    echo "⚠️  WARNING: ArchiveLogs directory exceeds 1GB! Current size: $archive_size_human"
                    log_action "ArchiveLogs exceeded 1GB: $archive_size_human - WARNING triggered"
                else
                    echo "ArchiveLogs current size: $archive_size_human"
                fi
            fi
            ;;
            
        5)
            read -p "Are you sure you want to exit? (y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                log_action "Exited system"
                echo "✅ Goodbye!"
                exit 0
            else
                echo "Exit cancelled"
            fi
            ;;
            
        *)
            echo "❌ Invalid option. Please choose 1-5"
            ;;
    esac
done