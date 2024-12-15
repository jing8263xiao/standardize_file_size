# 文件标准化工具集

[English](README.md) | 简体中文

这是一个用于处理和标准化文件大小的工具集合，主要用于上传 Telegram 云备份前对文件的处理。

## 功能特性

### 1. 目录分析 (directory_detection.py)
- 分析指定目录下所有子目录的大小
- 生成人类可读的大小格式
- 保存分析结果到 JSON 文件
- 记录并比较不同时间的目录大小变化

### 2. 文件压缩 (compress_files.py)
- 将目录下的每个子文件夹单独压缩成 ZIP 文件
- 支持进度显示
- 可自定义输出目录
- 显示压缩后的文件大小

### 3. 小文件合并 (merge_small_file.py)
- 将源文件夹中的文件平均分配到指定数量的目标文件夹
- 根据文件大小优化分配
- 生成详细的分配报告（JSON格式）
- 显示每个目标文件夹的总大小

### 4. 大文件拆分 (split_large_file.py)
- 支持大文件拆分和合并
- 默认按 1.5GB 大小进行分片
- 支持批量处理目录中的大文件
- 生成拆分记录文件
- 智能分片文件管理和合并

## 使用方法

### 目录分析
```bash
python directory_detection.py
```

### 文件压缩
```bash
python compress_files.py <源目录> [-o 输出目录]
```

### 小文件合并
```bash
python merge_small_file.py <源目录> <目标文件夹数量>
```

### 大文件拆分
```bash
# 拆分文件
python split_large_file.py split <文件路径> [-s 分片大小(GB)]

# 合并文件
python split_large_file.py merge <分片文件路径或目录>
```

## 输出文件
- `directory_analysis_results.json`: 目录分析结果
- `directory_analysis_diff.json`: 目录变化记录
- `folder_files_map.json`: 文件分配映射
- `split_record.json`: 文件拆分记录

## 使用流程示例

1. 使用 `directory_detection.py` 分析目录大小，生成 `directory_analysis_results.json` 文件
    
    -  已经生成 `directory_analysis_results.json` 文件后，再次运行时，会自动读取 `directory_analysis_results.json` 文件，并进行目录变化分析，生成 `directory_analysis_diff.json` 文件。

2. 使用 `compress_files.py` 压缩指定路径下的二级文件夹，生成 `compressed_files` 文件夹，存放压缩后的文件

3. 使用 `merge_small_file.py` 合并压缩目录中的小文件，存放在多个合并文件夹中，每个生成的合并文件夹大小不超过1.5GB，所有合并文件夹存放在生成的 `merged_files` 文件夹中

4. 再次使用 `compress_files.py` 压缩合并后的标准化文件夹，生成 `compressed_files` 文件夹，存放压缩后的文件，用于上传

5. 使用 `split_large_file.py` 批量拆分指定目录下的所有大文件（大于2GB），拆分后的分片文件默认按 1.5GB 大小进行分片，存放在当前文件夹中，即可用于上传

    - 后续可使用 `split_large_file.py` 合并指定目录下的分片文件







## 注意事项
- 建议在处理大量文件前先进行目录分析
- 压缩和拆分操作可能需要较大的磁盘空间
- 建议定期备份重要数据
