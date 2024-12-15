import os
import zipfile
from pathlib import Path

def compress_subdirectories(source_path, output_path=None):
    """
    将指定目录下的每个子文件夹分别压缩成zip文件，
    所有zip文件放在指定的输出目录中的"源目录名_output"子目录下
    
    参数:
        source_path: 包含多个子文件夹的目录路径
        output_path: 输出目录路径，默认为源目录同级目录
    """
    source_path = Path(source_path)
    print(f"开始处理目录: {source_path}")
    
    # 设置输出目录
    if output_path is None:
        base_output_dir = source_path.parent
    else:
        base_output_dir = Path(output_path)
    
    # 在输出目录下创建源目录名_output子目录
    output_dir = base_output_dir / f"{source_path.name}_output"
    output_dir.mkdir(exist_ok=True, parents=True)
    print(f"创建输出目录: {output_dir}")
    
    # 获取所有子目录
    subdirs = [d for d in source_path.iterdir() if d.is_dir()]
    total_dirs = len(subdirs)
    print(f"找到 {total_dirs} 个子目录需要处理")
    
    for index, subdir in enumerate(subdirs, 1):
        print(f"\n[{index}/{total_dirs}] 开始压缩目录: {subdir.name}")
        
        # 在output目录中创建zip文件
        output_path = output_dir / f"{subdir.name}.zip"
        
        # 首先计算总文件数，用于显示进度
        total_files = sum(len(files) for _, _, files in os.walk(subdir))
        processed_files = 0
        
        # 创建zip文件
        with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zf:
            # 遍历子目录
            for root, dirs, files in os.walk(subdir):
                for file in files:
                    # 获取文件完整路径
                    file_path = os.path.join(root, file)
                    # 获取相对路径(用于zip文件内的目录结构)
                    arcname = os.path.relpath(file_path, subdir)
                    # 将文件添加到zip中
                    zf.write(file_path, arcname)
                    
                    # 更新进度
                    processed_files += 1
                    print(f"\r  进度: {processed_files}/{total_files} 文件 "
                          f"({processed_files/total_files*100:.1f}%) - "
                          f"当前: {arcname}", end="")
        
        print(f"\n  完成: {subdir.name} -> {output_path}")
        print(f"  压缩文件大小: {output_path.stat().st_size / 1024 / 1024:.2f} MB")

    print(f"\n所有目录处理完成！共处理 {total_dirs} 个目录")

if __name__ == "__main__":
    import sys
    import argparse
    
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(description='将目录下的每个子文件夹压缩成独立的zip文件')
    parser.add_argument('source', help='源目录路径')
    parser.add_argument('-o', '--output', help='输出目录路径（可选）')
    
    args = parser.parse_args()
    compress_subdirectories(args.source, args.output)
