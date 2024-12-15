import os
from pathlib import Path
import humanize
import json
import time
from datetime import datetime

def get_directory_size(directory):
    """计算目录大小"""
    total_size = 0
    try:
        for path in Path(directory).rglob('*'):
            if path.is_file():
                total_size += path.stat().st_size
    except (PermissionError, OSError):
        return 0
    return total_size

def load_previous_result(json_file):
    """加载上次执行的结果"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def save_result(data, json_file):
    """保存执行结果到JSON文件"""
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def format_file_size(size_in_bytes):
    """
    将字节大小转换为人类可读的格式（使用1024作为基数）
    """
    units = ['B', 'KiB', 'MiB', 'GiB', 'TiB', 'PiB']
    size = float(size_in_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def calculate_diff(current_data, previous_data):
    """计算当前结果与上次执行结果的差异"""
    if not previous_data:
        return None
    
    total_size_change = current_data["total_size"] - previous_data["total_size"]
    
    diff = {
        "timestamp": datetime.now().isoformat(),
        "directory_changes": [],
        "total_size_change": total_size_change,
        "total_size_change_readable": format_file_size(total_size_change)
    }
    
    # 创建目录大小的字典用于比较
    prev_dirs = {item["name"]: item["size"] for item in previous_data["directories"]}
    curr_dirs = {item["name"]: item["size"] for item in current_data["directories"]}
    
    # 检查每个目录的变化
    all_dirs = set(prev_dirs.keys()) | set(curr_dirs.keys())
    for dir_name in all_dirs:
        old_size = prev_dirs.get(dir_name, 0)
        new_size = curr_dirs.get(dir_name, 0)
        if old_size != new_size:
            size_change = new_size - old_size
            diff["directory_changes"].append({
                "name": dir_name,
                "old_size": old_size,
                "old_size_readable": format_file_size(old_size),
                "new_size": new_size,
                "new_size_readable": format_file_size(new_size),
                "change": size_change,
                "change_readable": format_file_size(size_change)
            })
    
    return diff

def analyze_directory(root_path):
    """分析目录结构和大小"""
    start_time = time.time()
    
    print(f"\n开始分析目录: {root_path}\n")
    print("=" * 60)
    
    # 获取所有子目录
    subdirs = []
    try:
        for item in os.scandir(root_path):
            if item.is_dir():
                subdirs.append(item.path)
    except PermissionError:
        print("错误：没有权限访问某些目录")
        return None

    # 统计信息
    print(f"子目录总数: {len(subdirs)}")
    print("=" * 60)
    
    # 分析每个子目录
    dir_sizes = []
    total_size = 0
    for subdir in subdirs:
        size = get_directory_size(subdir)
        dir_sizes.append((subdir, size))
        total_size += size
    
    # 按大小排序
    dir_sizes.sort(key=lambda x: x[1], reverse=True)
    
    # 显示结果
    print("\n各子目录大小（从大到小排序）：")
    print("-" * 60)
    for dir_path, size in dir_sizes:
        dir_name = os.path.basename(dir_path)
        human_size = format_file_size(size)
        print(f"{dir_name:<40} {human_size:>10}")
    
    print("\n总大小:", format_file_size(total_size))
    
    # 记录执行时间
    execution_time = time.time() - start_time
    
    # 修改结果数据结构，只保存目录名而不是完整路径
    result = {
        "timestamp": datetime.now().isoformat(),
        "root_path": os.path.basename(root_path),  # 只保存目录名
        "total_size": total_size,
        "total_size_readable": format_file_size(total_size),
        "execution_time": execution_time,
        "subdirectory_count": len(subdirs),
        "directories": [
            {
                "name": os.path.basename(dir_path),
                "size": size,
                "size_readable": format_file_size(size)
            }
            for dir_path, size in dir_sizes
        ]
    }
    
    return result

if __name__ == "__main__":
    # 获取用户输入的目录路径
    directory = input("请输入要分析的目录路径: ").strip()
    
    # 设置结果文件路径
    results_file = "directory_analysis_results.json"
    diff_file = "directory_analysis_diff.json"
    
    # 检查目录是否存在
    if not os.path.exists(directory):
        print("错误：目录不存在！")
    elif not os.path.isdir(directory):
        print("错误：输入路径不是一个目录！")
    else:
        # 加载上次的结果
        previous_result = load_previous_result(results_file)
        
        # 执行当前分析
        current_result = analyze_directory(directory)
        
        if current_result:
            # 保存当前结果
            save_result(current_result, results_file)
            
            # 计算并保存差异
            diff = calculate_diff(current_result, previous_result)
            if diff:
                save_result(diff, diff_file)
                print(f"\n差异已保存到 {diff_file}")
            
            print(f"\n分析结果已保存到 {results_file}")
            print(f"执行时间: {current_result['execution_time']:.2f} 秒")
