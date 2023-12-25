import os

def convert_txt_to_m3u(folder_path, epg_url):
    # 获取指定文件夹下的所有文件
    file_list = os.listdir(folder_path)
    
    # 遍历文件列表
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        
        # 检查文件是否为txt格式
        if file_name.endswith('.txt'):
            # 读取txt文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # 构建m3u格式的内容
            m3u_content = f'#EXTM3U x-tvg-url="{epg_url}"\n'
            
            channel_genre = '未分类'  # 默认分类为"未分类"
            
            for line in lines:
                line = line.strip()
                
                # 跳过空行和注释行
                if not line or line.startswith('#'):
                    continue
                
                # 判断是否为频道分类行
                if line.endswith(',#genre#'):
                    channel_genre = line.replace(',#genre#', '').strip()
                    continue
                
                # 解析频道名称和链接
                parts = line.split(',')
                channel_name = parts[0].strip()
                channel_url = parts[1].strip()
                
                # 构建m3u格式的频道条目，将频道分类名称写入group-title字段
                tvg_logo = f'https://live.zhoujie218.top/taibiao/{channel_name}.png'
                m3u_entry = f'#EXTINF:-1 group-title="{channel_genre}" tvg-name="{channel_name}" tvg-logo="{tvg_logo}",{channel_name}\n{channel_url}\n'
                m3u_content += m3u_entry
            
            # 构建新的文件名
            new_file_name = file_name.replace('.txt', '.m3u')
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # 将m3u内容写入新文件
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(m3u_content)
                
            print(f'转换文件 {file_name} 成功！')
        else:
            print(f'跳过文件 {file_name}，不是txt格式。')

# 指定目录路径和EPG URL
folder_path = 'dsyy'
epg_url = 'http://epg.51zmt.top:8000/e.xml'

# 调用函数进行转换
convert_txt_to_m3u(folder_path, epg_url)
