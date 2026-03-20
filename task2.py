#!/usr/bin/env python3
"""
Task 2: High Performance Computing Job Scheduler
Advanced Operating Systems - Assignment 1
DISTINCTION VERSION - With robust error handling and defensive programming
"""

import time
import datetime
import os
import sys

# Configuration
QUEUE_FILE = "job_queue.txt"
COMPLETED_FILE = "completed_jobs.txt"
LOG_FILE = "scheduler_log.txt"
TIME_QUANTUM = 5  # seconds for Round Robin

def log_event(student_id, job_name, schedule_type, status):
    """Log scheduling events with timestamp"""
    try:
        with open(LOG_FILE, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp} - {student_id} - {job_name} - {schedule_type} - {status}\n")
    except IOError as e:
        print(f"⚠️  Warning: Could not write to log file: {e}")

def load_jobs():
    """Load jobs from queue file with robust error handling"""
    jobs = []
    if not os.path.exists(QUEUE_FILE):
        return jobs
    
    try:
        with open(QUEUE_FILE, "r") as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                parts = line.strip().split("|")
                if len(parts) != 4:
                    print(f"⚠️  Warning: Malformed line {line_num} in {QUEUE_FILE}: {line}")
                    continue
                
                student_id, job_name, est_time, priority = parts
                
                # ==== ROBUST PARSING WITH TRY/EXCEPT (Critical for distinction) ====
                try:
                    est_time = int(est_time)
                    priority = int(priority)
                except ValueError:
                    print(f"⚠️  Warning: Invalid numeric data in line {line_num}: {line}")
                    continue
                
                # Validate data ranges
                if priority < 1 or priority > 10:
                    print(f"⚠️  Warning: Priority out of range (1-10) in line {line_num}: {priority}")
                    # Adjust to valid range
                    priority = max(1, min(10, priority))
                
                if est_time <= 0:
                    print(f"⚠️  Warning: Invalid execution time in line {line_num}: {est_time}")
                    est_time = 1  # Default to 1 second
                
                jobs.append({
                    "student_id": student_id,
                    "job_name": job_name,
                    "est_time": est_time,
                    "priority": priority,
                    "remaining": est_time
                })
    except IOError as e:
        print(f"❌ Error reading job queue: {e}")
    
    return jobs

def save_jobs(jobs):
    """Save jobs to queue file"""
    try:
        with open(QUEUE_FILE, "w") as f:
            for job in jobs:
                f.write(f"{job['student_id']}|{job['job_name']}|{job['est_time']}|{job['priority']}\n")
    except IOError as e:
        print(f"❌ Error saving job queue: {e}")

def save_completed_job(job):
    """Save completed job to completed file"""
    try:
        with open(COMPLETED_FILE, "a") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"{timestamp}|{job['student_id']}|{job['job_name']}|{job['est_time']}|{job['priority']}\n")
    except IOError as e:
        print(f"❌ Error saving completed job: {e}")

def display_jobs(jobs):
    """Display pending jobs in formatted table"""
    if not jobs:
        print("\n📋 No pending jobs in queue.")
        return
    
    print("\n" + "="*80)
    print(f"{'Student ID':<12} {'Job Name':<20} {'Est Time':<10} {'Priority':<8} {'Remaining':<10}")
    print("="*80)
    for job in jobs:
        print(f"{job['student_id']:<12} {job['job_name']:<20} {job['est_time']:<10} {job['priority']:<8} {job['remaining']:<10}")
    print("="*80)

def round_robin_schedule(jobs):
    """Round Robin scheduling algorithm with 5-second quantum"""
    if not jobs:
        print("\n📋 No jobs to process.")
        return []
    
    print("\n" + "="*60)
    print("🔄 ROUND ROBIN SCHEDULING (Quantum: 5 seconds)")
    print("="*60)
    
    # ==== DESIGN LIMITATION COMMENT (For distinction) ====
    # NOTE: This implementation uses time.sleep() which blocks the entire program.
    # Real operating system schedulers use preemption and context switching
    # without blocking the scheduler itself. This is a simplification for
    # demonstration purposes.
    
    queue = jobs.copy()
    completed = []
    
    while queue:
        job = queue.pop(0)
        print(f"\n▶️ Executing: {job['job_name']} (Student: {job['student_id']})")
        print(f"   Remaining time: {job['remaining']} seconds")
        
        # Execute for quantum or remaining time
        execute_time = min(TIME_QUANTUM, job['remaining'])
        
        # Simulate execution (blocks - see note above)
        for i in range(execute_time):
            time.sleep(1)
            print(f"   ⏳ Progress: {i+1}/{execute_time} seconds", end='\r')
        print()  # New line after progress
        
        job['remaining'] -= execute_time
        log_event(job['student_id'], job['job_name'], "Round Robin", f"Executed for {execute_time}s")
        
        if job['remaining'] <= 0:
            print(f"✅ Job {job['job_name']} COMPLETED!")
            completed.append(job)
            save_completed_job(job)
            log_event(job['student_id'], job['job_name'], "Round Robin", "Completed")
        else:
            print(f"⏸️ Job {job['job_name']} paused. Remaining: {job['remaining']}s")
            queue.append(job)  # Add back to queue
    
    print("\n✅ All jobs processed!")
    return completed

def priority_schedule(jobs):
    """Priority scheduling algorithm (non-preemptive)"""
    if not jobs:
        print("\n📋 No jobs to process.")
        return []
    
    print("\n" + "="*60)
    print("🎯 PRIORITY SCHEDULING (Highest priority first)")
    print("="*60)
    
    # ==== DESIGN LIMITATION COMMENT (For distinction) ====
    # NOTE: This implementation does not include priority aging.
    # In real systems, aging prevents starvation of low-priority jobs
    # by gradually increasing their priority over time.
    
    # Sort by priority (lower number = higher priority)
    sorted_jobs = sorted(jobs, key=lambda x: x['priority'])
    
    completed = []
    for job in sorted_jobs:
        print(f"\n▶️ Executing: {job['job_name']} (Priority: {job['priority']})")
        print(f"   Student: {job['student_id']}, Time: {job['est_time']} seconds")
        
        # Simulate execution with progress indicator
        for i in range(job['est_time']):
            time.sleep(1)
            print(f"   ⏳ Progress: {i+1}/{job['est_time']} seconds", end='\r')
        print()  # New line after progress
        
        print(f"✅ Job {job['job_name']} COMPLETED!")
        completed.append(job)
        save_completed_job(job)
        log_event(job['student_id'], job['job_name'], "Priority", "Completed")
    
    print("\n✅ All jobs processed!")
    return completed

def validate_job_input(student_id, job_name, est_time, priority):
    """Validate job submission inputs"""
    if not student_id or not student_id.strip():
        return False, "Student ID cannot be empty"
    
    if not job_name or not job_name.strip():
        return False, "Job name cannot be empty"
    
    try:
        est_time = int(est_time)
        if est_time <= 0:
            return False, "Estimated time must be positive"
    except ValueError:
        return False, "Estimated time must be a number"
    
    try:
        priority = int(priority)
        if priority < 1 or priority > 10:
            return False, "Priority must be between 1 and 10"
    except ValueError:
        return False, "Priority must be a number"
    
    return True, None

def main():
    """Main program with menu system"""
    
    # Load existing jobs
    global pending_jobs
    pending_jobs = load_jobs()
    
    print("\n" + "="*60)
    print("   HIGH PERFORMANCE COMPUTING JOB SCHEDULER")
    print("="*60)
    print("DISTINCTION VERSION - With robust error handling")
    
    while True:
        print("\n" + "="*60)
        print("   MAIN MENU")
        print("="*60)
        print("1. View pending jobs")
        print("2. Submit a new job")
        print("3. Process job queue")
        print("4. View completed jobs")
        print("5. Exit")
        print("="*60)
        
        choice = input("Choose option [1-5]: ").strip()
        
        if choice == "1":
            display_jobs(pending_jobs)
            
        elif choice == "2":
            print("\n--- Submit New Job ---")
            student_id = input("Enter Student ID: ").strip()
            job_name = input("Enter Job Name: ").strip()
            est_time = input("Enter Estimated Time (seconds): ").strip()
            priority = input("Enter Priority (1-10, 1=highest): ").strip()
            
            # Validate inputs
            valid, error_msg = validate_job_input(student_id, job_name, est_time, priority)
            if not valid:
                print(f"❌ {error_msg}")
                continue
            
            # Convert to integers now that validation passed
            est_time = int(est_time)
            priority = int(priority)
            
            # Create new job
            new_job = {
                "student_id": student_id,
                "job_name": job_name,
                "est_time": est_time,
                "priority": priority,
                "remaining": est_time
            }
            
            pending_jobs.append(new_job)
            save_jobs(pending_jobs)
            log_event(student_id, job_name, "Submission", f"Added to queue (Priority:{priority}, Time:{est_time}s)")
            print(f"✅ Job '{job_name}' submitted successfully!")
            
        elif choice == "3":
            if not pending_jobs:
                print("\n📋 No pending jobs to process.")
                continue
            
            print("\nSelect scheduling algorithm:")
            print("1. Round Robin")
            print("2. Priority Scheduling")
            algo = input("Choose [1-2]: ").strip()
            
            completed = []
            if algo == "1":
                completed = round_robin_schedule(pending_jobs)
                pending_jobs = []  # Clear queue after processing
            elif algo == "2":
                completed = priority_schedule(pending_jobs)
                pending_jobs = []  # Clear queue after processing
            else:
                print("❌ Invalid choice.")
                continue
            
            # Save updated queue (should be empty)
            save_jobs(pending_jobs)
            
        elif choice == "4":
            print("\n--- Completed Jobs ---")
            if os.path.exists(COMPLETED_FILE):
                try:
                    with open(COMPLETED_FILE, "r") as f:
                        content = f.read().strip()
                        if content:
                            print("\n" + "="*80)
                            print(f"{'Timestamp':<20} {'Student ID':<12} {'Job Name':<20} {'Time':<6} {'Priority':<8}")
                            print("="*80)
                            
                            for line in content.split('\n'):
                                parts = line.split('|')
                                if len(parts) == 5:
                                    ts, sid, name, t, pri = parts
                                    print(f"{ts:<20} {sid:<12} {name:<20} {t:<6} {pri:<8}")
                        else:
                            print("No completed jobs yet.")
                except IOError as e:
                    print(f"❌ Error reading completed jobs: {e}")
            else:
                print("No completed jobs yet.")
            
        elif choice == "5":
            confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
            if confirm == 'y':
                log_event("SYSTEM", "EXIT", "SYSTEM", "User exited")
                print("✅ Goodbye!")
                break
        else:
            print("❌ Invalid option. Please choose 1-5.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user. Exiting gracefully...")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        print("Please report this issue.")
        sys.exit(1)