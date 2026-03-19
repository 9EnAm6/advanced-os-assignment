# Advanced Operating Systems - Assignment 1

## 📋 Project Overview
This repository contains three scripts for the Advanced Operating Systems assignment:
- `task1.sh`: Process and Resource Management System  
- `task2.py`: High Performance Computing Job Scheduler  
- `task3.sh`: Secure Examination Submission System  

## 🚀 How to Run

### Prerequisites
- Ubuntu/WSL environment  
- Python 3 (for task2.py)  

### Setup
1. Make scripts executable:
   ```bash
   chmod +x task1.sh task3.sh

   - Run tasks:
- Task 1: Process Management

./task1.sh
- Task 2: Job Scheduler

python3 task2.py
- Task 3: Secure Submission System
./task3.sh

# Advanced Operating Systems - Assignment 1

## 📋 Project Overview
This repository contains three scripts for the Advanced Operating Systems assignment:
- `task1.sh`: Process and Resource Management System  
- `task2.py`: High Performance Computing Job Scheduler  
- `task3.sh`: Secure Examination Submission System  

## 🚀 How to Run

### Prerequisites
- Ubuntu/WSL environment  
- Python 3 (for task2.py)  

### Setup
1. Make scripts executable:
   ```bash
   chmod +x task1.sh task3.sh


- Run tasks:
- Task 1: Process Management
./task1.sh
- Task 2: Job Scheduler
python3 task2.py
- Task 3: Secure Submission System
./task3.sh


📁 File Structure
- task1.sh - Bash script for process monitoring and log management
- task2.py - Python scheduler with Round Robin and Priority algorithms
- task3.sh - Bash script for file validation and access control
- README.md - This file
👤 Author
- Name: Md Shuaib
- Email: amd20301@gmail.com
- GitHub: 9EnAm6
🔗 GitHub Repository
https://github.com/9EnAm6/advanced-os-assignment

📝 Script Details
Task 1: Process Management System
Features:
- Display CPU and memory usage
- List top 10 memory-consuming processes
- Terminate processes with confirmation
- Protect critical system processes
- Detect and archive large log files (>50MB)
- Warning when archive exceeds 1GB
- Comprehensive logging
Task 2: Job Scheduler
Features:
- Submit jobs with Student ID, name, time, priority (1-10)
- View pending and completed jobs
- Round Robin scheduling (5-second quantum)
- Priority scheduling (highest priority first)
- Job queue persistence
- Activity logging
Task 3: Secure Submission System
Features:
- File validation (.pdf, .docx only)
- File size limit (5MB maximum)
- Duplicate detection via MD5 hashing
- Account lockout after 3 failed login attempts
- 60-second lockout window
- Comprehensive logging

📄 Log Files Generated
- system_monitor_log.txt - Task 1 activities
- scheduler_log.txt - Task 2 activities
- submission_log.txt - Task 3 activities
- job_queue.txt - Pending jobs (Task 2)
- completed_jobs.txt - Completed jobs (Task 2)
- login_attempts.txt - Login tracking (Task 3)
📂 Directories Created
- ArchiveLogs/ - Compressed log files (Task 1)
- submissions/ - Uploaded assignment files (Task 3)



