import os

def convert_txt_to_m3u(folder_path, epg_url):
    # ?????????????
    file_list = os.listdir(folder_path)
    
    # ??????
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        
        # ???????txt??
        if file_name.endswith('.txt'):
            # ??txt????
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            # ??m3u?????
            m3u_content = f'#EXTM3U x-tvg-url="{epg_url}"\n'
            
            channel_genre = '???'  # ?????"???"
            
            for line in lines:
                line = line.strip()
                
                # ????????
                if not line or line.startswith('#'):
                    continue
                
                # ??????????
                if line.endswith(',#genre#'):
                    channel_genre = line.replace(',#genre#', '').strip()
                    continue
                
                # ?????????
                parts = line.split(',')
                channel_name = parts[0].strip()
                channel_url = parts[1].strip()
                
                # ??m3u?????????????????group-title??
                tvg_logo = f'https://live.proton218.top/taibiao/{channel_name}.png'
                m3u_entry = f'#EXTINF:-1 group-title="{channel_genre}" tvg-name="{channel_name}" tvg-logo="{tvg_logo}",{channel_name}\n{channel_url}\n'
                m3u_content += m3u_entry
            
            # ???????
            new_file_name = file_name.replace('.txt', '.m3u')
            new_file_path = os.path.join(folder_path, new_file_name)
            
            # ?m3u???????
            with open(new_file_path, 'w', encoding='utf-8') as file:
                file.write(m3u_content)
                
            print(f'???? {file_name} ???')
        else:
            print(f'???? {file_name}???txt???')

# ???????EPG URL
folder_path = 'dsyy'
epg_url = 'http://epg.51zmt.top:8000/e.xml'

# ????????
convert_txt_to_m3u(folder_path, epg_url)
