#!/bin/bash

# Task 3: Secure Examination Submission System
# Advanced Operating Systems - Assignment 1
# DISTINCTION VERSION - With security awareness and limitations documented

LOG_FILE="submission_log.txt"
SUBMISSIONS_DIR="submissions"
MAX_FILE_SIZE=$((5*1024*1024)) # 5MB in bytes
LOGIN_ATTEMPTS_FILE="login_attempts.txt"
LOCKOUT_TIME=60 # seconds

# Create submissions directory if it doesn't exist
mkdir -p "$SUBMISSIONS_DIR"

# Function to log events
log_event() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to get file hash (MD5)
# ==== SECURITY NOTE (For distinction) ====
# MD5 is used for demonstration purposes only.
# MD5 has known collision vulnerabilities and should NOT be used
# in production systems. SHA-256 or SHA-3 are recommended alternatives.
get_file_hash() {
    md5sum "$1" | cut -d' ' -f1
}

# Function to check duplicate submission
is_duplicate() {
    local filename="$1"
    local filehash="$2"
    
    if [ ! -f "$SUBMISSIONS_DIR/manifest.txt" ]; then
        return 1 # No manifest, not duplicate
    fi
    
    while IFS='|' read -r saved_fname saved_hash saved_sid saved_time; do
        # Check both filename and content hash
        if [ "$saved_fname" = "$filename" ] || [ "$saved_hash" = "$filehash" ]; then
            return 0 # Duplicate found
        fi
    done < "$SUBMISSIONS_DIR/manifest.txt"
    
    return 1 # No duplicate
}

# Function to check login attempts
check_login_attempts() {
    local username="$1"
    local current_time=$(date +%s)
    
    # Clean old attempts outside lockout window
    if [ -f "$LOGIN_ATTEMPTS_FILE" ]; then
        temp_file=$(mktemp)
        while IFS='|' read -r user time status; do
            # Keep only attempts within lockout window
            if [ "$user" = "$username" ] && [ $((current_time - time)) -lt $LOCKOUT_TIME ]; then
                echo "$user|$time|$status" >> "$temp_file"
            fi
        done < "$LOGIN_ATTEMPTS_FILE"
        mv "$temp_file" "$LOGIN_ATTEMPTS_FILE"
    fi
    
    # Count recent failed attempts
    local failed=0
    if [ -f "$LOGIN_ATTEMPTS_FILE" ]; then
        failed=$(grep "^$username|.*|FAIL" "$LOGIN_ATTEMPTS_FILE" 2>/dev/null | wc -l)
    fi
    
    echo $failed
}

# Function to validate file
validate_file() {
    local file_path="$1"
    local filename=$(basename "$file_path")
    
    # Check if file exists
    if [ ! -f "$file_path" ]; then
        echo "❌ Error: File does not exist!"
        return 1
    fi
    
    # ==== SECURITY NOTE (For distinction) ====
    # Extension checking alone is NOT secure. Malicious users can
    # rename any file to .pdf or .docx. Production systems should
    # implement MIME type detection using 'file' command or
    # libmagic for true file type verification.
    
    # Check file extension
    extension="${filename##*.}"
    if [ "$extension" != "pdf" ] && [ "$extension" != "docx" ]; then
        echo "❌ Error: Only .pdf and .docx files are allowed!"
        log_event "Submission failed - Invalid format: $filename"
        return 1
    fi
    
    # Check file size
    if [ -f "$file_path" ]; then
        file_size=$(stat -c%s "$file_path" 2>/dev/null || stat -f%z "$file_path" 2>/dev/null)
        if [ -z "$file_size" ]; then
            echo "❌ Error: Cannot determine file size"
            return 1
        fi
        
        if [ "$file_size" -gt "$MAX_FILE_SIZE" ]; then
            echo "❌ Error: File exceeds 5MB limit!"
            log_event "Submission failed - File too large: $filename ($file_size bytes)"
            return 1
        fi
    fi
    
    return 0
}

# Function to check if account is locked
is_account_locked() {
    local username="$1"
    local attempts=$(check_login_attempts "$username")
    
    if [ -f "$LOGIN_ATTEMPTS_FILE" ] && grep -q "^$username|.*|LOCKED" "$LOGIN_ATTEMPTS_FILE" 2>/dev/null; then
        return 0 # Locked
    fi
    
    return 1 # Not locked
}

# Main menu
while true; do
    echo ""
    echo "====================================="
    echo "   SECURE SUBMISSION SYSTEM"
    echo "====================================="
    echo "1. Submit an assignment"
    echo "2. Check if file already submitted"
    echo "3. List all submitted assignments"
    echo "4. Simulate login attempt"
    echo "5. Exit"
    echo "====================================="
    read -p "Choose option [1-5]: " choice
    
    case $choice in
        1)
            echo ""
            echo "--- Submit Assignment ---"
            read -p "Enter Student ID: " student_id
            read -p "Enter file path: " file_path
            
            # Validate file
            if ! validate_file "$file_path"; then
                continue
            fi
            
            filename=$(basename "$file_path")
            file_hash=$(get_file_hash "$file_path")
            
            # Check for duplicates
            if is_duplicate "$filename" "$file_hash"; then
                echo "❌ Error: Duplicate submission detected!"
                log_event "Duplicate submission blocked: $filename (Hash: $file_hash)"
                continue
            fi
            
            # Copy file to submissions directory
            timestamp=$(date '+%Y%m%d_%H%M%S')
            dest_filename="${student_id}_${timestamp}_${filename}"
            cp "$file_path" "$SUBMISSIONS_DIR/$dest_filename"
            
            # Update manifest
            echo "$filename|$file_hash|$student_id|$timestamp" >> "$SUBMISSIONS_DIR/manifest.txt"
            
            echo "✅ Submission successful!"
            log_event "Submission: $filename by $student_id (Hash: $file_hash)"
            ;;
            
        2)
            echo ""
            echo "--- Check Submission ---"
            read -p "Enter filename to check: " check_file
            
            if [ ! -f "$SUBMISSIONS_DIR/manifest.txt" ]; then
                echo "No submissions found."
                continue
            fi
            
            found=0
            while IFS='|' read -r fname hash sid time; do
                if [ "$fname" = "$check_file" ]; then
                    echo "✅ File '$fname' was submitted by $sid on $time"
                    found=1
                    break
                fi
            done < "$SUBMISSIONS_DIR/manifest.txt"
            
            if [ $found -eq 0 ]; then
                echo "❌ File '$check_file' not found in submissions."
            fi
            log_event "Checked submission status for: $check_file"
            ;;
            
        3)
            echo ""
            echo "--- Submitted Assignments ---"
            if [ ! -f "$SUBMISSIONS_DIR/manifest.txt" ]; then
                echo "No submissions found."
                continue
            fi
            
            echo ""
            printf "%-30s %-12s %-15s\n" "Filename" "Student ID" "Date"
            echo "--------------------------------------------------------"
            while IFS='|' read -r fname hash sid time; do
                printf "%-30s %-12s %-15s\n" "$fname" "$sid" "$time"
            done < "$SUBMISSIONS_DIR/manifest.txt"
            log_event "Listed all submissions"
            ;;
            
        4)
            echo ""
            echo "--- Login Simulation ---"
            read -p "Enter username: " username
            read -p "Enter password: " password
            
            current_time=$(date +%s)
            
            # ==== LOCKOUT NOTE (For distinction) ====
            # TODO: Add automatic unlock mechanism after timeout period
            # or implement admin reset functionality. Currently, once locked,
            # accounts remain locked indefinitely. Production systems should
            # include unlock workflows (email verification, cooldown timer,
            # or admin override).
            
            # Check if account is locked
            if is_account_locked "$username"; then
                echo "🔒 Account LOCKED due to too many failed attempts!"
                echo "   (Note: This implementation has no auto-unlock mechanism)"
                log_event "Login blocked - Account locked: $username"
                continue
            fi
            
            # Simulate login validation (hardcoded for demo)
            if [ "$username" = "student" ] && [ "$password" = "pass123" ]; then
                echo "✅ Login successful!"
                log_event "Successful login: $username"
                # Clear failed attempts on success
                if [ -f "$LOGIN_ATTEMPTS_FILE" ]; then
                    grep -v "^$username|" "$LOGIN_ATTEMPTS_FILE" > tmp && mv tmp "$LOGIN_ATTEMPTS_FILE"
                fi
            else
                echo "❌ Login failed!"
                log_event "Failed login attempt: $username"
                
                # Record failed attempt
                echo "$username|$current_time|FAIL" >> "$LOGIN_ATTEMPTS_FILE"
                
                # Check if account should be locked
                failed_attempts=$(check_login_attempts "$username")
                if [ "$failed_attempts" -ge 3 ]; then
                    echo "🔒 Account LOCKED after 3 failed attempts!"
                    echo "   (Note: Account will remain locked indefinitely)"
                    echo "$username|$current_time|LOCKED" >> "$LOGIN_ATTEMPTS_FILE"
                    log_event "Account locked: $username (3 failed attempts)"
                else
                    attempts_left=$((3 - failed_attempts))
                    echo "   ${attempts_left} attempts remaining before lockout"
                fi
            fi
            ;;
            
        5)
            read -p "Are you sure you want to exit? (y/n): " confirm
            if [ "$confirm" = "y" ] || [ "$confirm" = "Y" ]; then
                log_event "Exited system"
                echo "✅ Goodbye!"
                exit 0
            fi
            ;;
            
        *)
            echo "❌ Invalid option. Please choose 1-5"
            ;;
    esac
done