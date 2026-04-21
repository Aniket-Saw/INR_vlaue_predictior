#!/usr/bin/env python3
"""
Generate a comprehensive text file containing all project source code and documents.
"""

import os
import sys
from pathlib import Path
from datetime import datetime


def should_include_file(file_path, root_dir):
    """Determine if a file should be included in the report."""
    # Files to exclude
    exclude_patterns = {
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.exe',
        '.git', '.gitignore', '__pycache__', '.venv', 'venv',
        '.env', '.DS_Store', '.idea', '.vscode',
        '.csv', '.xlsx', '.xls', '.db', '.sqlite',
        'node_modules', '.egg-info'
    }
    
    # File extensions to include
    include_extensions = {
        '.py', '.txt', '.md', '.yml', '.yaml', '.json',
        '.sql', '.sh', '.bat', '.ps1', '.r', '.R',
        '.java', '.cpp', '.c', '.h', '.js', '.ts',
        '.html', '.css', '.xml', '.html'
    }
    
    name = os.path.basename(file_path)
    
    # Skip hidden files and directories
    if name.startswith('.'):
        return False
    
    # Skip excluded patterns
    for pattern in exclude_patterns:
        if pattern in name or pattern in str(file_path):
            return False
    
    # Skip large files
    try:
        if os.path.getsize(file_path) > 10_000_000:  # 10MB
            return False
    except OSError:
        return False
    
    # Check extension
    ext = os.path.splitext(name)[1].lower()
    if ext in include_extensions:
        return True
    
    # Include specific files without extensions
    if name in {'README', 'Makefile', 'Dockerfile', 'requirements', 'setup', 'LICENSE'}:
        return True
    
    return False


def generate_codebase_report(root_dir, output_file='codebase_report.txt'):
    """Generate a text report of all project source code."""
    output_path = os.path.join(root_dir, output_file)
    
    # Collect all files
    files_to_process = []
    for root, dirs, files in os.walk(root_dir):
        # Skip certain directories
        dirs[:] = [d for d in dirs if d not in {'.git', '__pycache__', 'venv', '.venv', 'node_modules'}]
        
        for file in files:
            file_path = os.path.join(root, file)
            if should_include_file(file_path, root_dir):
                rel_path = os.path.relpath(file_path, root_dir)
                files_to_process.append((file_path, rel_path))
    
    # Sort files for better organization
    files_to_process.sort(key=lambda x: x[1])
    
    # Generate report
    with open(output_path, 'w', encoding='utf-8', errors='ignore') as report:
        # Write header
        report.write("=" * 80 + "\n")
        report.write("PROJECT CODEBASE REPORT\n")
        report.write("=" * 80 + "\n")
        report.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        report.write(f"Root Directory: {root_dir}\n")
        report.write(f"Total Files: {len(files_to_process)}\n")
        report.write("=" * 80 + "\n\n")
        
        # Table of Contents
        report.write("TABLE OF CONTENTS\n")
        report.write("-" * 80 + "\n")
        for i, (_, rel_path) in enumerate(files_to_process, 1):
            report.write(f"{i:3d}. {rel_path}\n")
        report.write("\n" + "=" * 80 + "\n\n")
        
        # File contents
        for file_path, rel_path in files_to_process:
            report.write("\n" + "=" * 80 + "\n")
            report.write(f"FILE: {rel_path}\n")
            report.write("=" * 80 + "\n")
            
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    report.write(content)
                    if not content.endswith('\n'):
                        report.write("\n")
            except Exception as e:
                report.write(f"[ERROR reading file: {str(e)}]\n")
            
            report.write("\n")
    
    print(f"✓ Codebase report generated: {output_path}")
    print(f"✓ Total files included: {len(files_to_process)}")
    return output_path


if __name__ == "__main__":
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Generate report
    output_file = "codebase_report.txt"
    if len(sys.argv) > 1:
        output_file = sys.argv[1]
    
    generate_codebase_report(script_dir, output_file)
