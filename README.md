# 🖥️ Advanced Operating Systems - Assignment 1

<div align="center">
  
  ### *University Data Centre Management Suite*
  
  [![GitHub](https://img.shields.io/badge/Repository-Advanced--OS--Assignment-blue?logo=github)](https://github.com/9EnAm6/advanced-os-assignment)
  [![Bash](https://img.shields.io/badge/Language-Bash-4EAA25?logo=gnu-bash)](https://www.gnu.org/software/bash/)
  [![Python](https://img.shields.io/badge/Language-Python-3776AB?logo=python)](https://www.python.org/)
  [![License](https://img.shields.io/badge/License-Academic%20Use-green)](LICENSE)
  
</div>

---

## 📋 **Table of Contents**
- [Project Overview](#-project-overview)
- [Learning Outcomes](#-learning-outcomes)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
- [Script Documentation](#-script-documentation)
  - [Task 1: Process Management System](#task-1-process-management-system)
  - [Task 2: High Performance Computing Job Scheduler](#task-2-high-performance-computing-job-scheduler)
  - [Task 3: Secure Examination Submission System](#task-3-secure-examination-submission-system)
- [File Structure](#-file-structure)
- [Log Files](#-log-files)
- [Screenshots](#-screenshots)
- [Troubleshooting](#-troubleshooting)
- [Author](#-author)
- [License](#-license)
- [Acknowledgments](#-acknowledgments)

---

## 🎯 **Project Overview**

This repository contains three system administration scripts developed for the **Advanced Operating Systems (U14553)** module at Canterbury Christ Church University. Each script demonstrates core operating system concepts including process management, CPU scheduling algorithms, file system operations, and access control mechanisms.

| **Script** | **Language** | **Purpose** |
|------------|--------------|-------------|
| `task1.sh` | Bash | Process monitoring, log archiving, and system resource management |
| `task2.py` | Python | Job scheduler with Round Robin and Priority algorithms |
| `task3.sh` | Bash | Secure file validation, duplicate detection, and login monitoring |

---

## 📚 **Learning Outcomes**

This assignment addresses the following learning outcomes:

| **Outcome** | **Description** | **Demonstrated In** |
|-------------|-----------------|---------------------|
| **LO2** | Exploit tools and techniques for OS administration | Task 1 & Task 3 |
| **LO4** | Operate UNIX command line environment with POSIX standards | Task 2 |

---

## 💻 **System Requirements**

### **Hardware Requirements**
| Component | Minimum Requirement |
|-----------|---------------------|
| Processor | Any x86_64 processor |
| RAM | 2GB (4GB recommended) |
| Storage | 100MB free space |

### **Software Requirements**
| Requirement | Version | Purpose |
|-------------|---------|---------|
| **Ubuntu/WSL** | 20.04 or higher | Linux environment for Bash scripts |
| **Python** | 3.8+ | Required for Task 2 scheduler |
| **Bash** | 5.0+ | Built-in shell for Task 1 and Task 3 |
| **Git** | 2.25+ | Version control |

## 📋 Design Decisions & Trade-offs

### Task 1: Process Management
- **Tool Selection:** Chose `ps` over `top` or `/proc` for simpler parsing, trading real-time monitoring for snapshot reliability.
- **Critical Process Protection:** Blacklist approach (PID 1,2, systemd) balances safety with flexibility but may miss some critical processes.
- **Log Archiving:** Manual implementation with `find` and `tar` demonstrates understanding, but `logrotate` would be production-ready.

### Task 2: Job Scheduler
- **Scheduling Algorithms:** Round Robin (5s quantum) vs Priority – fairness vs efficiency trade-off.
- **Starvation Risk:** Priority scheduling without aging may starve low-priority jobs – acknowledged limitation.
- **Data Persistence:** Flat files chosen over database for simplicity, but lacks concurrency control.

### Task 3: Secure Submission
- **MD5 Usage:** Known weakness – collisions possible. SHA-256 recommended for production.
- **File Validation:** Extension checking only – should use magic number verification.
- **Lockout Mechanism:** 3 attempts/60s balances security and usability, but lacks unlock workflow.

## ⚠️ Known Limitations
- Task 1: No process tree termination, slow `du` on large directories
- Task 2: No priority aging, no I/O wait consideration
- Task 3: MD5 collisions, no IP logging, no CAPTCHA

### **WSL Installation (Windows Users)**
If you're on Windows and don't have WSL:
```powershell
# Run in PowerShell as Administrator
wsl --install
After installation, search for "Ubuntu" in Start menu and complete setup.
🔧 Installation Guide
Step 1: Clone the Repository
git clone https://github.com/9EnAm6/advanced-os-assignment.git
cd advanced-os-assignment
Step 2: Make Scripts Executable
chmod +x task1.sh task3.sh
Step 3: Verify Python Installation
python3 --version
# Should show Python 3.8 or higher
Step 4: (Optional) Create a Virtual Environment for Python
python3 -m venv venv
source venv/bin/activate
📖 Script Documentation
Task 1: Process Management System
File: task1.sh

Purpose
Monitors system resources, manages processes, and handles log file archiving.

Features
Option	Function	Description
1	Display CPU/Memory Usage	Shows real-time system resource utilization
2	List Top 10 Memory Processes	Displays PID, user, CPU%, MEM%, and command name
3	Terminate a Process	Safely terminates selected process with confirmation
4	Inspect Disk and Archive Logs	Finds log files >50MB and compresses them
5	Exit	Graceful exit with confirmation
Critical Process Protection
The script protects these system processes from termination:

init, systemd, kernel processes

Any process with PID 1 or 2
How to Run
./task1.sh

Sample Output
=====================================
   PROCESS MANAGEMENT SYSTEM
=====================================
1. Display CPU/Memory Usage
2. List Top 10 Memory Processes
3. Terminate a Process
4. Inspect Disk and Archive Logs
5. Exit
=====================================
Choose option [1-5]: 2

---------------------------------
Top 10 Memory-Consuming Processes:
---------------------------------
PID   USER     %CPU  %MEM  COMMAND
1234  novos    12.5  15.2  python3
5678  root     5.2   8.1   systemd
...
Task 2: High Performance Computing Job Scheduler
File: task2.py

Purpose
Simulates a job scheduling system with multiple scheduling algorithms.

Job Format
Each job contains:

Student ID: Unique identifier

Job Name: Descriptive name

Estimated Time: Execution time in seconds

Priority: Value from 1-10 (1 = highest priority)

Features
Option	Function	Description
1	View Pending Jobs	Displays current job queue
2	Submit a New Job	Adds job to queue with all details
3	Process Job Queue	Choose between Round Robin or Priority
4	View Completed Jobs	Shows execution history
5	Exit	Exit with confirmation

Scheduling Algorithms
Algorithm	Description
Round Robin	Time quantum of 5 seconds; jobs cycle until completion
Priority	Non-preemptive; highest priority (lowest number) executes first

How to Run
python3 task2.py

Sample Output

============================================================
   HIGH PERFORMANCE COMPUTING JOB SCHEDULER
============================================================
1. View pending jobs
2. Submit a new job
3. Process job queue
4. View completed jobs
5. Exit
============================================================
Choose option [1-5]: 2

--- Submit New Job ---
Enter Student ID: S12345
Enter Job Name: DataProcessing
Enter Estimated Time (seconds): 10
Enter Priority (1-10, 1=highest): 3
✅ Job 'DataProcessing' submitted successfully!

Task 3: Secure Examination Submission System

File: task3.sh

Purpose
Simulates a secure file submission system with access control.

Security Features
Feature	Description
File Validation	Only accepts .pdf and .docx files
File Size Limit	Maximum 5MB per file
Duplicate Detection	MD5 hashing to prevent duplicate submissions
Account Lockout	Locks after 3 failed login attempts within 60 seconds
Comprehensive Logging	All actions recorded with timestamps
Menu Options
Option	Function	Description
1	Submit Assignment	Validates and stores submission
2	Check Submission	Verifies if file already submitted
3	List Submissions	Shows all submitted assignments
4	Simulate Login	Tests access control system
5	Exit	Exit with confirmation

How to Run
./task3.sh
Sample Output
=====================================
   SECURE SUBMISSION SYSTEM
=====================================
1. Submit an assignment
2. Check if file already submitted
3. List all submitted assignments
4. Simulate login attempt
5. Exit
=====================================
Choose option [1-5]: 1

--- Submit Assignment ---
Enter Student ID: S12345
Enter file path: ./assignment.pdf
✅ Submission successful!

📁 File Structure
📦 advanced-os-assignment/
├── 📄 task1.sh                     # Process Management System (Bash)
├── 📄 task2.py                     # Job Scheduler (Python)
├── 📄 task3.sh                     # Secure Submission System (Bash)
├── 📄 README.md                     # This documentation file
├── 📄 .gitignore                    # Git ignore rules
├── 📁 Advanced_OS_Snapshots/         # Screenshots of script execution
├── 📁 submissions/                   # Uploaded assignment files (Task 3)
├── 📁 ArchiveLogs/                   # Compressed log files (Task 1)
├── 📄 system_monitor_log.txt         # Task 1 activity log
├── 📄 scheduler_log.txt              # Task 2 activity log
├── 📄 submission_log.txt             # Task 3 activity log
├── 📄 job_queue.txt                   # Pending jobs (Task 2)
├── 📄 completed_jobs.txt              # Completed jobs (Task 2)
├── 📄 login_attempts.txt              # Login tracking (Task 3)
└── 📄 test.pdf                        # Sample test file

📊 Log Files
Log File	Created By	Purpose
system_monitor_log.txt	Task 1	Records all administrative actions
scheduler_log.txt	Task 2	Logs job submissions and executions
submission_log.txt	Task 3	Tracks file submissions and login attempts
job_queue.txt	Task 2	Stores pending jobs
completed_jobs.txt	Task 2	Archives completed job history
login_attempts.txt	Task 3	Tracks login attempts for lockout feature

Sample Log Entry Format

2026-03-19 14:30:45 - Terminated process PID 1234
2026-03-19 14:31:20 - Submitted job: DataProcessing by S12345
2026-03-19 14:32:10 - File submission: assignment.pdf by S12345

📸 Screenshots

Screenshots demonstrating script execution can be found in the Advanced_OS_Snapshots/ folder.

🔍 Troubleshooting

Common Issues and Solutions
Problem	Solution
Permission denied	Run chmod +x task1.sh task3.sh
Command not found	Ensure you're in the correct directory: cd ~/advanced-os-assignment
Python not found	Install Python: sudo apt install python3 -y
Script hangs	Press Ctrl+C to force quit
Git push fails	Run git pull origin main --rebase then try again
WSL not working	Restart Windows or run wsl --shutdown in PowerShell

Testing Scripts
# Test Task 1
./task1.sh

# Test Task 2
python3 task2.py

# Test Task 3
./task3.sh

Resetting the System
To start fresh:

rm -f *.txt
rm -rf submissions/ ArchiveLogs/

👤 Author
<div align="center">
Md Shuaib
Student ID	[Your Student ID]
Email	amd20301@gmail.com
GitHub	@9EnAm6
Institution	Canterbury Christ Church University
Module	Advanced Operating Systems (U14553)
Course	BSc (Hons) Computer Science
</div>

📜 License
This project is submitted as part of academic coursework for the Advanced Operating Systems module at Canterbury Christ Church University.

All rights reserved. Unauthorized copying, distribution, or use of this code is prohibited.

© 2026 Md Shuaib. All Rights Reserved.



🙏 Acknowledgments

Dr Victor Obarafor - Module Leader

Tim Jackson - Module Team

Canterbury Christ Church University - Computing Department

Open Source Community - For bash and Python documentation

<div align="center">
⭐ If you found this project helpful, please star the repository! ⭐

⬆ Back to Top

Last Updated: March 2026

</div> ```