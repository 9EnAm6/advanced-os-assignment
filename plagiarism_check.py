#!/usr/bin/env python3
"""
plagiarism_check.py - Simple Code Similarity Checker
Advanced Operating Systems - Assignment 1
Note: This is a basic educational tool for demonstrating concepts
"""

import os
import hashlib
import sys
from collections import defaultdict

def get_file_hash(filepath):
    """Calculate MD5 hash of file"""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        hasher.update(f.read())
    return hasher.hexdigest()

def normalize_code(content):
    """Normalize code by removing comments and whitespace"""
    lines = []
    for line in content.split('\n'):
        # Remove comments (simple version)
        if '#' in line:
            line = line[:line.index('#')]
        if '//' in line:
            line = line[:line.index('//')]
        
        # Remove whitespace
        line = line.strip()
        if line:
            lines.append(line)
    return ' '.join(lines)

def jaccard_similarity(text1, text2):
    """Calculate Jaccard similarity between two texts"""
    set1 = set(text1.split())
    set2 = set(text2.split())
    
    if not set1 and not set2:
        return 1.0
    
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union if union > 0 else 0

def check_plagiarism(directory, threshold=0.7):
    """Check all Python/Bash files in directory for similarity"""
    files = []
    for f in os.listdir(directory):
        if f.endswith(('.py', '.sh')) and os.path.isfile(os.path.join(directory, f)):
            files.append(f)
    
    if len(files) < 2:
        print("📁 Need at least 2 files to compare")
        return
    
    print("\n" + "="*60)
    print("🔍 PLAGIARISM SIMILARITY CHECK")
    print("="*60)
    print(f"Threshold: {threshold*100}%")
    print("-"*60)
    
    # Compare each pair
    for i in range(len(files)):
        for j in range(i+1, len(files)):
            file1 = os.path.join(directory, files[i])
            file2 = os.path.join(directory, files[j])
            
            # Read files
            with open(file1, 'r') as f:
                content1 = f.read()
            with open(file2, 'r') as f:
                content2 = f.read()
            
            # Normalize
            norm1 = normalize_code(content1)
            norm2 = normalize_code(content2)
            
            # Calculate similarity
            similarity = jaccard_similarity(norm1, norm2)
            
            # Get hashes
            hash1 = get_file_hash(file1)[:8]
            hash2 = get_file_hash(file2)[:8]
            
            # Report
            status = "⚠️  SUSPICIOUS" if similarity > threshold else "✅ OK"
            print(f"{files[i]:<20} vs {files[j]:<20}")
            print(f"  Similarity: {similarity:.1%} {status}")
            print(f"  Hashes: {hash1} / {hash2}")
            print("-"*60)

def main():
    """Main function"""
    print("📋 Simple Code Similarity Checker")
    print("For educational purposes only - not a real plagiarism detector\n")
    
    directory = input("Enter directory to check [.]: ").strip() or "."
    
    if not os.path.exists(directory):
        print("❌ Directory not found!")
        return
    
    try:
        threshold_input = input("Enter similarity threshold (0.0-1.0) [0.7]: ").strip()
        threshold = float(threshold_input) if threshold_input else 0.7
        threshold = max(0.0, min(1.0, threshold))
    except ValueError:
        threshold = 0.7
        print(f"Using default threshold: {threshold}")
    
    check_plagiarism(directory, threshold)

if __name__ == "__main__":
    main()