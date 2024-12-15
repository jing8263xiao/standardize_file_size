import os
import shutil
from pathlib import Path
import argparse
import json

def analyse_and_divide_files(source_path, target_folders_count):
    """
    分析源文件夹中的文件并将它们平均分配到指定数量的目标文件夹中
    
    参数:
    source_path: 源文件夹路径
    target_folders_count: 目标文件夹数量
    """
    # 获取所有文件及其大小
    files_with_size = []
    total_size = 0
    
    for file_path in Path(source_path).rglob('*'):
        if file_path.is_file():
            size = file_path.stat().st_size
            files_with_size.append((file_path, size))
            total_size += size
    
    # 按文件大小降序排序
    files_with_size.sort(key=lambda x: x[1], reverse=True)
    
    # 计算每个目标文件夹的理想大小
    target_size_per_folder = total_size / target_folders_count
    
    # 创建目标文件夹
    target_folders = []
    folder_files_map = {}  # 用于记录文件夹和文件的对应关系
    
    for i in range(target_folders_count):
        folder_name = f'folder_{i+1}'
        folder_path = os.path.join(source_path, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        target_folders.append({'path': folder_path, 'current_size': 0})
        folder_files_map[folder_name] = {
            'files': [],
            'total_size': 0,
            'total_size_mb': 0
        }
    
    # 分配文件到文件夹
    for file_path, file_size in files_with_size:
        # 找到当前大小最小的文件夹
        target_folder = min(target_folders, key=lambda x: x['current_size'])
        
        # 移动文件到目标文件夹
        dest_path = os.path.join(target_folder['path'], file_path.name)
        shutil.move(file_path, dest_path)
        
        # 更新文件夹大小
        target_folder['current_size'] += file_size
        
        # 记录文件分配信息
        folder_name = os.path.basename(target_folder['path'])
        folder_files_map[folder_name]['files'].append(file_path.name)
        folder_files_map[folder_name]['total_size'] = target_folder['current_size']
        folder_files_map[folder_name]['total_size_mb'] = round(target_folder['current_size'] / (1024 * 1024), 2)
    
    # 打印每个文件夹的最终大小
    for folder in target_folders:
        size_mb = folder['current_size'] / (1024 * 1024)
        print(f"文件夹 {os.path.basename(folder['path'])}: {size_mb:.2f} MB")
    
    # 添加总体信息
    folder_files_map['summary'] = {
        'total_size': total_size,
        'total_size_mb': round(total_size / (1024 * 1024), 2),
        'folder_count': target_folders_count,
        'average_size_mb': round(total_size / (1024 * 1024) / target_folders_count, 2)
    }
    
    # 保存文件分配信息到JSON文件
    json_path = os.path.join(source_path, 'folder_files_map.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(folder_files_map, f, ensure_ascii=False, indent=4)
    
    print(f"\n文件分配信息已保存到: {json_path}")

if __name__ == "__main__":
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将文件夹中的文件平均分配到指定数量的子文件夹中')
    parser.add_argument('source_path', type=str, help='源文件夹路径')
    parser.add_argument('target_folders_count', type=int, help='目标文件夹数量')
    
    # 解析命令行参数
    args = parser.parse_args()
    
    # 运行主函数
    analyse_and_divide_files(args.source_path, args.target_folders_count)
