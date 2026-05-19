import os
import re
from collections import defaultdict

def parse_m3u(m3u_file):
    """
    解析M3U文件并将其转换为指定格式的TXT文件
    支持两种格式：
    1. 带group-title和tvg-name的标准格式
    2. 简单的EXTINF格式
    
    :param m3u_file: M3U文件的路径
    """
    # 生成输出TXT文件的路径
    txt_file = os.path.splitext(m3u_file)[0] + ".txt"
    
    # 读取M3U文件内容
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    channels = defaultdict(list)
    current_name = None
    
    for i in range(len(lines)):
        line = lines[i].strip()
        
        # 跳过空行和M3U头部标记
        if not line or line == '#EXTM3U':
            continue
            
        if line.startswith('#EXTINF:'):
            # 处理标准格式
            if 'group-title=' in line:
                group_match = re.search(r'group-title="([^"]*)"', line)
                group = group_match.group(1) if group_match else "未分组"
                name_match = re.search(r'tvg-name="([^"]*)"', line)
                current_name = name_match.group(1) if name_match else line.split(',')[-1]
            # 处理简单格式
            else:
                group = "未分组"
                current_name = line.split(',')[-1] if ',' in line else line.split(':')[-1]
                
        # 处理URL行
        elif line.startswith('http'):
            if current_name:
                # 只对完全相同的条目（相同名称和相同URL）进行去重
                if (current_name, line) not in channels[group]:
                    channels[group].append((current_name, line))
                current_name = None

    # 写入TXT文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        for group, channel_list in channels.items():
            # 对每个分组内的频道按名称进行排序，但保留所有不同的URL
            sorted_channels = sorted(channel_list, key=lambda x: x[0])
            
            f.write(f"{group},#genre#\n")
            for name, url in sorted_channels:
                f.write(f"{name},{url}\n")
            f.write("\n")  # 在每个分组后添加一个空行

def convert_all_m3u_files():
    """
    转换当前目录下的所有M3U文件
    """
    current_directory = os.getcwd()
    for file in os.listdir(current_directory):
        if file.endswith(".m3u"):
            m3u_path = os.path.join(current_directory, file)
            print(f"正在转换: {m3u_path}")
            try:
                parse_m3u(m3u_path)
                print(f"成功转换: {m3u_path}")
            except Exception as e:
                print(f"转换失败: {m3u_path}, 错误信息: {str(e)}")

if __name__ == "__main__":
    convert_all_m3u_files()
