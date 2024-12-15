# File Standardization Toolkit

English | [简体中文](README-CN.md)

A toolkit for processing and standardizing file sizes...

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
