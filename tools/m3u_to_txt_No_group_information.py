import os
from datetime import datetime

def parse_m3u(m3u_file):
    """
    解析M3U文件并将其转换为TXT文件
    
    :param m3u_file: M3U文件的路径
    """
    # 生成新的输出TXT文件名
    current_datetime = datetime.now()
    current_date = current_datetime.strftime("%Y%m%d")
    current_time = current_datetime.strftime("%H%M%S")
    base_name = os.path.splitext(os.path.basename(m3u_file))[0]
    txt_file = f"{base_name}_{current_date}_{current_time}.txt"
    
    # 读取M3U文件内容
    with open(m3u_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    channels = []
    for i in range(len(lines)):
        line = lines[i].strip()
        if line.startswith('#EXTINF:-1'):
            # 提取频道信息
            info = line.split('tvg-name="')[1].split('"')[0] if 'tvg-name="' in line else "未知"
            # 获取URL（假设URL在下一行）
            url = lines[i + 1].strip() if i + 1 < len(lines) else ""
            channels.append((info, url))

    # 写入TXT文件
    with open(txt_file, 'w', encoding='utf-8') as f:
        for info, url in channels:
            f.write(f"{info},{url}\n")

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
