import os
import math
import argparse
import glob
import json

def format_size(size_in_bytes):
    """
    将字节大小转换为人类可读的格式
    """
    units = ['B', 'KB', 'MB', 'GB', 'TB']
    size = float(size_in_bytes)
    unit_index = 0
    
    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1
    
    return f"{size:.2f} {units[unit_index]}"

def get_large_files(directory, min_size=2*1024*1024*1024):
    """
    获取目录下所有大于指定大小的文件
    """
    large_files = []
    for file in os.listdir(directory):
        file_path = os.path.join(directory, file)
        if os.path.isfile(file_path) and os.path.getsize(file_path) > min_size:
            large_files.append(file_path)
    return large_files

def split_large_file(input_file, chunk_size=1.5*1024*1024*1024):
    """
    将大文件拆分成多个小文件
    """
    if not os.path.exists(input_file):
        print(f"错误: 文件 '{input_file}' 不存在")
        return None, None
        
    file_size = os.path.getsize(input_file)
    num_chunks = math.ceil(file_size / chunk_size)
    chunk_sizes = []
    
    with open(input_file, 'rb') as f:
        for i in range(num_chunks):
            chunk_name = f"{input_file}.part{i+1}"
            print(f"正在写入分片 {i+1}/{num_chunks}")
            
            with open(chunk_name, 'wb') as chunk:
                data = f.read(int(chunk_size))
                if data:
                    chunk.write(data)
                    chunk_sizes.append(len(data))
    
    return num_chunks, chunk_sizes

def find_chunk_files(input_path):
    """
    查找分片文件
    
    参数:
        input_path: 输入路径(可以是目录或文件)
    返回:
        (分片文件列表, 输出文件路径)
    """
    if os.path.isdir(input_path):
        # 如果是目录,查找目录下的所有.part文件
        base_dir = input_path
        # 获取目录下所有分片文件
        chunk_files = glob.glob(os.path.join(base_dir, "*.part*"))
        
        if not chunk_files:
            print(f"错误: 在目录 '{input_path}' 中未找到分片文件")
            return None, None
            
        # 按文件名分组
        file_groups = {}
        for chunk_file in chunk_files:
            base_name = chunk_file.rsplit('.part', 1)[0]
            if base_name not in file_groups:
                file_groups[base_name] = []
            file_groups[base_name].append(chunk_file)
        
        if len(file_groups) > 1:
            print("在目录中找到多个分片文件组:")
            for i, base_name in enumerate(file_groups.keys(), 1):
                print(f"{i}. {os.path.basename(base_name)} ({len(file_groups[base_name])} 个分片)")
            try:
                choice = int(input("请选择要合并的文件组 (输入序号): "))
                if choice < 1 or choice > len(file_groups):
                    print("无效的选择")
                    return None, None
                base_name = list(file_groups.keys())[choice-1]
                selected_group = file_groups[base_name]
            except ValueError:
                print("无效的输入")
                return None, None
        else:
            base_name = list(file_groups.keys())[0]
            selected_group = file_groups[base_name]
            
    else:
        # 如果是文件,查找同目录下的相关分片
        base_name = input_path.rsplit('.part', 1)[0]
        base_dir = os.path.dirname(base_name) or '.'
        file_pattern = f"{base_name}.part*"
        selected_group = glob.glob(file_pattern)
    
    # 确保文件按分片序号排序
    selected_group.sort(key=lambda x: int(x.rsplit('.part', 1)[1]))
    
    # 生成输出文件路径
    output_file = base_name
    
    return selected_group, output_file

def merge_files(chunk_files, output_file):
    """
    合并指定的分片文件
    
    参数:
        chunk_files: 分片文件路径列表
        output_file: 输出文件名
    """
    # 检查所有分片是否存在
    for chunk_file in chunk_files:
        if not os.path.exists(chunk_file):
            print(f"错误: 分片文件 '{chunk_file}' 不存在")
            return

    with open(output_file, 'wb') as outfile:
        for i, chunk_file in enumerate(chunk_files, 1):
            print(f"正在合并分片 {i}/{len(chunk_files)}: {os.path.basename(chunk_file)}")
            
            with open(chunk_file, 'rb') as chunk:
                outfile.write(chunk.read())

def main():
    parser = argparse.ArgumentParser(description='大文件拆分与合并工具')
    parser.add_argument('action', choices=['split', 'merge'], help='操作类型: split(拆分) 或 merge(合并)')
    
    if len(os.sys.argv) > 1 and os.sys.argv[1] == 'split':
        parser.add_argument('input_path', help='要拆分的文件或目录路径')
        parser.add_argument('-s', '--chunk-size', type=float, default=1.5,
                          help='拆分时每个分片的大小(GB),默认1.5GB')
    else:
        parser.add_argument('input_path', help='要合并的分片文件路径或包含分片文件的目录')

    args = parser.parse_args()

    if args.action == 'split':
        chunk_size = args.chunk_size * 1024 * 1024 * 1024  # 转换为字节
        
        if os.path.isdir(args.input_path):
            # 目录模式
            large_files = get_large_files(args.input_path)
            if not large_files:
                print(f"在目录 '{args.input_path}' 中未找到大于2GB的文件")
                return
                
            split_info = {}
            for file_path in large_files:
                print(f"\n开始拆分文件: {file_path}")
                num_chunks, chunk_sizes = split_large_file(file_path, chunk_size)
                if num_chunks:
                    split_info[file_path] = {
                        'total_size': format_size(os.path.getsize(file_path)),
                        'num_chunks': num_chunks,
                        'chunk_sizes': [format_size(size) for size in chunk_sizes]
                    }
                    print(f"文件拆分完成! 共生成 {num_chunks} 个分片")
            
            # 生成记录文件
            record_file = os.path.join(args.input_path, 'split_record.json')
            with open(record_file, 'w', encoding='utf-8') as f:
                json.dump(split_info, f, indent=2, ensure_ascii=False)
            print(f"\n拆分记录已保存到: {record_file}")
            
        else:
            # 单文件模式
            print(f"开始拆分文件: {args.input_path}")
            num_chunks, _ = split_large_file(args.input_path, chunk_size)
            if num_chunks:
                print(f"文件拆分完成! 共生成 {num_chunks} 个分片")

    elif args.action == 'merge':
        chunk_files, output_file = find_chunk_files(args.input_path)
        if chunk_files and output_file:
            print(f"找到 {len(chunk_files)} 个分片文件")
            print(f"输出文件: {output_file}")
            merge_files(chunk_files, output_file)
            print("文件合并完成!")

if __name__ == "__main__":
    main()
