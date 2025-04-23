# Document Organization Script

A Python script to automatically organize digitized historical documents into date-based subfolders.

## Overview

This script analyzes filenames of the format `XXX_YYYY_MM_DD_NNNN.tif` (where XXX is a three-letter newspaper abbreviation) and organizes them into folders named `YYYY-MM-DD`.

## Requirements

- Python 3.6 or higher
- No additional packages required (only uses Python standard library)

## Usage

1. Make the script executable (optional):
   ```
   chmod +x organize_by_date.py
   ```

2. Run the script with your source directory:
   ```
   python3 organize_by_date.py /path/to/your/files
   ```
   
   Example:
   ```
   python3 organize_by_date.py /Users/dougpeterson/SNL/FGL_1858
   ```

## Features

- Automatically extracts dates from filenames
- Creates date-based folders as needed
- Provides a detailed summary of operations
- Handles files without dates gracefully
- Maintains the original filename

## Example

Before:
```
SNL_1858_01_01_0001.tif
SNL_1858_01_01_0002.tif
FGL_1858_01_08_0001.tif
FGL_1858_01_08_0002.tif
```

After:
```
1858-01-01/
  ├── SNL_1858_01_01_0001.tif
  └── SNL_1858_01_01_0002.tif
1858-01-08/
  ├── FGL_1858_01_08_0001.tif
  └── FGL_1858_01_08_0002.tif
```