#!/usr/bin/env python3

# Task 2: High Performance Computing Job Scheduler
# Advanced Operating Systems - Assignment 1

import time
import datetime
import os

# File paths
QUEUE_FILE = "job_queue.txt"
COMPLETED_FILE = "completed_jobs.txt"
LOG_FILE = "scheduler_log.txt"

# Time quantum for Round Robin (seconds)
TIME_QUANTUM = 5

def log_event(student_id, job_name, schedule_type, status):
    """Log scheduling events"""
    with open(LOG_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp} - {student_id} - {job_name} - {schedule_type} - {status}\n")

def load_jobs():
    """Load jobs from queue file"""
    jobs = []
    if os.path.exists(QUEUE_FILE):
        with open(QUEUE_FILE, "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 4:
                    student_id, job_name, est_time, priority = parts
                    jobs.append({
                        "student_id": student_id,
                        "job_name": job_name,
                        "est_time": int(est_time),
                        "priority": int(priority),
                        "remaining": int(est_time)
                    })
    return jobs

def save_jobs(jobs):
    """Save jobs to queue file"""
    with open(QUEUE_FILE, "w") as f:
        for job in jobs:
            f.write(f"{job['student_id']}|{job['job_name']}|{job['est_time']}|{job['priority']}\n")

def save_completed_job(job):
    """Save completed job to completed file"""
    with open(COMPLETED_FILE, "a") as f:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{timestamp}|{job['student_id']}|{job['job_name']}|{job['est_time']}|{job['priority']}\n")

def display_jobs(jobs):
    """Display pending jobs"""
    if not jobs:
        print("\n📋 No pending jobs in queue.")
        return
    
    print("\n" + "="*60)
    print(f"{'Student ID':<12} {'Job Name':<15} {'Est Time':<10} {'Priority':<8} {'Remaining':<10}")
    print("="*60)
    for job in jobs:
        print(f"{job['student_id']:<12} {job['job_name']:<15} {job['est_time']:<10} {job['priority']:<8} {job['remaining']:<10}")
    print("="*60)

def round_robin_schedule(jobs):
    """Round Robin scheduling algorithm"""
    if not jobs:
        print("\n📋 No jobs to process.")
        return
    
    print("\n" + "="*60)
    print("🔄 ROUND ROBIN SCHEDULING (Quantum: 5 seconds)")
    print("="*60)
    
    queue = jobs.copy()
    completed = []
    
    while queue:
        job = queue.pop(0)
        print(f"\n▶️ Executing: {job['job_name']} (Student: {job['student_id']})")
        print(f"   Remaining time: {job['remaining']} seconds")
        
        # Simulate execution for quantum or remaining time
        execute_time = min(TIME_QUANTUM, job['remaining'])
        time.sleep(execute_time)  # Simulate execution
        
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
    
    # Update jobs list (remove completed)
    global pending_jobs
    pending_jobs = []
    print("\n✅ All jobs processed!")

def priority_schedule(jobs):
    """Priority scheduling algorithm"""
    if not jobs:
        print("\n📋 No jobs to process.")
        return
    
    print("\n" + "="*60)
    print("🎯 PRIORITY SCHEDULING (Highest priority first)")
    print("="*60)
    
    # Sort by priority (lower number = higher priority)
    sorted_jobs = sorted(jobs, key=lambda x: x['priority'])
    
    for job in sorted_jobs:
        print(f"\n▶️ Executing: {job['job_name']} (Priority: {job['priority']})")
        print(f"   Student: {job['student_id']}, Time: {job['est_time']} seconds")
        
        time.sleep(job['est_time'])  # Simulate execution
        
        print(f"✅ Job {job['job_name']} COMPLETED!")
        save_completed_job(job)
        log_event(job['student_id'], job['job_name'], "Priority", "Completed")
    
    # Clear pending jobs
    global pending_jobs
    pending_jobs = []
    print("\n✅ All jobs processed!")

# Main program
pending_jobs = load_jobs()

while True:
    print("\n" + "="*60)
    print("   HIGH PERFORMANCE COMPUTING JOB SCHEDULER")
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
        if not (student_id and job_name and est_time.isdigit() and priority.isdigit()):
            print("❌ Invalid input. All fields required and time/priority must be numbers.")
            continue
        
        est_time = int(est_time)
        priority = int(priority)
        
        if priority < 1 or priority > 10:
            print("❌ Priority must be between 1 and 10.")
            continue
        
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
        
        if algo == "1":
            round_robin_schedule(pending_jobs)
        elif algo == "2":
            priority_schedule(pending_jobs)
        else:
            print("❌ Invalid choice.")
            continue
        
        # Save updated queue (should be empty after processing)
        save_jobs(pending_jobs)
        
    elif choice == "4":
        print("\n--- Completed Jobs ---")
        if os.path.exists(COMPLETED_FILE):
            with open(COMPLETED_FILE, "r") as f:
                content = f.read()
                if content:
                    print(content)
                else:
                    print("No completed jobs yet.")
        else:
            print("No completed jobs yet.")
            
    elif choice == "5":
        confirm = input("Are you sure you want to exit? (y/n): ").strip().lower()
        if confirm == 'y':
            log_event("SYSTEM", "EXIT", "SYSTEM", "User exited")
            print("Goodbye!")
            break
    else:
        print("❌ Invalid option. Please choose 1-5.")