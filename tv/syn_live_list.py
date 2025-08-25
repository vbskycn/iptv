import requests
import os
import shutil
import filecmp
import datetime

# 打印当前时间的函数
def print_current_time(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{message} {current_time}")

# 从环境变量获取 GitHub 令牌
GITHUB_TOKEN = os.getenv('MY_GITHUB_TOKEN')

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN is not set")

# 需要下载并处理的文件URL
urls_to_process = [
    #'https://raw.githubusercontent.com/vbskycn/my_code/master/me/jxdx_hd.txt',
    #'https://raw.githubusercontent.com/vbskycn/my_code/master/me/jxdx_hd.m3u',    
    'https://raw.githubusercontent.com/vbskycn/iptv4/master/iptv6.txt',
    'https://raw.githubusercontent.com/vbskycn/iptv4/master/iptv4.txt',
    'https://raw.githubusercontent.com/vbskycn/iptv4/master/iptv4.m3u',
    'https://raw.githubusercontent.com/vbskycn/iptv4/master/iptv6.m3u'


    
]

# 仅需下载的文件URL
urls_to_download_only = [ 
    #'https://raw.githubusercontent.com/vbskycn/my_code/master/me/cs.m3u'
]

# 对应txt文件的分组标记替换规则
replacements = {
    'iptv6.txt': 'ip6,#genre#',
    'iptv4.txt': 'ip4,#genre#'
    
}

# 保存合并结果的文件名
output_file = 'hd.txt'

# 用于存储合并后的内容
merged_content = []

# 下载并处理每个文件
def download_and_process_files(urls, process_content):
    for url in urls:
        headers = {
            'Authorization': f'token {GITHUB_TOKEN}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            content = response.text
            # 保存下载的文件到当前目录
            filename = os.path.basename(url)
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f'成功下载并保存 {filename}')

            # 处理txt文件，替换分组标记
            if process_content and filename in replacements:
                modified_content = content.replace(',#genre#', replacements[filename])
                merged_content.append(modified_content)
        else:
            print(f'下载失败 {url}, 状态码: {response.status_code}')

# 在程序开始时打印当前时间
print_current_time("程序开始执行时间：")

# 下载并处理需要合并的文件
download_and_process_files(urls_to_process, process_content=True)

# 下载仅需下载的文件
download_and_process_files(urls_to_download_only, process_content=False)

# 将所有内容合并成一个文件
with open(output_file, 'w', encoding='utf-8') as f:
    for content in merged_content:
        f.write(content)
        f.write('\n')

print(f'所有文件已下载、保存并合并到 {output_file}')

# 在程序结束时打印当前时间
print_current_time("程序执行完成时间：")
