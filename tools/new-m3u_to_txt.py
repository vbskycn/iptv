import os
import re
from collections import defaultdict

def parse_m3u(m3u_file):
    """
    解析M3U文件并将其转换为指定格式的TXT文件
    
    :param m3u_file: M3U文件的路径
    """
    # 生成输出TXT文件的路径
    txt_file = os.path.splitext(m3u_file)[0] + ".txt"
    
    # 读取M3U文件内容
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    channels = defaultdict(list)
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith('#EXTINF:'):
            # 提取分组信息
            group_match = re.search(r'group-title="([^"]*)"', line)
            group = group_match.group(1) if group_match else "未分组"
            
            # 提取频道名称 - 查找方括号中的内容
            name_match = re.search(r'\[([^\]]*)\]\s*(.+)$', line.split(',')[-1])
            if name_match:
                # 如果找到方括号格式，使用方括号后面的内容作为名称
                name = name_match.group(2).strip()
            else:
                # 如果没有方括号格式，使用逗号后的完整内容
                name = line.split(',')[-1].strip()
            
            # 获取URL（假设URL在下一行）
            if i + 1 < len(lines):
                url = lines[i + 1].strip()
                if url and not url.startswith('#'):
                    channels[group].append((name, url))

    # 写入TXT文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        for group, channel_list in channels.items():
            f.write(f"{group},#genre#\n")
            for name, url in channel_list:
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
            parse_m3u(m3u_path)

if __name__ == "__main__":
    convert_all_m3u_files()
