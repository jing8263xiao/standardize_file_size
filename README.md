# File Standardization Toolkit

English | [简体中文](README-CN.md)

A toolkit for processing and standardizing file sizes, primarily designed for file preparation before uploading to Telegram cloud backup.

## Features

### 1. Directory Analysis (directory_detection.py)
- Analyzes the size of all subdirectories in a specified directory
- Generates human-readable size formats
- Saves analysis results to JSON file
- Records and compares directory size changes over time

### 2. File Compression (compress_files.py)
- Compresses each subdirectory into separate ZIP files
- Supports progress display
- Customizable output directory
- Displays compressed file sizes

### 3. Small File Merging (merge_small_file.py)
- Evenly distributes files from source folder to specified number of target folders
- Optimizes distribution based on file sizes
- Generates detailed allocation report (JSON format)
- Displays total size of each target folder

### 4. Large File Splitting (split_large_file.py)
- Supports large file splitting and merging
- Default chunk size of 1.5GB
- Supports batch processing of large files in directory
- Generates split record file
- Smart chunk file management and merging

## Usage

### Directory Analysis
```bash
python directory_detection.py
```

### File Compression
```bash
python compress_files.py <source_directory> [-o output_directory]
```

### Small File Merging
```bash
python merge_small_file.py <source_directory> <number_of_target_folders>
```

### Large File Splitting
```bash
# Split files
python split_large_file.py split <file_path> [-s chunk_size(GB)]

# Merge files
python split_large_file.py merge <chunk_file_path_or_directory>
```

## Output Files
- `directory_analysis_results.json`: Directory analysis results
- `directory_analysis_diff.json`: Directory change records
- `folder_files_map.json`: File allocation mapping
- `split_record.json`: File splitting records

## Usage Workflow Example

1. Use `directory_detection.py` to analyze directory sizes, generating `directory_analysis_results.json`
    - When run again after generating `directory_analysis_results.json`, it will automatically read the file and analyze directory changes, generating `directory_analysis_diff.json`

2. Use `compress_files.py` to compress second-level folders in the specified path, generating a `compressed_files` folder containing compressed files

3. Use `merge_small_file.py` to merge small files in the compressed directory into multiple merged folders, each not exceeding 1.5GB, stored in the generated `merged_files` folder

4. Use `compress_files.py` again to compress the standardized merged folders, generating a `compressed_files` folder containing compressed files ready for upload

5. Use `split_large_file.py` to batch split all large files (>2GB) in the specified directory into chunks of 1.5GB by default, stored in the current folder for upload
    - Later use `split_large_file.py` to merge chunk files in the specified directory

## Notes
- Recommended to analyze directories before processing large numbers of files
- Compression and splitting operations may require significant disk space
- Regular backup of important data is recommended
