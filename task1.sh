#!/bin/bash

# Task 1: Process and Resource Management System
# Advanced Operating Systems - Assignment 1

LOG_FILE="system_monitor_log.txt"
ARCHIVE_DIR="ArchiveLogs"
CRITICAL_PROCESSES=("init" "systemd" "kernel")

# Function to log actions
log_action() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
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
            echo "PID   USER     %CPU  %MEM  COMMAND"
            ps aux --sort=-%mem | head -11 | tail -10 | awk '{printf "%-5s %-8s %-5s %-5s %s\n", $2, $1, $3, $4, $11}'
            log_action "Listed top 10 memory processes"
            ;;
            
        3)
            read -p "Enter PID to terminate: " pid
            # Check if process is critical
            process_name=$(ps -p $pid -o comm= 2>/dev/null)
            critical=0
            for critical_p in "${CRITICAL_PROCESSES[@]}"; do
                if [[ "$process_name" == *"$critical_p"* ]] || [ "$pid" -le "2" ]; then
                    critical=1
                    break
                fi
            done
            
            if [ $critical -eq 1 ]; then
                echo "❌ ERROR: Cannot terminate critical system process (PID: $pid)"
                log_action "Attempted to terminate critical process PID $pid - BLOCKED"
            else
                read -p "Are you sure you want to terminate PID $pid? (y/n): " confirm
                if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                    kill -15 "$pid" 2>/dev/null
                    if [ $? -eq 0 ]; then
                        echo "✅ Process $pid terminated successfully"
                        log_action "Terminated process PID $pid"
                    else
                        echo "❌ Failed to terminate process. Check PID or permissions."
                        log_action "Failed to terminate PID $pid"
                    fi
                else
                    echo "Termination cancelled"
                    log_action "Cancelled termination of PID $pid"
                fi
            fi
            ;;
            
        4)
            read -p "Enter directory path to inspect: " dir_path
            if [ ! -d "$dir_path" ]; then
                echo "❌ Directory does not exist!"
                log_action "Failed to inspect non-existent directory $dir_path"
                continue
            fi
            
            echo "---------------------------------"
            echo "Disk usage for $dir_path:"
            echo "---------------------------------"
            du -sh "$dir_path"
            
            # Create archive directory if it doesn't exist
            mkdir -p "$ARCHIVE_DIR"
            
            # Find and compress large log files
            echo "Searching for log files > 50MB..."
            find "$dir_path" -name "*.log" -type f -size +50M 2>/dev/null | while read -r logfile; do
                echo "Found large log: $logfile"
                timestamp=$(date '+%Y%m%d_%H%M%S')
                filename=$(basename "$logfile")
                archive_name="${filename}_${timestamp}.tar.gz"
                
                # Compress the file
                tar -czf "$ARCHIVE_DIR/$archive_name" -C "$(dirname "$logfile")" "$(basename "$logfile")" 2>/dev/null
                if [ $? -eq 0 ]; then
                    echo "✅ Compressed to $ARCHIVE_DIR/$archive_name"
                    log_action "Compressed $logfile to $archive_name"
                fi
            done
            
            # Check archive size
            archive_size=$(du -sb "$ARCHIVE_DIR" 2>/dev/null | cut -f1)
            if [ -n "$archive_size" ] && [ "$archive_size" -gt $((1024*1024*1024)) ]; then
                echo "⚠️  WARNING: ArchiveLogs directory exceeds 1GB!"
                log_action "ArchiveLogs exceeded 1GB - WARNING triggered"
            fi
            ;;
            
        5)
            read -p "Are you sure you want to exit? (y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                log_action "Exited system"
                echo "Goodbye!"
                exit 0
            fi
            ;;
            
        *)
            echo "❌ Invalid option. Please choose 1-5"
            ;;
    esac
done