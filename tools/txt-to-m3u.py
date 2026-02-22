import os

def convert_txt_to_m3u(epg_url):
    # 获取当前脚本所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    for file_name in os.listdir(current_dir):
        if not file_name.endswith('.txt'):
            print(f'跳过文件 {file_name}，不是txt格式。')
            continue

        file_path = os.path.join(current_dir, file_name)
        m3u_content = [f'#EXTM3U x-tvg-url="{epg_url}"']
        channel_genre = '未分类'

        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                for line_number, line in enumerate(file, 1):
                    line = line.strip()
                    if not line or line.startswith('#'):
                        continue

                    # 检查是否是分类标记（支持两种格式）
                    if line.endswith('#genre#'):
                        if ',' in line:
                            channel_genre = line.replace(',#genre#', '').strip()
                        else:
                            channel_genre = line.replace('#genre#', '').strip()
                        continue

                    try:
                        if ',' not in line:
                            print(f'提示：在文件 {file_name} 的第 {line_number} 行发现分类标记：{line}')
                            continue
                            
                        channel_name, channel_url = map(str.strip, line.split(',', 1))
                        tvg_logo = f'https://tb.zbds.top/logo/{channel_name}.png'
                        m3u_entry = f'#EXTINF:-1 group-title="{channel_genre}" tvg-name="{channel_name}" tvg-logo="{tvg_logo}",{channel_name}\n{channel_url}'
                        m3u_content.append(m3u_entry)
                    except ValueError as e:
                        print(f'警告：在文件 {file_name} 的第 {line_number} 行解析失败：{line}')
                        continue

            new_file_path = os.path.join(current_dir, file_name.replace('.txt', '.m3u'))
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write('\n'.join(m3u_content))

            print(f'转换文件 {file_name} 成功！')
            
        except Exception as e:
            print(f'处理文件 {file_name} 时发生错误：{str(e)}')

# 指定EPG URL
epg_url = 'http://epg.51zmt.top:8000/e.xml'

# 调用函数进行转换
convert_txt_to_m3u(epg_url)
