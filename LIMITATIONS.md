# Known Limitations and Future Improvements

## Task 1: Process Management System
- **Process Tree Handling:** Does not terminate child processes when parent is killed
- **Performance:** `du` command becomes slow on very large directories
- **Critical Process Detection:** Relies on process names which can be spoofed

## Task 2: Job Scheduler
- **Blocking Simulation:** Uses `time.sleep()` which blocks the scheduler - real OS uses preemption
- **No Priority Aging:** Low-priority jobs may starve indefinitely
- **No Concurrency Control:** Multiple users submitting simultaneously could corrupt queue files

## Task 3: Secure Submission System
- **MD5 Weakness:** Known collision vulnerabilities - SHA-256 recommended
- **Extension-only Validation:** Can be bypassed by renaming files
- **No Unlock Mechanism:** Once locked, accounts stay locked forever
- **No IP Tracking:** Cannot detect distributed attacks

## Future Improvements
1. Replace MD5 with SHA-256
2. Add MIME type detection using `file` command
3. Implement priority aging to prevent starvation
4. Add database backend for concurrent access
5. Implement exponential backoff for login attempts
6. Add email verification for account unlock