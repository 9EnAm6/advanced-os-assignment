#!/usr/bin/env python3
"""
task3.py - Secure Examination Submission System (Python Version)
Advanced Operating Systems - Assignment 1
"""

import os
import hashlib
import time
from datetime import datetime

# Configuration
LOG_FILE = "submission_log.txt"
SUBMISSIONS_DIR = "submissions"
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
LOGIN_ATTEMPTS_FILE = "login_attempts.txt"
LOCKOUT_TIME = 60  # seconds

# Create submissions directory if it doesn't exist
if not os.path.exists(SUBMISSIONS_DIR):
    os.makedirs(SUBMISSIONS_DIR)

def log_event(message):
    """Log events with timestamp"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {message}\n")

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def is_duplicate(filename, filehash):
    """Check if file already submitted"""
    manifest_file = os.path.join(SUBMISSIONS_DIR, "manifest.txt")
    if not os.path.exists(manifest_file):
        return False
    
    with open(manifest_file, "r") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 2:
                saved_fname, saved_hash = parts[0], parts[1]
                if saved_fname == filename or saved_hash == filehash:
                    return True
    return False

def check_login_attempts(username):
    """Check and update login attempts"""
    current_time = int(time.time())
    attempts = []
    
    # Read existing attempts
    if os.path.exists(LOGIN_ATTEMPTS_FILE):
        with open(LOGIN_ATTEMPTS_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 3:
                    user, ts, status = parts
                    ts = int(ts)
                    # Keep only attempts within lockout window
                    if user == username and current_time - ts < LOCKOUT_TIME:
                        attempts.append((user, ts, status))
    
    return attempts

def save_login_attempt(username, status):
    """Save login attempt"""
    current_time = int(time.time())
    with open(LOGIN_ATTEMPTS_FILE, "a") as f:
        f.write(f"{username}|{current_time}|{status}\n")

def is_account_locked(username):
    """Check if account is locked"""
    attempts = check_login_attempts(username)
    failed_count = sum(1 for a in attempts if a[2] == "FAIL")
    return failed_count >= 3

def main():
    """Main menu system"""
    while True:
        print("\n" + "="*50)
        print("   SECURE SUBMISSION SYSTEM (Python Version)")
        print("="*50)
        print("1. Submit an assignment")
        print("2. Check if file already submitted")
        print("3. List all submitted assignments")
        print("4. Simulate login attempt")
        print("5. Exit")
        print("="*50)
        
        choice = input("Choose option [1-5]: ").strip()
        
        if choice == "1":
            print("\n--- Submit Assignment ---")
            student_id = input("Enter Student ID: ").strip()
            file_path = input("Enter file path: ").strip()
            
            # Check if file exists
            if not os.path.exists(file_path):
                print("❌ Error: File does not exist!")
                log_event(f"Submission failed - File not found: {file_path}")
                continue
            
            # Check file extension
            filename = os.path.basename(file_path)
            if not (filename.endswith('.pdf') or filename.endswith('.docx')):
                print("❌ Error: Only .pdf and .docx files are allowed!")
                log_event(f"Submission failed - Invalid format: {filename}")
                continue
            
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > MAX_FILE_SIZE:
                print("❌ Error: File exceeds 5MB limit!")
                log_event(f"Submission failed - File too large: {filename}")
                continue
            
            # Check duplicates
            file_hash = get_file_hash(file_path)
            if is_duplicate(filename, file_hash):
                print("❌ Error: Duplicate submission detected!")
                log_event(f"Duplicate submission blocked: {filename}")
                continue
            
            # Copy file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            dest_filename = f"{student_id}_{timestamp}_{filename}"
            dest_path = os.path.join(SUBMISSIONS_DIR, dest_filename)
            
            import shutil
            shutil.copy2(file_path, dest_path)
            
            # Update manifest
            with open(os.path.join(SUBMISSIONS_DIR, "manifest.txt"), "a") as f:
                f.write(f"{filename}|{file_hash}|{student_id}|{timestamp}\n")
            
            print("✅ Submission successful!")
            log_event(f"Submission: {filename} by {student_id}")
            
        elif choice == "2":
            print("\n--- Check Submission ---")
            filename = input("Enter filename to check: ").strip()
            
            manifest_file = os.path.join(SUBMISSIONS_DIR, "manifest.txt")
            if not os.path.exists(manifest_file):
                print("No submissions found.")
                continue
            
            found = False
            with open(manifest_file, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 1 and parts[0] == filename:
                        print(f"✅ File '{filename}' was submitted by {parts[2]} on {parts[3]}")
                        found = True
                        break
            
            if not found:
                print(f"❌ File '{filename}' not found in submissions.")
            
        elif choice == "3":
            print("\n--- Submitted Assignments ---")
            manifest_file = os.path.join(SUBMISSIONS_DIR, "manifest.txt")
            if not os.path.exists(manifest_file):
                print("No submissions found.")
                continue
            
            print(f"{'Filename':<20} {'Student ID':<12} {'Date':<15}")
            print("-"*50)
            with open(manifest_file, "r") as f:
                for line in f:
                    parts = line.strip().split("|")
                    if len(parts) >= 4:
                        print(f"{parts[0]:<20} {parts[2]:<12} {parts[3]:<15}")
            
        elif choice == "4":
            print("\n--- Login Simulation ---")
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            
            if is_account_locked(username):
                print("🔒 Account LOCKED due to too many failed attempts!")
                log_event(f"Login blocked - Account locked: {username}")
                continue
            
            # Simulate login (hardcoded for demo)
            if username == "student" and password == "pass123":
                print("✅ Login successful!")
                log_event(f"Successful login: {username}")
                # Clear failed attempts
                if os.path.exists(LOGIN_ATTEMPTS_FILE):
                    with open(LOGIN_ATTEMPTS_FILE, "r") as f:
                        lines = f.readlines()
                    with open(LOGIN_ATTEMPTS_FILE, "w") as f:
                        for line in lines:
                            if not line.startswith(f"{username}|"):
                                f.write(line)
            else:
                print("❌ Login failed!")
                log_event(f"Failed login attempt: {username}")
                save_login_attempt(username, "FAIL")
                
                # Check if account should be locked
                attempts = check_login_attempts(username)
                failed_count = sum(1 for a in attempts if a[2] == "FAIL")
                if failed_count >= 3:
                    print("🔒 Account LOCKED after 3 failed attempts!")
                    log_event(f"Account locked: {username}")
            
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (y/n): ").lower()
            if confirm == 'y':
                log_event("Exited system")
                print("Goodbye!")
                break
        else:
            print("❌ Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    main()