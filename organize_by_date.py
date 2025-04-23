#!/usr/bin/env python3
"""
Organize digitized documents into date-based folders.

This script scans a source directory for image files that have dates in their filenames,
then organizes them into subfolders named with the date.

Usage:
    python organize_by_date.py <source_directory>

Example:
    python organize_by_date.py /Users/dougpeterson/SNL/FGL_1858
"""

import os
import sys
import shutil
import re
from datetime import datetime


def extract_date(filename):
    """
    Extract date from filename with more flexible matching:
    - Allow one digit month or day numbers
    - Allow dashes instead of underscores
    - Allow any number of characters for the newspaper abbreviation
    
    Returns date string in format YYYY-MM-DD or None if no match
    """
    # New flexible pattern
    pattern = r'([A-Za-z]+)[_-](\d{4})[_-](\d{1,2})[_-](\d{1,2})[_-]'
    match = re.search(pattern, filename)
    if match:
        abbr, year, month, day = match.groups()
        # Zero-pad month and day to ensure consistent format
        month = month.zfill(2)
        day = day.zfill(2)
        return f"{year}-{month}-{day}", is_standard_format(abbr, filename)
    return None, False


def is_standard_format(abbr, filename):
    """
    Check if a filename follows the standard format: XXX_YYYY_MM_DD_NNNN.tif
    where XXX is a three-letter uppercase abbreviation
    """
    # Check if abbreviation is exactly 3 uppercase letters
    if not (len(abbr) == 3 and abbr.isupper() and abbr.isalpha()):
        return False
    
    # Check if the filename uses underscores, not dashes
    if '-' in filename:
        return False
    
    # Check if month and day are two digits
    # First extract the parts with the original strict pattern
    strict_pattern = r'[A-Z]{3}_(\d{4})_(\d{2})_(\d{2})_'
    match = re.search(strict_pattern, filename)
    if not match:
        return False
    
    return True


def organize_files(source_dir):
    """
    Organize files in source_dir into date-based subfolders
    """
    # Verify the source directory exists
    if not os.path.isdir(source_dir):
        print(f"Error: Source directory '{source_dir}' does not exist")
        return False

    # Count for summary
    total_files = 0
    moved_files = 0
    skipped_files = 0
    created_folders = set()
    
    # Track non-standard filenames
    non_standard_files = []

    # Get all files in the source directory
    for filename in os.listdir(source_dir):
        # Skip directories
        file_path = os.path.join(source_dir, filename)
        if not os.path.isfile(file_path):
            continue

        total_files += 1
        
        # Extract date from filename
        date_result = extract_date(filename)
        if date_result[0] is None:
            print(f"Warning: Could not extract date from '{filename}', skipping")
            skipped_files += 1
            continue
        
        date_str, is_standard = date_result
        
        # Record non-standard filenames
        if not is_standard:
            non_standard_files.append(filename)
        
        # Create destination folder if it doesn't exist
        dest_folder = os.path.join(source_dir, date_str)
        if not os.path.exists(dest_folder):
            os.makedirs(dest_folder)
            created_folders.add(date_str)
            print(f"Created folder: {date_str}")
        
        # Move file to destination folder
        dest_path = os.path.join(dest_folder, filename)
        shutil.move(file_path, dest_path)
        moved_files += 1
        print(f"Moved: {filename} → {date_str}/")

    # Write non-standard filenames to report file
    if non_standard_files:
        report_path = os.path.join(os.path.dirname(source_dir), f"{os.path.basename(source_dir)}_non_standard.txt")
        with open(report_path, 'w') as f:
            f.write(f"Non-standard filenames found in {source_dir}:\n")
            f.write("\n".join(non_standard_files))
        print(f"\nReported {len(non_standard_files)} non-standard filenames to {report_path}")

    # Print summary
    print("\nSummary:")
    print(f"Total files processed: {total_files}")
    print(f"Files moved: {moved_files}")
    print(f"Files skipped: {skipped_files}")
    print(f"Folders created: {len(created_folders)}")
    print(f"Non-standard filenames: {len(non_standard_files)}")
    
    return True


def main():
    # Check if source directory is provided
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <source_directory>")
        return 1
    
    source_dir = sys.argv[1]
    print(f"Organizing files in: {source_dir}")
    
    # Organize files
    if organize_files(source_dir):
        print("\nOrganization complete!")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main()) 