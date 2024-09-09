import os
import subprocess
import requests
import datetime

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"错误: {error.decode('utf-8')}")
        exit(1)
    return output.decode('utf-8').strip()

def print_current_time(message):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{message} {current_time}")

# 1. 获取脚本所在路径和系统时间日期
script_path = os.path.dirname(os.path.abspath(__file__))
print(f"脚本所在路径：{script_path}")
print_current_time("系统时间：")

# 2. 切换到程序所在目录
os.chdir(script_path)
print("切换到程序所在目录...")

# 3. 设置 Git 用户名和邮箱
run_command('git config user.name "vbskycn"')
run_command('git config user.email "zhoujie218@gmail.com"')

# 4. 执行 Git 操作，放弃本地更改并拉取最新代码
print("正在执行 Git 操作...")
run_command('git fetch origin')
run_command('git reset --hard origin/master')
run_command('git clean -fd')
run_command('git pull')

# 5. 下载文件列表
print("正在下载文件...")
files_to_download = [
    {
        "url": "https://tv.zhoujie218.top/tv/liebiao/jxdx_hd.txt",
        "filename": "jxdx_hd.txt"
    },
    {
        "url": "https://tv.zhoujie218.top/tv/liebiao/jxdx_hd.m3u",
        "filename": "jxdx_hd.m3u"
    },
    # 在这里添加更多的文件下载信息
    # 例如：
    # {
    #     "url": "https://example.com/another_file.txt",
    #     "filename": "another_file.txt"
    # },
]

for file_info in files_to_download:
    url = file_info["url"]
    filename = file_info["filename"]
    file_path = os.path.join(script_path, filename)

    print(f"正在下载 {filename} 文件...")
    response = requests.get(url)
    if response.status_code == 200:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
        print(f"成功下载并保存 {filename} 到 {file_path}")
    else:
        print(f"下载失败 {filename}, 状态码: {response.status_code}")
        exit(1)

# 6. 同步文件
print("正在同步文件...")
files_to_sync = ['iptv4.txt', 'iptv4.m3u', 'iptv6.txt', 'iptv6.m3u']
for file in files_to_sync:
    source = f"/docker/iptv4/{file}"
    destination = os.path.join(script_path, file)
    run_command(f'cp {source} {destination}')

# 7. 合并文件
print("正在合并文件...")
output_file = os.path.join(script_path, 'hd.txt')
files_to_merge = ['jxdx_hd.txt', 'iptv4.txt', 'iptv6.txt']
replacements = {
    'jxdx_hd.txt': 'jxH,#genre#',
    'iptv6.txt': 'ip6,#genre#',
    'iptv4.txt': 'ip4,#genre#'
}

with open(output_file, 'w', encoding='utf-8') as outfile:
    for filename in files_to_merge:
        filepath = os.path.join(script_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                if filename in replacements:
                    content = content.replace(',#genre#', replacements[filename])
                outfile.write(content)
                outfile.write('\n')
        else:
            print(f'警告：文件 {filepath} 不存在，已跳过')

print(f'文件已合并到 {output_file}')

# 8. 提交更改并推送到 GitHub
print("正在提交更改并推送...")
run_command('git add .')
commit_message = f"debian100 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 同步IPTV4仓库文件和处理新文件"
run_command(f'git commit -m "{commit_message}"')
run_command('git push')

print("脚本执行完成")